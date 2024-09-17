from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

from django.views.generic import *

urlpatterns = [
    #path("home", views.home, name="home"),
    path("home", views.HomeView.as_view(),name='home'),
    path("contact", views.ContactView,name="contact"),
    path("email-sent", views.MailSendView.as_view(),name='email-sent'),
    path("about", views.AboutView.as_view(),name="about"),
    path("home/<param>",views.IndexView.as_view()),

    path("product/list",views.ProductListView.as_view(),name="product-list"),
    path("item/list",views.ProductItemListView.as_view() ,name='item-list'),
    path("attributes/list",views.ProductAttributeListView.as_view() ,name='attribute-list'),

    path("product/<pk>",views.ProductDetailView.as_view(), name="product-detail"),
    path("item/<pk>",views.ProductItemDetailView.as_view(), name="item-detail"),
    path("attribute/<pk>",views.ProductAttributeDetailView.as_view() ,name='attribute-detail'),
    
    path('login/', views.ConnectView.as_view(), name='login'),
    path('logout/', views.DisconnectView.as_view(), name='logout'),
    path("register/", views.RegisterView.as_view(), name="register"),
    
    path("product/add/",views.ProductCreateView.as_view(), name="product-add"),
    path("attribute/add/",views.ProductAttributeCreateView.as_view(), name="attribute-add"),
    path("item/add/",views.ProductItemCreateView.as_view(), name="item-add"),

    path("product/<pk>/update/",views.ProductUpdateView.as_view(), name="product-update"),
    path("attribute/<pk>/update/",views.ProductAttributeUpdateView.as_view(), name="attribute-update"),
    path("item/<pk>/update/",views.ProductItemUpdateView.as_view(), name="item-update"),

    path("product/<pk>/delete/",views.ProductDeleteView.as_view(), name="product-delete"),
    path("attribute/<pk>/delete/",views.ProductAttributeDeleteView.as_view(), name="attribute-delete"),
    path("item/<pk>/delete/",views.ProductItemDeleteView.as_view(), name="item-delete"),
]

