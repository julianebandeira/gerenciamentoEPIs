from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Colaborador, EPI, Entrega
from django.http import HttpResponse
import csv

def index(request):
    return render(request, 'index.html')

def colaboradores(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        cpf = request.POST['cpf']
        telefone = request.POST['telefone']
        funcao = request.POST['funcao']
        
        Colaborador.objects.create(nome=nome, cpf=cpf, telefone=telefone, funcao=funcao)
        messages.success(request, 'Colaborador cadastrado com sucesso!')
        return redirect('colaboradores')
    
    colaboradores = Colaborador.objects.all()
    return render(request, 'colaboradores.html', {'colaboradores': colaboradores})

def epis(request):
    if request.method == 'POST':
        nome_epi = request.POST['nomeEPI']
        funcoes = request.POST['funcoes']
        descricao = request.POST['descricao']
        tempo_uso = request.POST['tempoUso']
        
        EPI.objects.create(nome_epi=nome_epi, funcoes=funcoes, descricao=descricao, tempo_uso_recomendado=tempo_uso)
        messages.success(request, 'EPI cadastrado com sucesso!')
        return redirect('epis')
    
    epis = EPI.objects.all()
    return render(request, 'epis.html', {'epis': epis})

def entrega(request):
    if request.method == 'POST':
        equipamento = EPI.objects.get(id=request.POST['equipamento'])
        colaborador = Colaborador.objects.get(id=request.POST['colaborador'])
        data_emprestimo = request.POST['dataEmprestimo']
        data_prevista_devolucao = request.POST['dataPrevistaDevolucao']
        condicoes_equipamento = request.POST['condicoesEquipamento']
        status = request.POST['status']
        
        # Inicializa data_devolucao e observacao como None
        data_devolucao = None
        observacao = None
        
        # Se o status não for "Em uso", pega os valores adicionais
        if status != 'Em uso':
            data_devolucao = request.POST.get('dataDevolucao') or None
            observacao = request.POST.get('observacao') or None
        
        Entrega.objects.create(
            equipamento=equipamento,
            colaborador=colaborador,
            data_emprestimo=data_emprestimo,
            data_prevista_devolucao=data_prevista_devolucao,
            condicoes_equipamento=condicoes_equipamento,
            status=status,
            data_devolucao=data_devolucao,
            observacao=observacao
        )
        messages.success(request, 'Entrega registrada com sucesso!')
        return redirect('entrega')
    
    epis = EPI.objects.all()
    colaboradores = Colaborador.objects.all()
    return render(request, 'entrega.html', {'epis': epis, 'colaboradores': colaboradores})

def avisos(request):
    return render(request, 'avisos.html')

def gerar_relatorio(request):
    if request.method == 'POST':
        tipo_relatorio = request.POST['tipoRelatorio']
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{tipo_relatorio}.csv"'
        
        writer = csv.writer(response)
        
        if tipo_relatorio == 'epis':
            writer.writerow(['Nome', 'Funções', 'Descrição', 'Tempo de Uso Recomendado'])
            for epi in EPI.objects.all():
                writer.writerow([epi.nome_epi, epi.funcoes, epi.descricao, epi.tempo_uso_recomendado])
        elif tipo_relatorio == 'colaboradores':
            writer.writerow(['Nome', 'CPF', 'Telefone', 'Função'])
            for colaborador in Colaborador.objects.all():
                writer.writerow([colaborador.nome, colaborador.cpf, colaborador.telefone, colaborador.funcao])
        elif tipo_relatorio == 'emprestimos':
            writer.writerow(['Equipamento', 'Colaborador', 'Data Empréstimo', 'Data Prevista Devolução', 'Status'])
            for entrega in Entrega.objects.all():
                writer.writerow([entrega.equipamento.nome_epi, entrega.colaborador.nome, entrega.data_emprestimo, entrega.data_prevista_devolucao, entrega.status])
        
        return response

    # Se não for uma requisição POST, redireciona para a página de avisos
    return redirect('avisos')