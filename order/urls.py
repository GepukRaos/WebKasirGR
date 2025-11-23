from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_page, name='order_page'),
    path('antrian/', views.antrian_page, name='antrian'),
    path("done/<int:order_id>/", views.order_done, name="order_done"),
]
