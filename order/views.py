from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from main.models import Merchant
from menu.models import Menu
from .models import Order, OrderItem


@login_required
def order_page(request):
    merchant = Merchant.objects.get(user=request.user)
    menus = Menu.objects.filter(merchant=merchant)

    # BUG FIX #2 → Jika tidak ada menu sama sekali
    if menus.count() == 0:
        messages.error(request, "Tidak dapat membuat pesanan karena menu belum tersedia.")
        return render(request, "orderpage.html", {"menus": menus})

    if request.method == "POST":
        customer_name = request.POST.get("customer_name")
        order_type = request.POST.get("order_type")

        # BUG FIX #1 → Hitung jumlah total item yang dipilih
        total_items = 0
        for menu in menus:
            qty = int(request.POST.get(f"qty_{menu.id}", 0))
            if qty > 0:
                total_items += qty

        # Jika tidak ada item dipilih → JANGAN buat order
        if total_items == 0:
            messages.error(request, "Gagal membuat pesanan. Anda harus memilih minimal 1 menu.")
            return render(request, "orderpage.html", {"menus": menus})

        # Jika ada item → buat order
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

        messages.success(request, "Pesanan berhasil dibuat.")
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
