from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from main.models import Merchant
from menu.models import Menu
from .models import Order, OrderItem

@login_required
def order_page(request):
    merchant = Merchant.objects.get(user=request.user)
    menus = Menu.objects.filter(merchant=merchant)

    if request.method == "POST":
        customer_name = request.POST.get("customer_name")
        order_type = request.POST.get("order_type")

        order = Order.objects.create(
            merchant=merchant,
            customer_name=customer_name,
            order_type=order_type
        )

        for menu in menus:
            qty = int(request.POST.get(f"qty_{menu.id}", 0))
            note = request.POST.get(f"note_{menu.id}", "")
            if qty > 0:
                OrderItem.objects.create(
                    order=order,
                    menu=menu,
                    quantity=qty,
                    note=note
                )

        return redirect("antrian")

    return render(request, "orderpage.html", {"menus": menus})


@login_required
def antrian_page(request):
    merchant = Merchant.objects.get(user=request.user)

    orders_created = Order.objects.filter(
        merchant=merchant,
        is_done=False
    ).order_by("created_at")

    orders_completed = Order.objects.filter(
        merchant=merchant,
        is_done=True
    ).order_by("-created_at")

    context = {
        "orders_created": orders_created,
        "orders_completed": orders_completed,
    }

    return render(request, "antrian.html", context)

@login_required
def order_done(request, order_id):
    order = Order.objects.get(id=order_id)
    order.is_done = True
    order.save()
    return redirect("antrian")

