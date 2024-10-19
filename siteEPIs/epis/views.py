from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Colaborador, EPI, Entrega
from django.http import HttpResponse
from .forms import ColaboradorForm, EPIForm
import csv
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q

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

@require_POST
def gerar_relatorio(request):
    tipo_relatorio = request.POST.get('tipoRelatorio')
    
    if tipo_relatorio == 'epis':
        data = list(EPI.objects.values('nome_epi', 'funcoes', 'descricao', 'tempo_uso_recomendado'))
    elif tipo_relatorio == 'colaboradores':
        data = list(Colaborador.objects.values('nome', 'cpf', 'telefone', 'funcao'))
    elif tipo_relatorio == 'entregas':
        colaborador_id = request.POST.get('colaborador')
        status = request.POST.get('status')
        
        query = Entrega.objects.all()
        if colaborador_id:
            query = query.filter(colaborador_id=colaborador_id)
        if status:
            query = query.filter(status=status)
        
        data = list(query.values(
            'equipamento__nome_epi',
            'colaborador__nome',
            'data_emprestimo',
            'data_prevista_devolucao',
            'status'
        ))
    else:
        data = []

    return JsonResponse(data, safe=False)

def editar_colaboradores(request):
    colaboradores = Colaborador.objects.all()
    return render(request, 'editar_colb.html', {'colaboradores': colaboradores})

def editar_colaborador(request, colaborador_id):
    colaborador = get_object_or_404(Colaborador, id=colaborador_id)
    if request.method == 'POST':
        form = ColaboradorForm(request.POST, instance=colaborador)
        if form.is_valid():
            form.save()
            messages.success(request, 'Colaborador atualizado com sucesso!')
            return redirect('editar_colaboradores')
    else:
        form = ColaboradorForm(instance=colaborador)
    return render(request, 'editar_colaborador.html', {'form': form, 'colaborador': colaborador})

def excluir_colaborador(request, colaborador_id):
    colaborador = get_object_or_404(Colaborador, id=colaborador_id)
    if request.method == 'POST':
        colaborador.delete()
        messages.success(request, 'Colaborador excluído com sucesso!')
        return redirect('editar_colaboradores')
    return render(request, 'confirmar_exclusao.html', {'colaborador': colaborador})

def editar_epis(request):
    epis = EPI.objects.all()
    return render(request, 'editar_epis.html', {'epis': epis})

def editar_epi(request, epi_id):
    epi = get_object_or_404(EPI, id=epi_id)
    if request.method == 'POST':
        form = EPIForm(request.POST, instance=epi)
        if form.is_valid():
            form.save()
            messages.success(request, 'EPI atualizado com sucesso!')
            return redirect('editar_epis')
    else:
        form = EPIForm(instance=epi)
    return render(request, 'editar_epi.html', {'form': form, 'epi': epi})

def excluir_epi(request, epi_id):
    epi = get_object_or_404(EPI, id=epi_id)
    epi.delete()
    messages.success(request, 'EPI excluído com sucesso!')
    return redirect('editar_epis')

def consultar_entrega(request):
    search_performed = False
    entregas = None
    colaboradores = Colaborador.objects.all()
    
    print(f"Número de colaboradores: {colaboradores.count()}")  # Debug print
    
    if 'colaborador' in request.GET and request.GET['colaborador']:
        search_performed = True
        colaborador_id = request.GET['colaborador']
        entregas = Entrega.objects.filter(colaborador_id=colaborador_id)
    
    return render(request, 'consultar_entrega.html', {
        'entregas': entregas,
        'search_performed': search_performed,
        'colaboradores': colaboradores
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

def relatorio_entregas(request):
    colaboradores = Colaborador.objects.all().order_by('nome')
    entregas = None
    filtro_aplicado = False

    if request.method == 'POST':
        colaborador_id = request.POST.get('colaborador')
        status = request.POST.get('status')
        
        query = Entrega.objects.all()
        if colaborador_id:
            query = query.filter(colaborador_id=colaborador_id)
        if status:
            query = query.filter(status=status)
        
        entregas = query.select_related('equipamento', 'colaborador').order_by('-data_emprestimo')
        filtro_aplicado = True

    context = {
        'colaboradores': colaboradores,
        'entregas': entregas,
        'filtro_aplicado': filtro_aplicado
    }
    
    return render(request, 'relatorio_entregas.html', context)