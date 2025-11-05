"""
URL configuration for adminpanel project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('clients/', views.clients_list, name='clients_list'),
    path('products/', views.products_list, name='products_list'),
    path("products/edit-product/<int:product_id>/", views.edit_product, name="edit_product"),
    path("products/delete-product/<int:product_id>/", views.delete_product, name="delete_product"),
    path("order/change-status/<int:order_id>/", views.change_status, name="change_status"),
    path("order/change_composition/<int:order_id>/", views.change_composition, name="change_composition"),
    path('order/<int:order_id>/change-price/<int:item_id>/', views.change_price, name='change_price'),
    path('orders/', views.orders_list, name='orders_list'),
    path('compositions-list/<int:composition_id>/products_availability', views.products_availability, name='products_availability'),
    path('compositions-list/', views.compositions_list, name='composition_list'),
    path("order/<int:order_id>/add_item/", views.add_item, name="add_item"),
    path('client_orders/<int:client_id>/', views.client_orders, name='client_orders'),
    path("delete/<int:client_id>/", views.delete_client_view, name="delete_client"),
    path("delete-item/<int:item_id>/", views.delete_item, name="delete_item"),
    path("order/<int:order_id>/add_item/", views.add_item, name="add_item"),
    path("order/create/<int:client_id>", views.create_order, name="create_order"),
    path("order/<int:order_id>/change-item-imei/<int:item_id>", views.change_item_imei, name="change_item_imei"),
    path("order/change-item-status/<int:item_id>", views.change_item_status, name="change_item_status"),
    path("edit/<int:client_id>/", views.edit_client_view, name="edit_client"),
    path("order/<int:order_id>/", views.order_details, name="order"),
    path('products-autocomplete/', views.products_autocomplete, name='products_autocomplete'),
    path('compositions_autocomplete/', views.compositions_autocomplete, name='compositions_autocomplete'),
    path("transportations/", views.transportations, name="transportations"),
    path("transportations/<int:transportation_id>", views.transportation, name="transportation"),
    path("transportations/create_transportation/", views.create_transportation, name="create_transportation"),
    path("transportations/<int:transportation_id>/add-item/", views.add_transportation_item , name="add_transportation_item"),
    path("transportations/<int:transportation_id>/delete-item/<int:item_id>/", views.delete_transportation_item , name="delete_transportation_item"),
    path("transportations/<int:transportation_id>/change-composition/", views.change_transportation_composition , name="change_transportation_composition"),
    path('availability-autocomplete/', views.availability_autocomplete, name='availability_autocomplete'),
    path('to_order/', views.to_order, name='to_order'),
    path('supplies/', views.supplies, name='supplies'),
    path('supplies/supply/<int:supply_id>', views.supply, name='supply'),
    path('supplies/create-supply/<int:item_id>', views.create_supply, name='create_supply'),
    
    
    
    
    
    
     
    
]
