from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('boss/', views.dashboard, name='dashboard'),
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('suppliers/add/', views.supplier_add, name='supplier_add'),
    path('suppliers/edit/<int:pk>/', views.supplier_edit, name='supplier_edit'),
    path('suppliers/delete/<int:pk>/', views.supplier_delete, name='supplier_delete'),

    # Buyer URLs
    path('buyers/', views.buyer_list, name='buyer_list'),
    path('buyer/add/', views.buyer_create, name='buyer_create'),
    path('buyer/edit/<int:pk>/', views.buyer_update, name='buyer_update'),
    path('buyer/delete/<int:pk>/', views.buyer_delete, name='buyer_delete'),

    # Product URLs
    path('products/', views.product_list, name='product_list'),
    path('product/add/', views.product_create, name='product_create'),
    path('product/edit/<int:pk>/', views.product_update, name='product_update'),
    path('product/delete/<int:pk>/', views.product_delete, name='product_delete'),

    # Order URLs
    path('orders/', views.order_list, name='order_list'),
    path('order/add/', views.order_create, name='order_create'),
    path('order/edit/<int:pk>/', views.order_update, name='order_update'),
    path('order/delete/<int:pk>/', views.order_delete, name='order_delete'),


    path('seller/register/', views.seller_register, name='seller_register'),
    path('buyer/register/', views.buyer_register, name='buyer_register'),
    path('seller/login/', views.seller_login, name='seller_login'),
    path('buyer/login/', views.buyer_login, name='buyer_login'),
    path('pending-users/', views.pending_users, name='pending_users'),
    path('approve/<str:user_type>/<int:user_id>/', views.approve_user, name='approve_user'),




    path('dashboard/buyer/', views.buyer_dashboard, name='buyer_dashboard'),
    path('dashboard/seller/', views.seller_dashboard, name='seller_dashboard'),


    path('dashboard/seller/product/add/', views.add_product, name='add_product'),
    path('dashboard/seller/product/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('dashboard/seller/product/delete/<int:product_id>/', views.delete_product, name='delete_product'),


    path('dashboard/buyer/add-order/', views.add_order, name='add_order'),
    path('dashboard/buyer/cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),



    path('delete-user/<str:user_type>/<int:user_id>/', views.delete_user, name='delete_user'),




]

