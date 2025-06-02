from rest_framework import serializers
from api.models.sucursal import Sucursal
 
class SucursalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sucursal
        fields = ['id', 'empresa', 'nombre'] 