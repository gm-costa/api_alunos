from typing import Optional
from ninja import ModelSchema, Schema
from .models import Aluno

class AlunoSchema(ModelSchema):
    class Meta:
        model = Aluno
        fields = ['nome', 'email', 'data_nascimento', 'faixa']

