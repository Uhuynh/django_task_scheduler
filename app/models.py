from faker import Faker

from django.db import models


class CompanyName(models.Model):
    create_dt = models.DateTimeField(auto_now_add=True, verbose_name='Created')
    name = models.CharField(max_length=255, null=False, blank=False)

    def generate_obj_list(self, count: int):
        obj_list = []
        fake = Faker()
        Faker.seed(0)
        for _ in range(count):
            obj_list.append(self.__class__(**{'name': fake.company()}))
        return obj_list
