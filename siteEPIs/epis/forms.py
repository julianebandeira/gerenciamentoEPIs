from django import forms
from .models import Entrega

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