import re

from django import forms

from .models import Lead


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['nome', 'telefone', 'email', 'tipo_evento', 'mensagem']
        labels = {
            'nome': 'Nome',
            'telefone': 'Telefone',
            'email': 'E-mail',
            'tipo_evento': 'Tipo de evento',
            'mensagem': 'Mensagem',
        }
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Seu nome completo'}),
            'telefone': forms.TextInput(
                attrs={
                    'placeholder': '+351 912 345 678',
                    'inputmode': 'tel',
                    'autocomplete': 'tel',
                }
            ),
            'email': forms.EmailInput(attrs={'placeholder': 'voce@exemplo.com'}),
            'tipo_evento': forms.TextInput(
                attrs={'placeholder': 'Ex.: Chá da tarde, aniversário, mini wedding'}
            ),
            'mensagem': forms.Textarea(
                attrs={
                    'rows': 5,
                    'placeholder': 'Conte mais sobre o seu evento, data prevista e número de convidados.',
                }
            ),
        }

    def clean_telefone(self):
        telefone = self.cleaned_data['telefone'].strip()
        digits = re.sub(r'\D', '', telefone)
        if digits.startswith('351'):
            digits = digits[3:]
        if len(digits) != 9 or digits[0] != '9':
            raise forms.ValidationError('Informe um telefone português válido. Ex.: +351 912 345 678')
        return telefone
