from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.models import User
from django.views import View
from django.contrib import messages
from ..models import picker_schedule, user_member, delivery_status, history
from .forms import PickupUpdateForm

class EmployHome(View):
    pickup_form = PickupUpdateForm

    def get(self, request, *args, **kwargs):
        active_user = User.objects.get(id=request.user.id)
        all_schedules = []
        for each_schedule in picker_schedule.objects.filter(emp_name = active_user):
            all_schedules.append({
                'addr': each_schedule.pick_place.user_details.addr,
                'time': each_schedule.pick_place.day_picked,
                'form':  self.pickup_form(history_id=history.objects.filter(id = each_schedule.pick_place.id)[0])
            })
        return render(request, './myapp/emp_home.html', {'details': all_schedules})
    
    def post(self, request, *args, **kwargs):
        active_user = User.objects.get(id=request.user.id)
        selected_details = request.POST.get('status').split('##$$&&')
        history_id = int(selected_details[0])
        selected_option = selected_details[1]

        update_history = history.objects.filter(id = history_id)[0]
        update_history.choice = delivery_status.objects.filter(status = selected_option)[0]
        update_history.save()

        all_schedules = []
        for each_schedule in picker_schedule.objects.filter(emp_name = active_user):
            all_schedules.append({
                'addr': each_schedule.pick_place.user_details.addr,
                'time': each_schedule.pick_place.day_picked,
                'form':  self.pickup_form(history_id = history.objects.filter(id = each_schedule.pick_place.id)[0])
            })
        
        return render(request, './myapp/emp_home.html', {'details': all_schedules})
