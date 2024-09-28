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

def editar_colaboradores(request):
    colaboradores = Colaborador.objects.all()
    return render(request, 'editar_colb.html', {'colaboradores': colaboradores})

def editar_colaborador(request, colaborador_id):
    colaborador = get_object_or_404(Colaborador, id=colaborador_id)
    if request.method == 'POST':
        # Lógica para atualizar o colaborador
        colaborador.nome = request.POST['nome']
        colaborador.cpf = request.POST['cpf']
        colaborador.telefone = request.POST['telefone']
        colaborador.funcao = request.POST['funcao']
        colaborador.save()
        messages.success(request, 'Colaborador atualizado com sucesso!')
        return redirect('editar_colaboradores')
    return render(request, 'editar_colaborador.html', {'colaborador': colaborador})

def excluir_colaborador(request, colaborador_id):
    colaborador = get_object_or_404(Colaborador, id=colaborador_id)
    colaborador.delete()
    messages.success(request, 'Colaborador excluído com sucesso!')
    return redirect('editar_colaboradores')

def editar_epis(request):
    epis = EPI.objects.all()
    return render(request, 'editar_epis.html', {'epis': epis})

def editar_epi(request, epi_id):
    epi = get_object_or_404(EPI, id=epi_id)
    if request.method == 'POST':
        # Lógica para atualizar o EPI
        epi.nome_epi = request.POST['nome_epi']
        epi.funcoes = request.POST['funcoes']
        epi.descricao = request.POST['descricao']
        epi.tempo_uso_recomendado = request.POST['tempo_uso_recomendado']
        epi.save()
        messages.success(request, 'EPI atualizado com sucesso!')
        return redirect('editar_epis')
    return render(request, 'editar_epi.html', {'epi': epi})

def excluir_epi(request, epi_id):
    epi = get_object_or_404(EPI, id=epi_id)
    epi.delete()
    messages.success(request, 'EPI excluído com sucesso!')
    return redirect('editar_epis')

def consultar_entrega(request):
    search_performed = False
    entregas = None
    if 'colaborador' in request.GET:
        search_performed = True
        colaborador_nome = request.GET['colaborador']
        entregas = Entrega.objects.filter(colaborador__nome__icontains=colaborador_nome)
    return render(request, 'consultar_entrega.html', {
        'entregas': entregas,
        'search_performed': search_performed
    })

def editar_entrega(request, entrega_id):
    entrega = get_object_or_404(Entrega, id=entrega_id)
    if request.method == 'POST':
        # Lógica para atualizar a entrega
        entrega.status = request.POST['status']
        entrega.data_devolucao = request.POST.get('data_devolucao')
        entrega.observacao = request.POST.get('observacao')
        entrega.save()
        messages.success(request, 'Entrega atualizada com sucesso!')
        return redirect('consultar_entrega')
    return render(request, 'editar_entrega.html', {'entrega': entrega})