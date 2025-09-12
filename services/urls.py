from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('', views.service_list, name='list'),
    path('packages/', views.package_list, name='package_list'),
    path('packages/<slug:slug>/', views.package_detail, name='package_detail'),
    path('<slug:slug>/', views.service_detail, name='detail'),
]
