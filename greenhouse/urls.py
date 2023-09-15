from django.urls import path
from django.urls import include

from . import views

import datetime

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.calendar_view, name='index'),
    path('production_data/', views.upload_prod_data, name='production_data'),
    path('reports/', views.generate_report, name='reports'),
    path('profile/', views.user_profile, name='profile'),

    


]
