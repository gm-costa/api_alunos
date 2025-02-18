from typing import Optional
from ninja import ModelSchema, Schema
from .models import Aluno

class AlunoSchema(ModelSchema):
    class Meta:
        model = Aluno
        fields = ['nome', 'email', 'data_nascimento', 'faixa']

class AulaRealizadaSchema(Schema):
    qtd: Optional[int] = 1
    email_aluno: str
