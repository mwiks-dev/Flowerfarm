from django.shortcuts import render
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User




import calendar
from datetime import datetime

from.models import Production, Profile
from .forms import ProductionForm,UpdateProfileForm

# Create your views here.  

#profile page
@login_required(login_url='/accounts/login/')
def user_profile(request):
    current_user = request.user
    profile = Profile.objects.filter(user_id=current_user.id).first()

    return render(request,"profile/profile.html",{'profile':profile})

# update profile page
@login_required(login_url='/accounts/login/')
def update_profile(request,id):
    user = User.objects.get(id=id)
    profile = Profile.objects.get(user = user)
    form = UpdateProfileForm(instance=profile)
    if request.method == "POST":
            form = UpdateProfileForm(request.POST,request.FILES,instance=profile)
            if form.is_valid():  
                profile = form.save(commit=False)
                profile.save()
            return redirect('profile') 
            
    return render(request, 'profile/update_profile.html', {"form":form})

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
