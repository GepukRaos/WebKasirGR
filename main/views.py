from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from .forms import MerchantRegisterForm
from .models import Merchant


def landing_page(request):
    return render(request, 'landingPage.html')

def order_page(request):
    return render(request, 'orderpage.html')

def antrian_page(request):
    return render(request, 'antrian.html')


def register_user(request):
    if request.method == "POST":
        form = MerchantRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Buat Merchant terkait user
            store = form.cleaned_data.get("store_name")
            Merchant.objects.create(user=user, store_name=store)

            messages.success(request, "Akun berhasil dibuat! Silakan login.")
            return redirect("login")
    else:
        form = MerchantRegisterForm()

    return render(request, "register.html", {"form": form})


def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("landing")
        else:
            messages.error(request, "Username atau password salah.")
    else:
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form})


def logout_user(request):
    logout(request)
    return redirect("landing")
