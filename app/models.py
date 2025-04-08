from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField

class Endereco(models.Model):
    nu_cep = models.IntegerField()
    ds_complemento = models.CharField(max_length=100)
    nu_numero = models.IntegerField()
    nm_rua = models.CharField(max_length=100)
    nm_bairro = models.CharField(max_length=50)
    nm_cidade = models.CharField(max_length=50)
    sg_estado = models.CharField(max_length=50)
    nm_pais = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nm_rua}, {self.nu_numero} - {self.nm_cidade}"


class Empresa(models.Model):
    id_endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)
    nm_nome = models.CharField(max_length=100)
    ds_cnpj = models.CharField(max_length=20)

    def __str__(self):
        return self.nm_nome


class Usuario(models.Model):
    id_endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)
    nm_nome = models.CharField(max_length=100)
    nu_cpf = models.BigIntegerField()
    ds_email = models.EmailField()
    nu_telefone = models.BigIntegerField()
    ds_senha_hash = models.CharField(max_length=200)
    bl_bloqueado = models.BooleanField(default=False)
    nu_tentativas_falhas = models.IntegerField(default=0)
    dt_bloqueio = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.nm_nome


class UsuarioEmpresa(models.Model):
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    ds_usuario_permissao = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.id_usuario} - {self.id_empresa}"


class TentativaAcesso(models.Model):
    id_usuario_empresa = models.ForeignKey(UsuarioEmpresa, on_delete=models.CASCADE)
    dt_tentativa = models.DateTimeField(auto_now_add=True)
    bl_sucesso = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id_usuario_empresa} - {self.dt_tentativa}"


class Face(models.Model):
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    bt_image = models.BinaryField()
    dt_criado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Face do {self.id_usuario}"


class Alerta(models.Model):
    id_usuario_empresa = models.ForeignKey(UsuarioEmpresa, on_delete=models.CASCADE)
    tp_alerta = models.CharField(max_length=50)
    ds_mensagem = models.JSONField()
    dt_criado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alerta: {self.tp_alerta}"


class Relatorio(models.Model):
    id_empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    tp_relatorio = models.CharField(max_length=50)
    js_conteudo = models.JSONField()
    dt_criado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Relatório: {self.tp_relatorio} - Empresa: {self.id_empresa}"


class TentativaAcessoAnonimo(models.Model):
    id_empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    dt_tentativa = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Anonimo - {self.dt_tentativa}"


class FaceAnonima(models.Model):
    id_tentativa_acesso_anonimo = models.ForeignKey(TentativaAcessoAnonimo, on_delete=models.CASCADE)
    bt_image = models.BinaryField()
    dt_criado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Face Anônima - {self.dt_criado}"


class AlertaAnonimo(models.Model):
    id_empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)  # Correção aplicada!
    tp_alerta = models.CharField(max_length=50)
    js_mensagem = models.JSONField()
    dt_criado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alerta Anônimo: {self.tp_alerta}"
