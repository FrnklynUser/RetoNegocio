from django.shortcuts import render
from promociones.models import PromocionCombinada

def evaluar_promocion(request):
    resultado = None

    if request.method == "POST":
        producto = request.POST.get("producto")
        monto = float(request.POST.get("monto", 0))

        # Buscar la promoción activa del producto
        promo = PromocionCombinada.objects.filter(producto_principal=producto, activa=True).first()
        if promo:
            resultado = promo.aplicar_promocion(producto, monto)
        else:
            resultado = {"error": "No se encontró una promoción activa para ese producto."}

    return render(request, "promociones/evaluar_promocion.html", {"resultado": resultado})
