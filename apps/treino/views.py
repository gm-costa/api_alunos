from datetime import date
from typing import List
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.errors import HttpError
from .schemas import AlunoSchema, AulaRealizadaSchema, ProgressoAlunoSchema, UpdateAlunoSchema
from .models import Aluno, AulasConcluidas
from .graduacao import order_faixas, calcular_qtd_aulas_evoluir_de_faixa


treino_router = Router()

@treino_router.post('/', response={200: str})
def criar_aluno(request, aluno_schema: AlunoSchema):

    nome, email, *_  = aluno_schema.dict().values()

    if not all((nome, email)):
        raise HttpError(400, 'Nome e e-mail são obrigatórios.')

    if Aluno.objects.filter(email=email).exists():
        raise HttpError(400, "E-mail já cadastrado.")
    
    aluno = Aluno(**aluno_schema.dict())
    
    try:
        aluno.save()
        return 200, f'{aluno.nome} foi cadastrado com sucesso.'
    except Exception as e:
        raise HttpError(400, f'Erro: {e}.')

@treino_router.get('alunos/', response=List[AlunoSchema])
def listar_alunos(request, nome: str = '*'):
    alunos = Aluno.objects.all()
    if nome != '*':
        alunos = alunos.filter(nome__startswith=nome)
    
    return alunos

@treino_router.put("alunos/{aluno_id}", response={200: str, 400:str})
def update_aluno(request, aluno_id: int, aluno_data: AlunoSchema):

    aluno = get_object_or_404(Aluno, id=aluno_id)
    
    idade = date.today() - aluno_data.data_nascimento

    if int(idade.days/365) < 18 and aluno_data.dict()['faixa'] in ('A', 'R', 'M', 'P'):
        return 400, f'Menor de 18 anos não pode ser graduado para a faixa informada.'

    for key, value in aluno_data.dict().items():
        if key == 'nome':
            value=value.title()
        if key == 'email':
            value=value.lower()
        if value:
            setattr(aluno, key, value)

    try:
        aluno.save()
        return 200, 'Atualização realizada com sucesso.'
    except Exception as e:
        return 400, f'Erro: {e}.'

@treino_router.post('aula-realizada/', response={200: str, 400:str})
def aula_realizada(request, aula_realizada: AulaRealizadaSchema):
    qtd, email_aluno = aula_realizada.dict().values()

    if qtd < 1:
        return 400, 'Quantidade de aulas deve ser maior que zero (0).'
    
    if not email_aluno:
        return 400, 'E-mail não informado !'
    
    try:
        aluno = Aluno.objects.get(email=email_aluno)
    except Aluno.DoesNotExist:
        return 400, f'Não existe aluno com o e-mail {email_aluno} !'

    aulas = [AulasConcluidas(aluno=aluno, faixa_atual=aluno.faixa) for _ in range(qtd)]
    
    try:
        AulasConcluidas.objects.bulk_create(aulas)
        return 200, f'Aula(s) marcada(s) como realizada para {aluno.nome}.'
    except Exception as ex:
        return 400, f'Erro: {ex}.'

@treino_router.get('progresso-aluno/', response={200: ProgressoAlunoSchema, 400: str})
def progresso_aluno(request, email_aluno: str):
    if not email_aluno:
        return 400, 'E-mail não informado !'
    
    try:
        aluno = Aluno.objects.get(email=email_aluno)
        
        faixa_atual = aluno.get_faixa_display()
        
        nivel_faixa = order_faixas.get(faixa_atual, 0)
    
        total_aulas_proxima_faixa = calcular_qtd_aulas_evoluir_de_faixa(nivel_faixa)

        total_aulas_concluidas_faixa = AulasConcluidas.objects.filter(aluno=aluno, faixa_atual=aluno.faixa).count()

        aulas_faltantes = max(total_aulas_proxima_faixa - total_aulas_concluidas_faixa, 0)

        return {
            'nome': aluno.nome.title(),
            'email': aluno.email,
            'faixa': aluno.get_faixa_display(),
            'total_aulas_proxima_faixa': total_aulas_proxima_faixa,
            'total_aulas_concluidas_faixa_atual': total_aulas_concluidas_faixa,
            'total_aulas_faltantes_proxima_faixa': aulas_faltantes,
        }

    except Aluno.DoesNotExist:
        return 400, f'Não existe aluno com o e-mail {email_aluno} !'
    
@treino_router.get('alunos/busca/', response={200: UpdateAlunoSchema, 400: str})
def busca_aluno(request, email_aluno: str):
    if not email_aluno:
        return 400, 'E-mail não informado !'
    
    try:
        aluno = Aluno.objects.get(email=email_aluno)
        
        return 200, aluno

    except Aluno.DoesNotExist:
        return 400, f'Não existe aluno com o e-mail {email_aluno} !'
    except Exception as ex:
        return 400, f'Erro: {ex}.'
