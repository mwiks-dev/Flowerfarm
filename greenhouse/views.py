from django.shortcuts import render
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from django.views import View
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy

import calendar
from datetime import datetime
import qrcode
from PIL import Image

from.models import Production, Profile, User
from .forms import ProductionForm,UpdateProfileForm,CreateProfileForm

# Create your views here.  

#login view

class CustomLoginView(LoginView):
    template_name = 'registration/login.html' 

#create profile page
# @login_required(login_url='/greenhouse/login/')
class UserProfileCreateView(CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = 'create_profile.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        # Associate the user with the profile
        form.instance.user = self.request.user 
        
        # Handle the uploaded file, if provided
        if self.request.FILES.get('prof_photo'):
            form.instance.prof_photo = self.request.FILES['prof_photo']

        return super().form_valid(form)

#profile page
@login_required(login_url='/accounts/login/')
def user_profile(request):
    current_user = request.user
    profile = Profile.objects.filter(user_id=current_user.id).first()

    return render(request,"profile.html",{'profile':profile})

# update profile page
# @login_required(login_url='/accounts/login/')
class UserProfileUpdateView(UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'update_profile.html'
    success_url = reverse_lazy('/greenhouse/profile')

#index/calendar view function
@login_required(login_url='/accounts/login/')
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

#production form
@login_required(login_url='login/')
def upload_prod_data(request):
    print(f"User: {request.user}")  # Debugging output

    today = datetime.today()

    form = ProductionForm(request.POST or None, request.FILES or None, user=request.user)
    if request.method == 'POST' :
        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user
            data.save()
        return redirect('index')
    else:
        form = ProductionForm()
    return render(request, 'production.html',{'form':form,'today': today})

#report generation
@login_required(login_url='/accounts/login/')
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
        
        # Concatenate the fields (name, age, and gender) into a single string
        rejects = str(prod_data.rejected_flowers) if prod_data.rejected_flowers is not None else ""
        rej_reason = prod_data.rejection_reason if prod_data.rejection_reason else ""
        data_to_encode = f"Date: {prod_data.production_date}, Variety: {prod_data.variety}, Length: {prod_data.length}"
        
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
