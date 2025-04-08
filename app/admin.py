from django.contrib import admin
from .models import (
    Endereco,
    Empresa,
    Usuario,
    UsuarioEmpresa,
    TentativaAcesso,
    TentativaAcessoAnonimo,
    Face,
    FaceAnonima,
    Alerta,
    AlertaAnonimo,
    Relatorio,
)

models_admin = [
    Endereco,
    Empresa,
    Usuario,
    UsuarioEmpresa,
    TentativaAcesso,
    Face,
    Alerta,
    Relatorio,
    TentativaAcessoAnonimo,
    FaceAnonima,
    AlertaAnonimo,
]

for model in models_admin:
    admin.site.register(model)
