from django.db import models

class EstadoEntidades(models.IntegerChoices):
    ACTIVO = 1, "Activo"
    INACTIVO = 9, "Inactivo"


