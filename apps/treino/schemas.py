from typing import Optional
from ninja import ModelSchema, Schema
from .models import Aluno

class AlunoSchema(ModelSchema):
    class Meta:
        model = Aluno
        fields = ['nome', 'email', 'data_nascimento', 'faixa']

class UpdateAlunoSchema(ModelSchema):
    class Meta:
        model = Aluno
        fields = '__all__'

class AulaRealizadaSchema(Schema):
    qtd: Optional[int] = 1
    email_aluno: str

class ProgressoAlunoSchema(Schema):
    nome: str
    email: str
    faixa: str
    total_aulas_proxima_faixa: int
    total_aulas_concluidas_faixa_atual: int
    total_aulas_faltantes_proxima_faixa: int
