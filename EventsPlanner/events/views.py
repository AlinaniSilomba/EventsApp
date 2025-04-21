from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from.forms import RegistrationForm

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    return render(request, 'events/index.html')


def sign_up(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
    else:
        form = RegistrationForm()
    return render(request,'events/sign_up.html',{
        'form':form
    })