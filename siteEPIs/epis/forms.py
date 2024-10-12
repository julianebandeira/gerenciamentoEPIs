from django import forms
from .models import Entrega, Colaborador, EPI

class EntregaForm(forms.ModelForm):
    class Meta:
        model = Entrega
        fields = ['equipamento', 'colaborador', 'data_emprestimo', 'data_prevista_devolucao', 
                  'condicoes_equipamento', 'status', 'data_devolucao', 'observacao']
        widgets = {
            'data_emprestimo': forms.DateInput(attrs={'type': 'date'}),
            'data_prevista_devolucao': forms.DateInput(attrs={'type': 'date'}),
            'data_devolucao': forms.DateInput(attrs={'type': 'date'}),
        }

class ColaboradorForm(forms.ModelForm):
    class Meta:
        model = Colaborador
        fields = ['nome', 'cpf', 'telefone', 'funcao']

class EPIForm(forms.ModelForm):
    class Meta:
        model = EPI
        fields = ['nome_epi', 'funcoes', 'descricao', 'tempo_uso_recomendado']