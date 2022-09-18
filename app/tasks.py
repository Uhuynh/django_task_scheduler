from project.celery import app


@app.task()
def company_name_bulk_create(count: int):
    from app.models import CompanyName
    obj_list = CompanyName().generate_obj_list(count)
    CompanyName.objects.bulk_create(obj_list)
