from django.db import models

class Empresa(models.Model):
    nombre = models.CharField(max_length=255)

    class Meta:
        db_table = 'empresa'
