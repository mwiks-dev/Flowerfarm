from django.shortcuts import render
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required



import calendar
from datetime import datetime
import time

from.models import Production, User
from .forms import ProductionForm

# Create your views here.  

#index/calendar view function
@login_required(login_url='/accounts/login/')
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
@login_required(login_url='/accounts/login/')
def upload_prod_data(request):
    today = datetime.today()
    selected_date = request.GET.get('date')

    try:
        data = Production.objects.get(production_date = selected_date)
    except Production.DoesNotExist:
        data = None
    
    form = ProductionForm()

    if request.method == 'POST' :
        form = ProductionForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.save()
        return redirect('index')
    else:
        form = ProductionForm(instance=data)
    return render(request, 'production.html',{'form':form,'today': today})

#report generation
@login_required(login_url='/accounts/login/')
def generate_report(request):
    data = Production.objects.all()

    # Search functionality
    query = request.GET.get('q')
    if query:
        data = data.filter(Q(variety__icontains=query) | Q(greenhouse_number__icontains=query))
    paginator = Paginator(data, 1)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'report_template.html',{'page_obj':page_obj} )
