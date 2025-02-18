from ninja import NinjaAPI
from apps.treino.views import treino_router

api = NinjaAPI()

api.add_router('', treino_router)
