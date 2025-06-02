from rest_framework import serializers
from api.models.empresa import Empresa
 
class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = ['id', 'nombre'] 