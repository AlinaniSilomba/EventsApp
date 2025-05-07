from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'), 
    path('events/', views.index, name='index'), 
    path('accounts/sign-up/', views.sign_up, name='sign_up'),
    path('accounts/logout/', views.log_out, name='logout'), 
    path('contacts-us/', views.contact_us, name='contact_us'),  
    path('upcoming-events/', views.upcoming_events, name='upcoming_events'), 
    path('past-events/', views.past_events, name='past_events'),
    path('create-event/', views.eventform, name='create_event'),
]
