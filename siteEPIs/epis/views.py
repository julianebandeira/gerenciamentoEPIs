from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request,'index.html')

def colaboradores(request):
    return render(request,'colaboradores.html')

def epis(request):
    return render(request, 'epis.html')

def avisos(request):
    return render(request, 'avisos.html')

def entrega(request):
    return render(request, 'entrega.html')