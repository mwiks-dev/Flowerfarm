from django.shortcuts import render
from django.shortcuts import redirect, render
from django.utils import timezone
from django import template
from django.utils.safestring import mark_safe

import calendar
from datetime import datetime

from.models import Production, User
from .forms import ProductionForm

# Create your views here.

#Home page
# def index(request):
#     name = "Mwikali"
#     today = timezone.now().date()
#     selected_date = request.GET.get('date', today)

#     try:
#         data = Production.objects.get(production_date=selected_date)
#     except Production.DoesNotExist:
#         data = None

#     if request.method == 'POST':
#         form = ProductionForm(request.POST, instance=data)
#         if form.is_valid():
#             form.save()
#             return redirect('index')
#     else:
#         form = ProductionForm(instance = data)
#     return render(request, 'index.html',{
#         'name':name,
#         'form':form,
#         'selected_date':selected_date})


    
def calendar_view(request, year, month):
    year = int(year)
    month = int(month)
    today = datetime.today()
    cal = calendar.monthcalendar(year, month)
    context = {
        'year': year,
        'month': month,
        'calendar': cal,
        'today': today.day,
    }
    return render(request, 'index.html', context)

#Login Page
def login(request, id):
    user = User.objects.filter(id = id)
    return redirect('/')
