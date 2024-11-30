import pytest
from django.urls import reverse
from epis.models import EPI
from django.test import Client

@pytest.mark.django_db
class TestEPIs:
    @pytest.fixture
    def client(self):
        return Client()
    
    @pytest.fixture
    def valid_epi_data(self):
        return {
            'nomeEPI': 'Capacete de Segurança',
            'funcoes': 'Operador de Máquinas, Construção Civil',
            'descricao': 'Capacete de segurança com carneira ajustável',
            'tempoUso': '180'
        }
    
    @pytest.fixture
    def invalid_epi_data(self):
        return {
            'nomeEPI': '',  # Nome vazio (inválido)
            'funcoes': 'Operador de Máquinas',
            'descricao': 'Descrição do EPI',
            'tempoUso': 'abc'  # Valor não numérico (inválido)
        }

    def test_epi_url(self, client):
        """Testa se a URL de EPIs está acessível"""
        url = reverse('epis')
        response = client.get(url)
        assert response.status_code == 200
    
    @pytest.mark.cadastro
    def test_cadastro_epi_valido(self, client, valid_epi_data):
        """Testa o cadastro de um EPI com dados válidos"""
        url = reverse('epis')
        response = client.post(url, valid_epi_data)
        
        # Verifica se o redirecionamento foi bem-sucedido
        assert response.status_code == 302
        
        # Verifica se o EPI foi criado no banco de dados
        epi = EPI.objects.filter(nome_epi=valid_epi_data['nomeEPI']).first()
        assert epi is not None
        assert epi.funcoes == valid_epi_data['funcoes']
        assert epi.descricao == valid_epi_data['descricao']
        assert epi.tempo_uso_recomendado == int(valid_epi_data['tempoUso'])
    
    @pytest.mark.cadastro
    def test_cadastro_epi_invalido(self, client, invalid_epi_data):
        """Testa o cadastro de um EPI com dados inválidos"""
        url = reverse('epis')
        initial_count = EPI.objects.count()
        
        try:
            response = client.post(url, invalid_epi_data)
        except ValueError:
            pass  # Esperamos um erro ao tentar converter 'abc' para inteiro
        
        # Verifica se nenhum novo EPI foi criado
        assert EPI.objects.count() == initial_count