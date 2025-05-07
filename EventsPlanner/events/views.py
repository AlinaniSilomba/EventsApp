from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from.forms import RegistrationForm,EventForm
from django.contrib.auth import login, logout, authenticate
from django.core.mail import send_mail
from .models import EventModel


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
    events_count = EventModel.objects.count() # fetches the count of the events from the data base to be displayed
    event_title = EventModel.objects.all() # Fetches all the events for title extraction on the frontend 
    return render(request, 'events/index.html',{
        'events_count':events_count, 
        'event_title':event_title
    })


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

  
def contact_us(request)->HttpResponseRedirect | HttpResponse :
    ''' A contact us view that routes the user to the contact us page
    Where they can fill in a form to contact us.
    The contact us method uses Django's mail library method sendmail() which takes in:
    1. The Subject 2. the email message 3. the senders mail and 4. recepient mail. 
    to enable email functionality.
    
    params: http request
    
    return : HttpResponseRedirect or HttpResponse to an  HTML template
    
    example would be index.html 
    '''
    reciever_email:str = 'alinanisilomba1@gmail.com'
    if request.method == 'POST':
        user_name:str = request.POST.get('name')
        user_email:str = request.POST.get('email_address')
        user_message = request.POST.get('email_message')
        try:
            send_mail(
    #Subject here
    f'Message from:{user_name}',
    # Here is the message
    f'{user_message}',
    #"from@example.com"
    f'{user_email}',
   # ["to@example.com"] 
   # Todo
   # security? YESSSS!! you dummy! 🤧 Maybe think about
   # putting this in SECERETS as opposed to writing it here in plain text
    [reciever_email],
    fail_silently=False,)     
        except:
            return HttpResponse('Failed to send email') 
    else:
         return render(request, 'events/contact_us.html')
    return render(request, 'events/contact_us.html',{
        'message': user_name
    })

def upcoming_events(request)->HttpResponseRedirect | HttpResponse :
    ''' 
    An upcocming_events view that routes a user to the upcoming_events page
    
    params: http request
    
    returns:HttpResponseRedirect or HttpResponse to an  HTML template
    
    example would be index.html
    '''
    events = EventModel.objects.all()
    return render(request, 'events/upcoming_events.html',{
        'events':events
    })



def past_events(request)->HttpResponseRedirect | HttpResponse :
    ''' An past_events view that routes a user to the past_events page
    
    params: http request
    
    returns:HttpResponseRedirect or HttpResponse to an  HTML template
    
    example would be index.html '''
    return render(request, 'events/past_events.html')



def eventform(request)->HttpResponseRedirect | HttpResponse:
     if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            user_event = form.save(commit=False)
            user_event.author = request.user 
            user_event.save()
            return HttpResponseRedirect(reverse('upcoming_events'))
        
     else:
        form = EventForm()
        
     return render (request, 'events/create_event.html',{
         'form':form
     })
    




    

