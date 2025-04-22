from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'), 
    path('index', views.index, name='index'), 
    path('accounts/sign-up/', views.sign_up, name='sign_up'), 
     path('accounts/logout/', views.log_out, name='logout'), 
]
