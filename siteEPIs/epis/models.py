from django.db import models

class Colaborador(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=15)
    funcao = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

class EPI(models.Model):
    nome_epi = models.CharField(max_length=100)
    funcoes = models.TextField()
    descricao = models.TextField()
    tempo_uso_recomendado = models.IntegerField()  # em dias

    def __str__(self):
        return self.nome_epi

class Entrega(models.Model):
    equipamento = models.ForeignKey(EPI, on_delete=models.CASCADE)
    colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE)
    data_emprestimo = models.DateField()
    data_prevista_devolucao = models.DateField()
    condicoes_equipamento = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    data_devolucao = models.DateField(null=True, blank=True)
    observacao = models.TextField(null=True, blank=True)  # Modificado esta linha

    def __str__(self):
        return f"{self.equipamento} - {self.colaborador} - {self.status}"