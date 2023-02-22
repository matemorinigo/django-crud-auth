from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse

# Create your views here.

def home(request):

    return render(request,'index.html')

def signUp(request):

    if request.method == "GET":
        data_to_html = {
            'form': UserCreationForm(),
        }

        return render(request, 'sign-up.html', data_to_html)

    else:
        if request.POST['password1']==request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                return HttpResponse("USUARIO CREADO")

            except:
                return HttpResponse("USUARIO YA EXISTE")

        return render(request, 'layouts/base.html')
