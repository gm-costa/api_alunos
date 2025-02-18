from datetime import date
from typing import List
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.errors import HttpError
from .schemas import AlunoSchema
from .models import Aluno


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
        return 200, 'Aluno cadastrado com sucesso.'
    except Exception as e:
        raise HttpError(400, f'Erro: {e}.')

@treino_router.get('alunos/', response=List[AlunoSchema])
def listar_alunos(request):
    alunos = Aluno.objects.all()
    return alunos

@treino_router.put("alunos/{aluno_id}/", response={200: str})
def update_aluno(request, aluno_id: int, aluno_data: AlunoSchema):

    aluno = get_object_or_404(Aluno, id=aluno_id)
    
    idade = date.today() - aluno.data_nascimento

    if int(idade.days/365) < 18 and aluno_data.dict()['faixa'] in ('A', 'R', 'M', 'P'):
        raise HttpError(400, f'Menor de 18 anos não pode ser graduado para a faixa informada.')

    for key, value in aluno_data.dict().items():
        if value:
            setattr(aluno, key, value)

    try:
        aluno.save()
        return 200, 'Atualização realizada com sucesso.'
    except Exception as e:
        HttpError(400, f'Erro: {e}.')
