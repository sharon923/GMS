from django.shortcuts import render, redirect
from .forms import LoginForm, SignupForm
from django.contrib.auth import authenticate,login, logout
from django.contrib import sessions
from django.contrib.auth.models import User
from django.views import View
from django.contrib import messages

class LoginView(View):
    form_class = LoginForm
    template_name = './myapp/login.html'

    def invalid_user(self, request , uname):
        messages.error(request, "Invalid username or password")
        form = self.form_class()
        form.default_user_name(uname)
        return render(request, self.template_name, {'form': form})
    
    def get(self, request, *args, **kwargs):
       
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        
        form = self.form_class(request.POST)
        if form.is_valid():
            uname = form.cleaned_data['uname']
            password  = form.cleaned_data['password']
            user = authenticate(username=uname, password=password)
            if user is not None:
                login(request, user)
                return self.user_type_routing(user)
            else:
                return self.invalid_user(request, uname)
        else:
            return self.invalid_user(request, uname)
    
    def user_type_routing(self, user):
        if user.is_superuser:
            return redirect('/admin')
        elif user.is_superuser == False and user.is_staff == True:
            return redirect('/emp_home')
        else:    
            return redirect('/home')
        
class SignupView(View):
    form_class = SignupForm
    template_name = './myapp/signup.html'

    def post(self,  request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password  = form.cleaned_data['password']
            fname = form.cleaned_data['fname']
            lname = form.cleaned_data['lname']
            form = LoginForm()
            user = User.objects.create_user(email, email = email, password = password, first_name = fname, last_name = lname)
            return render(request, './myapp/login.html', {'form': form})
        else:
            return render(request, './myapp/signup.html', {'form': form})
    
    def get(self,  request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
