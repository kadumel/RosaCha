import re

from django.db import models


class Lead(models.Model):
    nome = models.CharField(max_length=120)
    telefone = models.CharField(max_length=30)
    email = models.EmailField()
    tipo_evento = models.CharField(max_length=100)
    mensagem = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']
        verbose_name = 'Lead'
        verbose_name_plural = 'Leads'

    def __str__(self):
        return f'{self.nome} - {self.tipo_evento}'


class InformacoesEmpresa(models.Model):
    nome_empresa = models.CharField(max_length=120, default='Rosa Chá Catering')
    telefone_whatsapp = models.CharField(max_length=30, default='+351 932 079 149')
    email_contato = models.EmailField(default='contato@rosachacatering.pt')
    instagram_url = models.URLField(default='https://instagram.com')
    instagram_usuario = models.CharField(max_length=80, default='@rosacha')
    facebook_url = models.URLField(default='https://facebook.com', blank=True)
    facebook_usuario = models.CharField(max_length=80, default='@rosacha', blank=True)
    tiktok_url = models.URLField(default='https://tiktok.com', blank=True)
    tiktok_usuario = models.CharField(max_length=80, default='@rosacha', blank=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Informações da empresa'
        verbose_name_plural = 'Informações da empresa'

    def __str__(self):
        return self.nome_empresa

    @property
    def whatsapp_digits(self):
        return re.sub(r'\D', '', self.telefone_whatsapp or '')

    @property
    def whatsapp_url(self):
        digits = self.whatsapp_digits
        return f'https://wa.me/{digits}' if digits else '#'


class CategoriaGaleria(models.Model):
    nome = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nome']
        verbose_name = 'Categoria da galeria'
        verbose_name_plural = 'Categorias da galeria'

    def __str__(self):
        return self.nome


class EventoGaleria(models.Model):
    categoria = models.ForeignKey(
        CategoriaGaleria,
        on_delete=models.PROTECT,
        related_name='eventos',
        null=True,
    )
    nome = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)
    data_evento = models.DateField(null=True, blank=True)
    local = models.CharField(max_length=140, blank=True)
    descricao = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data_evento', 'nome']
        verbose_name = 'Evento da galeria'
        verbose_name_plural = 'Eventos da galeria'

    def __str__(self):
        if self.categoria:
            return f'{self.nome} ({self.categoria.nome})'
        return self.nome


class ImagemGaleria(models.Model):
    class Formato(models.TextChoices):
        HORIZONTAL = 'horizontal', 'Horizontal'
        VERTICAL = 'vertical', 'Vertical'
        DESTAQUE = 'destaque', 'Destaque'

    categoria = models.ForeignKey(
        CategoriaGaleria,
        on_delete=models.PROTECT,
        related_name='imagens',
        null=True,
        blank=True,
    )
    evento = models.ForeignKey(
        EventoGaleria,
        on_delete=models.PROTECT,
        related_name='imagens',
        null=True,
        blank=True,
    )
    titulo = models.CharField(max_length=120)
    imagem = models.ImageField(upload_to='galeria/')
    formato = models.CharField(
        max_length=20,
        choices=Formato.choices,
        default=Formato.HORIZONTAL,
    )
    alt_texto = models.CharField(max_length=160, blank=True)
    ativo = models.BooleanField(default=True)
    destaque_home = models.BooleanField(default=False)
    ordem = models.PositiveIntegerField(default=0)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['ordem', '-criado_em']
        verbose_name = 'Imagem da galeria'
        verbose_name_plural = 'Imagens da galeria'

    def __str__(self):
        return self.titulo
