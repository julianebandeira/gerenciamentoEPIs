import os
import django
import pytest
from django.conf import settings

# Configurações do pytest-django
@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass

def pytest_configure():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'siteEPIs.settings')
    django.setup()