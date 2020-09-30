import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from django.contrib.auth import authenticate
from django.contrib.auth import logout, login
from django.views.generic import View
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .forms import RegisterForm


class MyLogin(auth_views.LoginView):
    def get(self, request ):
        userlogin = request.user
        context = {
            'user_login': userlogin,
            'form': AuthenticationForm(),
        }
        return render(request, template_name='log_in.html', context=context )

    def post(self, request, next=''):
        user = request.POST.get('username')
        psw = request.POST.get('password')
        # self.cleaned_data.get('username')
        user = authenticate(request, username=user, password=psw)
        if user:
            login(request, user)
            print('login success: ', user)
            return redirect('index_page' )
        else:
            print(' invalid username or password ')
            form = AuthenticationForm(data=request.POST)
            context = {
                #'errors': 'error',
                'form' : form
            }
            return render(request, template_name='log_in.html', context = context)


class MyChangePassword(auth_views.PasswordChangeView):
    def get(self, request):
        user=request.user
        form = PasswordChangeForm(user=user)
        context = {'form':form, 'user_name':user}
        return render(request, template_name='password_change.html', context=context)

    def post(self, request):
        user = request.user
        print ('changing password for user : ', user)
        form = PasswordChangeForm(user=user, data=request.POST)
        if form.is_valid():
            form.save()
            # return render(request, template_name='password_change_ok.html', context=context)
            return HttpResponse(json.dumps({'result': True}))
        print('smth wrong, ')
        errors = list(form.errors.values())[0]
        return HttpResponse(json.dumps({'result': False, 'errors': errors}))
        # return render(request, template_name='password_change.html', context={'form' : form})


def logout_view(request):
    logout(request)
    return redirect('index_page')


class RegisterUser(View):
    def get(self, request):
        form = RegisterForm()
        return render(request , 'register.html', context = {'form':form})

    def post(self, request):
        form = RegisterForm(request.POST or None)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index_page')
        else:
            return render(request , 'register.html', context = {'form':form})

def registration(request, link):
    # get the link from url /users/registration/<linkhash>
    #  if link not exist: render error page
    # if link exist - get the user and load the form for create the new paswd
    pass