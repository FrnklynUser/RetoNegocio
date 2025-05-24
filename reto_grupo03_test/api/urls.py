from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'promociones', views.PromocionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('check-promotions/', views.check_promotions, name='check-promotions'),
] 