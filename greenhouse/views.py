from django.shortcuts import render
from django.shortcuts import redirect, render
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


    
def calendar_view(request):
    current_user = request.user
    username = current_user.username

    today = datetime.today()
    year = today.year
    month = today.month
    cal = calendar.monthcalendar(year, month)

    context = {
        'username':username,
        'year': year,
        'month': month,
        'calendar': cal,
        'today': today.day,
    }
    return render(request, 'index.html', context)

#production form
def production_data(request):
    today = datetime.today()
    selected_date = request.GET.get('date', today)

    try:
        data = Production.objects.get(production_date = selected_date)
    except Production.DoesNotExist:
        data = None
    
    form = ProductionForm()

    if request.method == 'POST' :
        form = ProductionForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            form = ProductionForm(instance=data)
    return render(request, 'production.html',{'form':form,'today': today})

#Login Page
def login(request, id):
    user = User.objects.filter(id = id)
    return redirect('/')
