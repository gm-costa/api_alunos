from typing import List
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
