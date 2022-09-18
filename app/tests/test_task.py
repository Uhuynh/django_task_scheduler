import pytest

from app.tasks import company_name_bulk_create


@pytest.mark.django_db
def test_task():
    assert 1 == company_name_bulk_create(1)
