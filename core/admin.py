from django import forms
from django.contrib import admin

from .models import CategoriaGaleria, EventoGaleria, ImagemGaleria, InformacoesEmpresa, Lead


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    widget = MultipleFileInput

    def clean(self, data, initial=None):
        if not data:
            return []

        if not isinstance(data, (list, tuple)):
            data = [data]

        cleaned_files = []
        errors = []
        for uploaded_file in data:
            try:
                cleaned_files.append(super().clean(uploaded_file, initial))
            except forms.ValidationError as exc:
                errors.extend(exc.error_list)

        if errors:
            raise forms.ValidationError(errors)

        return cleaned_files


class ImagemGaleriaAdminForm(forms.ModelForm):
    imagens = MultipleFileField(
        required=False,
        widget=MultipleFileInput(attrs={'multiple': True}),
        help_text='Você pode selecionar várias imagens de uma vez.',
    )

    class Meta:
        model = ImagemGaleria
        fields = ('evento', 'titulo', 'imagens', 'formato', 'alt_texto', 'ordem', 'ativo', 'destaque_home')

    def clean(self):
        cleaned_data = super().clean()
        imagens = cleaned_data.get('imagens') or []
        if not self.instance.pk and not imagens:
            raise forms.ValidationError('Envie ao menos uma imagem.')
        if not cleaned_data.get('evento'):
            raise forms.ValidationError('Selecione o evento para esta imagem.')
        return cleaned_data


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo_evento', 'email', 'telefone', 'criado_em')
    list_filter = ('tipo_evento', 'criado_em')
    search_fields = ('nome', 'email', 'telefone', 'mensagem')
    readonly_fields = ('criado_em',)


@admin.register(InformacoesEmpresa)
class InformacoesEmpresaAdmin(admin.ModelAdmin):
    list_display = (
        'nome_empresa',
        'telefone_whatsapp',
        'email_contato',
        'instagram_usuario',
        'facebook_usuario',
        'tiktok_usuario',
        'atualizado_em',
    )
    readonly_fields = ('atualizado_em',)

    def has_add_permission(self, request):
        # Mantem registro unico para facilitar gestao via admin.
        if InformacoesEmpresa.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(CategoriaGaleria)
class CategoriaGaleriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'slug', 'ativo', 'criado_em')
    list_filter = ('ativo', 'criado_em')
    search_fields = ('nome', 'slug')
    prepopulated_fields = {'slug': ('nome',)}
    readonly_fields = ('criado_em',)


@admin.register(EventoGaleria)
class EventoGaleriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'data_evento', 'local', 'ativo', 'criado_em')
    list_filter = ('categoria', 'ativo', 'data_evento', 'criado_em')
    search_fields = ('nome', 'categoria__nome', 'local', 'descricao', 'slug')
    prepopulated_fields = {'slug': ('nome',)}
    readonly_fields = ('criado_em',)


@admin.register(ImagemGaleria)
class ImagemGaleriaAdmin(admin.ModelAdmin):
    form = ImagemGaleriaAdminForm
    list_display = ('titulo', 'evento', 'formato', 'destaque_home', 'ordem', 'ativo', 'criado_em')
    list_filter = ('evento', 'formato', 'destaque_home', 'ativo', 'criado_em')
    search_fields = ('titulo', 'alt_texto', 'evento__nome')
    list_editable = ('destaque_home', 'ordem', 'ativo')
    readonly_fields = ('criado_em',)
    exclude = ('categoria', 'imagem')

    def save_model(self, request, obj, form, change):
        uploaded_files = form.cleaned_data.get('imagens') or []
        if uploaded_files:
            obj.imagem = uploaded_files[0]
        super().save_model(request, obj, form, change)
        if len(uploaded_files) <= 1:
            return

        for index, image_file in enumerate(uploaded_files[1:], start=1):
            ImagemGaleria.objects.create(
                evento=obj.evento,
                titulo=f'{obj.titulo} {index + 1}',
                imagem=image_file,
                formato=obj.formato,
                alt_texto=obj.alt_texto,
                ordem=obj.ordem + index,
                ativo=obj.ativo,
                destaque_home=obj.destaque_home,
            )
