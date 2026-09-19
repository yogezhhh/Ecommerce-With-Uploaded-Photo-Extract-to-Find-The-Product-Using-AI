from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product-list'),
    path('products/<slug:slug>/', views.product_detail, name='product-detail'),
    path('lens/', views.lens, name='lens'),

    path('cart/', views.cart_detail, name='cart'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart-add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart-remove'),
    path('cart/update/<int:product_id>/', views.cart_update, name='cart-update'),

    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.orders, name='orders'),
    path('orders/<int:pk>/success/', views.order_success, name='order-success'),

    path('login/', auth_views.LoginView.as_view(template_name='shop/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
]