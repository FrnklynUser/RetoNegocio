from rest_framework import serializers
from api.models.canal_cliente import CanalCliente

class CanalClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CanalCliente
        fields = ['id', 'nombre']