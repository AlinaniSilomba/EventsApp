from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from.forms import RegistrationForm
from django.contrib.auth import login, logout, authenticate


# Create your views here.
def index(request) ->HttpResponseRedirect | HttpResponse :
    '''
    This is our home page function, We first check if the user is authenticated, if not they are redirected to the login page
    otherwise if they are authenticated we allow them to stay on the homepage of index.html
    
    params:http request
    
    return: HttpResponseRedirect or HttpResponse to an  HTML template
    
    example would be index.html
    '''
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    return render(request, 'events/index.html')


def sign_up(request) ->HttpResponseRedirect | HttpResponse :
    '''
    Signing up a new user: by first importing the Registration form from forms.py then passing in the request which is a post 
    if the form is valid we save the form and login the user using the login() fucntion which takes the request and the user form
    however if the the credentials entered on the sign up form are invalid we display an empty form to them again to fill it out.
    
    params: http request
    
    returns:HttpResponseRedirect or HttpResponse to an  HTML template
    
    example would be index.html
    '''
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return HttpResponseRedirect(reverse('index'))
    else:
        form = RegistrationForm()
    return render(request,'events/sign_up.html',{
        'form':form
    })
       
def log_out(request)->HttpResponseRedirect | HttpResponse :
    '''
    A logout view that routes a user to the logout page
    
    params: http request
    
    returns:HttpResponseRedirect or HttpResponse to an  HTML template
    
    example would be index.html
    '''
    return render(request, 'events/logout.html')


def contact_us(request):
    ''' Write Documentation '''
    return render(request, 'events/contact_us.html')



def upcoming_events(request):
    ''' Write Documentation '''
    return render(request, 'events/upcoming_events.html')



def past_events(request):
    ''' Write Documentation '''
    return render(request, 'events/past_events.html')
    




    

