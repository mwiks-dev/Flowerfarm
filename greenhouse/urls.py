from django.urls import path
from django.urls import include

from . import views
from .views import GenerateQRCodeView


import datetime

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.calendar_view, name='index'),
    path('production_data/', views.upload_prod_data, name='production_data'),
    path('reports/', views.generate_report, name='reports'),
    path('profile/', views.user_profile, name='profile'),
    path('create_profile/', views.create_profile, name='create_profile'),
    path('update_profile/<int:id>', views.update_profile, name='update_profile'),
    path('generate_qr_code/<int:pk>/', GenerateQRCodeView.as_view(), name='generate_qr_code'),
]
