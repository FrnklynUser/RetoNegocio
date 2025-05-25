from django.urls import path
from .views import CalcularBonificacionesView

app_name = 'promociones'

urlpatterns = [
    path('calcular-bonificaciones/', CalcularBonificacionesView.as_view(), name='calcular_bonificaciones'),
] 