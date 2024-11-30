from django.test import TestCase, Client
from django.urls import reverse
from .models import Colaborador, EPI, Entrega
from datetime import date

class TesteDeViews(TestCase):
    def setUp(self):
        # Inicializa o cliente de teste
        self.client = Client()

        # Cria objetos para os testes
        self.colaborador = Colaborador.objects.create(
            nome="João Silva",
            cpf="123.456.789-00",
            telefone="(11) 98765-4321",
            funcao="Operador"
        )

        self.epi = EPI.objects.create(
            nome_epi="Capacete de Segurança",
            funcoes="Proteção da cabeça",
            descricao="Capacete resistente a impactos.",
            tempo_uso_recomendado=30
        )

        self.entrega = Entrega.objects.create(
            equipamento=self.epi,
            colaborador=self.colaborador,
            data_emprestimo=date(2024, 1, 1),
            data_prevista_devolucao=date(2024, 2, 1),
            condicoes_equipamento="Novo",
            status="Em uso"
        )

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_colaboradores_post(self):
        response = self.client.post(reverse('colaboradores'), {
            'nome': 'Maria Souza',
            'cpf': '987.654.321-00',
            'telefone': '(21) 12345-6789',
            'funcao': 'Auxiliar'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Colaborador.objects.count(), 2)
        self.assertTrue(Colaborador.objects.filter(nome='Maria Souza').exists())

    def test_epis_post(self):
        response = self.client.post(reverse('epis'), {
            'nomeEPI': 'Luva de Proteção',
            'funcoes': 'Proteção das mãos',
            'descricao': 'Luva resistente a cortes.',
            'tempoUso': 15
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(EPI.objects.count(), 2)
        self.assertTrue(EPI.objects.filter(nome_epi='Luva de Proteção').exists())

    def test_entrega_post(self):
        response = self.client.post(reverse('entrega'), {
            'equipamento': self.epi.id,
            'colaborador': self.colaborador.id,
            'dataEmprestimo': '2024-01-15',
            'dataPrevistaDevolucao': '2024-02-15',
            'condicoesEquipamento': 'Bom',
            'status': 'Em uso'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Entrega.objects.count(), 2)

    def test_gerar_relatorio(self):
        response = self.client.post(reverse('gerar_relatorio'), {
            'tipoRelatorio': 'colaboradores'
        })
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            [{'nome': 'João Silva', 'cpf': '123.456.789-00', 'telefone': '(11) 98765-4321', 'funcao': 'Operador'}]
        )

class TesteDeModels(TestCase):
    def setUp(self):
        # Criando instâncias de Colaborador e EPI para os testes
        self.colaborador = Colaborador.objects.create(
            nome="João Silva",
            cpf="123.456.789-00",
            telefone="(11) 98765-4321",
            funcao="Operador"
        )
        
        self.epi = EPI.objects.create(
            nome_epi="Capacete de Segurança",
            funcoes="Proteção da cabeça",
            descricao="Capacete resistente a impactos.",
            tempo_uso_recomendado=30
        )

    def test_create_colaborador(self):
        colaborador = Colaborador.objects.create(
            nome="Maria Souza",
            cpf="987.654.321-00",
            telefone="(21) 12345-6789",
            funcao="Auxiliar"
        )
        self.assertEqual(colaborador.nome, "Maria Souza")
        self.assertEqual(Colaborador.objects.count(), 2)

    def test_cpf_unique_constraint(self):
        with self.assertRaises(Exception):  # Garantindo que o CPF seja único
            Colaborador.objects.create(
                nome="Duplicate CPF",
                cpf="123.456.789-00",
                telefone="(11) 91234-5678",
                funcao="Supervisor"
            )

    def test_create_epi(self):
        epi = EPI.objects.create(
            nome_epi="Luva de Proteção",
            funcoes="Proteção das mãos",
            descricao="Luva resistente a cortes.",
            tempo_uso_recomendado=15
        )
        self.assertEqual(epi.nome_epi, "Luva de Proteção")
        self.assertEqual(EPI.objects.count(), 2)

    def test_create_entrega(self):
        entrega = Entrega.objects.create(
            equipamento=self.epi,
            colaborador=self.colaborador,
            data_emprestimo=date(2024, 1, 1),
            data_prevista_devolucao=date(2024, 2, 1),
            condicoes_equipamento="Bom",
            status="Em uso"
        )
        self.assertEqual(entrega.equipamento, self.epi)
        self.assertEqual(entrega.colaborador, self.colaborador)
        self.assertEqual(Entrega.objects.count(), 1)

    def test_entrega_string_representation(self):
        entrega = Entrega.objects.create(
            equipamento=self.epi,
            colaborador=self.colaborador,
            data_emprestimo=date(2024, 1, 1),
            data_prevista_devolucao=date(2024, 2, 1),
            condicoes_equipamento="Bom",
            status="Em uso"
        )
        self.assertEqual(str(entrega), f"{self.epi} - {self.colaborador} - Em uso")

    def test_null_optional_fields_entrega(self):
        entrega = Entrega.objects.create(
            equipamento=self.epi,
            colaborador=self.colaborador,
            data_emprestimo=date(2024, 1, 1),
            data_prevista_devolucao=date(2024, 2, 1),
            condicoes_equipamento="Bom",
            status="Em uso",
            data_devolucao=None,
            observacao=None
        )
        self.assertIsNone(entrega.data_devolucao)
        self.assertIsNone(entrega.observacao)

    def test_related_data(self):
        Entrega.objects.create(
            equipamento=self.epi,
            colaborador=self.colaborador,
            data_emprestimo=date(2024, 1, 1),
            data_prevista_devolucao=date(2024, 2, 1),
            condicoes_equipamento="Bom",
            status="Concluído"
        )
        self.assertEqual(self.colaborador.entrega_set.count(), 1)
        self.assertEqual(self.epi.entrega_set.count(), 1)