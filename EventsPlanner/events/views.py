from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from.forms import RegistrationForm
from django.contrib.auth import login, logout, authenticate
# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    return render(request, 'events/index.html')


def sign_up(request):
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
    

