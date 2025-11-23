from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from main.models import Merchant
from .models import Menu

@login_required
def menu_list(request):
    merchant = Merchant.objects.get(user=request.user)
    menus = Menu.objects.filter(merchant=merchant)
    return render(request, "menu/menu_list.html", {"menus": menus})

@login_required
def menu_add(request):
    merchant = Merchant.objects.get(user=request.user)

    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")

        Menu.objects.create(
            merchant=merchant,
            name=name,
            price=price
        )
        return redirect("menu_list")

    return render(request, "menu/menu_add.html")

@login_required
def menu_edit(request, id):
    merchant = Merchant.objects.get(user=request.user)
    menu_item = get_object_or_404(Menu, id=id, merchant=merchant)

    if request.method == "POST":
        menu_item.name = request.POST.get("name")
        menu_item.price = request.POST.get("price")
        menu_item.save()
        return redirect("menu_list")

    return render(request, "menu/menu_edit.html", {"menu": menu_item})

@login_required
def menu_delete(request, id):
    merchant = Merchant.objects.get(user=request.user)
    menu_item = get_object_or_404(Menu, id=id, merchant=merchant)
    menu_item.delete()
    return redirect("menu_list")
