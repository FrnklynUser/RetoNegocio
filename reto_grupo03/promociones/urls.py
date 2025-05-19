from django.urls import path
from . import views

urlpatterns = [

    path('evaluar/', views.evaluar_promocion, name='evaluar_promocion'),
]
