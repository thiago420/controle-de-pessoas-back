from django.db import models
from django.utils import timezone

class Endereco(models.Model):
    id = models.AutoField(primary_key=True)
    nu_cep = models.CharField(max_length=9)  # Formato: 00000-000
    nm_logradouro = models.CharField(max_length=100)  # Rua, Avenida, etc.
    nu_numero = models.CharField(max_length=20)  # CharField para permitir valores como "s/n"
    ds_complemento = models.CharField(max_length=100, blank=True, null=True)
    nm_bairro = models.CharField(max_length=50)
    nm_cidade = models.CharField(max_length=50)
    sg_estado = models.CharField(max_length=2)
    nm_pais = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'
        ordering = ['nm_pais','nm_cidade', 'sg_estado', 'nm_bairro', 'nm_logradouro']  # Ordem padrão
        db_table = 'tb_endereco'  # Nome personalizado da tabela no DB
    
    def _str_(self):
        return f"{self.logradouro}, {self.numero}\n{self.bairro}\n{self.cidade}/{self.estado}\n{self.cep}"

class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    nm_nome = models.CharField(max_length=100)
    ds_email = models.EmailField(unique=True)
    nu_telefone = models.CharField(max_length=15, blank=True, null=True)
    nu_cpf = models.CharField(max_length=15)
    id_endereco = models.ForeignKey(
        Endereco, 
        on_delete=models.SET_NULL,  # Não exclui o usuário se o endereço for excluído
        related_name='usuarios',     # Para acessar usuários a partir do endereço
        null=True,                  # Permite que o usuário não tenha endereço
        verbose_name='Endereço'
    )
    ds_senha_hash = models.CharField(max_length=200)
    bl_bloqueado = models.BooleanField(default=False)
    nu_tentativas_falhas = models.IntegerField()
    dt_bloqueio = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.pk:
            # Obtém o registro anterior para comparar o valor de bl_bloqueado
            old = Usuario.objects.get(pk=self.pk)
            if not old.bl_bloqueado and self.bl_bloqueado:
                self.dt_bloqueio = timezone.now()
        else:
            # Caso o usuário já seja criado como bloqueado
            if self.bl_bloqueado and not self.dt_bloqueio:
                self.dt_bloqueio = timezone.now()
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['nm_nome']
        db_table = 'tb_usuario'
    
    def _str_(self):
        f"{self.nm_nome} ({self.ds_email})"

class Face(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE,  
        related_name='faces',     
        null=True,                  
        verbose_name='Usuario'
    )
    ###FALTA IMAGEM
    dt_criado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Face'
        verbose_name_plural = 'Faces'
        db_table = 'tb_face'

class Empresa(models.Model):
    id = models.AutoField(primary_key=True)
    id_endereco = models.ForeignKey(
        Endereco, 
        on_delete=models.SET_NULL,  
        related_name='empresas',     
        null=True,                  
        verbose_name='Endereço'
    )
    nm_nome = models.CharField(max_length=100)
    ds_cnpj = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        db_table = 'tb_empresa'
    
    def _str_(self):
        return f"{self.nm_nome} - {self.ds_cnpj}"

class UsuarioEmpresa(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE,  
        related_name='usuariosempresa',     
        null=True,                  
        verbose_name='Usuario'
    )
    empresa = models.ForeignKey(
        Empresa, 
        on_delete=models.CASCADE,  
        related_name='usuariosempresas',     
        null=True,                  
        verbose_name='Empresa'
    )
    ds_usuario_permissao = models.CharField(max_length=20)

class Relatorio(models.Model):
    id = models.AutoField(primary_key=True)
    id_empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,  
        related_name='relatorios',     
        null=True,                  
        verbose_name='Empresa'
    )
    tp_relatorio = models.CharField(max_length=50)
    js_conteudo = models.JSONField()
    dt_criado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Relatorio'
        verbose_name_plural = 'Relatorios'
        db_table = 'tb_relatorio'

class TentativaAcesso(models.Model):
    id_usuario_empresa = models.ForeignKey(
        UsuarioEmpresa,
        on_delete=models.CASCADE,
        related_name='tentativasAcesso',
        null=True,
        verbose_name='UsuarioEmpresa'
    )
    dt_tentativa = models.DateTimeField(auto_now_add=True)
    bl_sucesso = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Tentativa de Acesso'
        verbose_name_plural = 'Tentativas de Acesso'
        db_table = 'tb_tentativa_acesso'
    
class Alerta(models.Model):
    id = models.AutoField(primary_key=True)
    id_usuario_empresa = models.ForeignKey(
        UsuarioEmpresa,
        on_delete=models.CASCADE,
        related_name='alertas',
        null=True,
        verbose_name='UsuarioEmpresa'
    )
    tp_alerta = models.CharField(max_length=50)
    ds_mensagem = models.JSONField()
    dt_criado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Alerta'
        verbose_name_plural = 'Alertas'
        db_table = 'tb_alerta'

class TentativaAcessoAnonimo(models.Model):
    id_empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,  
        related_name='tentativasAcessoAnonimos',     
        null=True,                  
        verbose_name='Empresa'
    )
    dt_tentativa = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Tentativa Acesso Anonimo'
        verbose_name_plural = 'Tentativas de Acesso Anonimo'
        db_table = 'tb_tentativa_acesso_anonimo'

class FaceAnonima(models.Model):
    id_tentativa_acesso_anonimo = models.ForeignKey(
        TentativaAcessoAnonimo,
        on_delete=models.SET_NULL,  #CONFERIR COM TIAGO
        related_name='facesanonimas',     
        null=True,                  
        verbose_name='Tentativa de Acesso Anonimo'
    )
    #COLOCAR IMAGEM
    dt_criado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Face Anonimas'
        verbose_name_plural = 'Faces Anonimas'
        db_table = 'tb_face_anonima' 
