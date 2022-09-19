from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('login_page', views.login_page, name='login_page'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('home_page', views.engineers_page, name='home_page'),
    path('add_product', views.add_product, name='add_product'),
    path('product_list', views.product_list, name='product_list'),
    path('add_items/', views.add_items, name='add_items'),
    path('user_list', views.user_list, name='user_list'),
    path('page_register', views.page_register, name="page_register"),
    path('sign_out', views.sign_out, name="sign_out"),
    path('home_order', views.home_order, name="home_order"),
    path('home_approvals', views.home_approvals, name="home_approvals"),
    path('order_list', views.order_list, name="order_list"),
    path('add_order', views.add_order, name="add_order"),
    path('approve_order/<str:order_id>/', views.approve_order, name='approve_order'),
    path('reject_order/<str:order_id>/', views.reject_order, name='reject_order')
]