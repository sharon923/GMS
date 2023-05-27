from django.shortcuts import render, redirect
from django.http import HttpResponse
from ..models import packages, history, user_member, delivery_status
from .forms import UserProfileForm, ScheduleForm
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.models import User
from django.views import View
from django.contrib import messages
from datetime import datetime

class UserProfile(View):
    form_class = UserProfileForm

    def get_user_details(self, request):
        active_user = User.objects.get(id=request.user.id)
        try:
            active_member = user_member.objects.filter(member = active_user)[0]
            return {
                'addr': active_member.addr, 
                'place': active_member.place, 
                'pincode': active_member.pin_code, 
                'phone': active_member.phone,
                'pack': active_member.pack.pack_name
            }
        except:
            pass
        return {
                
            }
        
    def update_db(self, request):
        addr = request.POST.get('addr')
        place = request.POST.get('place')
        pin_code = request.POST.get('pin_code')
        phone = request.POST.get('phone')
        pack = request.POST.get('pack')
        pack_db = packages.objects.filter(pack_name = pack)[0]

        active_user = User.objects.get(id=request.user.id)
        try:
            active_member = user_member.objects.filter(member = active_user)[0]

            active_member.addr = addr  
            active_member.place = place  
            active_member.pin_code = pin_code 
            active_member.phone = phone  
            active_member.pack = pack_db
            active_member.save()
        except:
            active_member = user_member(member = active_user, addr = addr, place = place, pin_code = pin_code, phone = phone, pack = pack_db)
            active_member.save()


    def get(self, request, *args, **kwargs):
        user_details = self.get_user_details(request)
        return render(request, './myapp/user_profile.html',{'form':self.form_class(user_obj=user_details)})
    
    def post(self, request, *args, **kwargs):
        self.update_db(request)
        user_details = self.get_user_details(request)
        return render(request, './myapp/user_profile.html',{'form':self.form_class(user_obj=user_details)})


class UserHome(View):
    form_class = ScheduleForm


    def get_user_history(self, request):
        user_history = []
        try:
            active_user = User.objects.get(id=request.user.id)
            active_member = user_member.objects.filter(member = active_user)[0]
        
            for each_history in history.objects.filter(user_details = active_member):
               user_history.append({
                "addr": each_history.user_details.addr,
                "status": each_history.choice.ui_text,
                "time": each_history.day_picked
               })
        except: 
            pass
        # print(user_history)
        return user_history
    
    def can_user_schedule(self, request):
        active_user = User.objects.get(id=request.user.id)
        try:
            active_member = user_member.objects.filter(member = active_user)[0]
            all_history = history.objects.filter(user_details = active_member)
            number_of_pickups = 0
            for each_history in all_history:
                if (each_history.day_picked.month == datetime.now().month):
                    number_of_pickups = number_of_pickups + 1
            
            if active_member.pack.pack_name == 'NO_PLAN':
                return { 'state': False, 'error': 'Please select a subscription plan by giving your details in user profile' }
            elif number_of_pickups >= int(active_member.pack.day_pickup):
                return { 'state': False, 'error': 'Number of pickups exceeded for this month. Consider upgrading the plan' } 
            else:
                return { 'state': True, 'error': '' }
        except: 
            pass

        return { 'state': False, 'error': 'Please fill your profile details', }



    def get(self, request, *args, **kwargs):
        user_history = self.get_user_history(request)
        return render(request, './myapp/user_home.html',{'form':self.form_class(), 'details': user_history, 'can_user_schedule': self.can_user_schedule(request)})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            
            pick_date = form.cleaned_data['pick_date']
            pick_time  = form.cleaned_data['pick_time']
            date_time = pick_date.strftime("%Y-%m-%d") + " " + pick_time.strftime("%H:%M:%S")
            active_user = User.objects.get(id=request.user.id)
            active_member = user_member.objects.filter(member = active_user)[0]
            default_status = delivery_status.objects.filter(status = "scheduled")[0]
            history_data = history(user_details = active_member, choice = default_status, day_picked = date_time)
            history_data.save()
            user_history = self.get_user_history(request)
            return render(request, './myapp/user_home.html',{'form':self.form_class(), 'details': user_history, 'can_user_schedule': self.can_user_schedule(request)})
        else:
            
            messages.error(request, "Enter a valid date and time")
            user_history = self.get_user_history(request)
            return render(request, './myapp/user_home.html',{'form':self.form_class(),  'details': user_history, 'can_user_schedule': self.can_user_schedule(request)})
            