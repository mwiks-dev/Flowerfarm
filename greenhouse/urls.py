from django.urls import path

from . import views
from .views import GenerateQRCodeView,CustomLoginView, UserDetailUpdateView


import datetime

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.calendar_view, name='index'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('production_data/', views.upload_prod_data, name='production_data'),
    path('reports/', views.generate_report, name='reports'),
    path('profile/', views.user_details, name='profile'),
    path('user/<int:pk>/update/', UserDetailUpdateView.as_view(),name='update_user'),
    path('generate_qr_code/<int:pk>/', GenerateQRCodeView.as_view(), name='generate_qr_code'),
]
