from django.shortcuts import render
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic import View

import calendar
from datetime import datetime
import qrcode
from PIL import Image
import csv

from.models import Production, User
from .forms import ProductionForm

# Create your views here.  

#login view

class CustomLoginView(LoginView):
    template_name = 'registration/login.html' 

class UserDetailUpdateView(LoginRequiredMixin, UpdateView):
    model = User  
    template_name = 'update.html'  # Create this template
    fields = ['full_name', 'email','prof_photo','phone_number'] 
    success_url = '/greenhouse/profile/'

    def get_object(self, queryset=None):
        # Retrieve the user object based on the provided primary key (pk)
        return get_object_or_404(self.model, pk=self.kwargs['pk'])

    def form_valid(self, form):
        # Save the updated user details
        user = form.save()
        # You can perform additional actions if needed
        return super().form_valid(form)
    

#index/calendar view function
@login_required(login_url='/login/')
def calendar_view(request):
    current_user = request.user
    username = current_user.full_name

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

#user details page
@login_required(login_url='/login/')
def user_details(request):
    current_user = request.user
    profile = User.objects.filter(id=current_user.id).first()

    return render(request,"profile.html",{'profile':profile})

#production form
class ProductionCreateView(CreateView):
    model = Production
    form_class = ProductionForm
    template_name = 'production.html'
    success_url = reverse_lazy('reports')

    def form_valid(self, form):
        # Associate the user with the profile
        form.instance.user = self.request.user 

        return super().form_valid(form)
    
#report generation
def generate_report(request):
    data = Production.objects.order_by('-production_date')

    # Search functionality
    query = request.GET.get('q')
    if query:
        data = data.filter(Q(variety__icontains=query) | Q(greenhouse_number__icontains=query))
    paginator = Paginator(data, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'report_template.html',{'page_obj':page_obj} )

#qr code generation
@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(never_cache, name='dispatch')
class GenerateQRCodeView(View):
    def get(self, request, pk):
        # Retrieve the object from the model based on the primary key (pk)
        prod_data = get_object_or_404(Production, pk=pk)
        
        # Concatenate the fields into a single string
        data_to_encode = f"Date: {prod_data.production_date},  Variety: {prod_data.variety}, Length: {prod_data.length}, GreenHouse Number: {prod_data.greenhouse_number}, Staff: {prod_data.user}, Rejects: {prod_data.rejected_flowers}, Reason: {prod_data.rejection_reason}"
        
        # Create a QR code instance
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        
        # Add data to the QR code
        qr.add_data(data_to_encode)
        qr.make(fit=True)
        
        # Create an image from the QR code
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Serve the image as a response
        response = HttpResponse(content_type="image/png")
        img.save(response, "PNG")
        
        return response
    
class ProductionDataCSVView(View):
    def get(self, request):
        # Query the production data you want to include in the report
        production_data = Production.objects.order_by('-production_date')
        # Create a CSV response
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="production_report.csv"'

        # Create a CSV writer
        writer = csv.writer(response)

        # Write the CSV header
        writer.writerow(['Date', 'Variety', 'Length', 'Greenhouse Number', 'Staff', 'Rejects', 'Reason'])

        # Write production data rows
        for data in production_data:
            user_staff_number = data.user.staff_number if data.user and hasattr(data.user, 'staff_number') else ''

            writer.writerow([
                data.production_date,
                data.variety,
                data.length,
                data.greenhouse_number,
                user_staff_number , 
                data.rejected_flowers,
                data.rejection_reason,
            ])

        return response

