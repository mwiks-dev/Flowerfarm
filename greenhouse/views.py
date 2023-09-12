from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone

from.models import Production, User
from .forms import ProductionForm

# Create your views here.

#Home page
def index(request):
    name = "Mwikali"
    today = timezone.now().date()
    selected_date = request.GET.get('date', today)

    try:
        data = Production.objects.get(production_date=selected_date)
    except Production.DoesNotExist:
        data = None

    if request.method == 'POST':
        form = ProductionForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ProductionForm(instance = data)
    return render(request, 'index.html',{
        'name':name,
        'form':form,
        'selected_date':selected_date})

#Login Page
def login(request, id):
    user = User.objects.filter(id = id)
    return redirect('/')
