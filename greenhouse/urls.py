from django.urls import path
from django.contrib.auth.views import PasswordResetConfirmView

from . import views
from .views import GenerateQRCodeView,CustomLoginView, UserDetailUpdateView, ProductionCreateView, RejectedDataCreateView,download_excel_report
urlpatterns = [
    # path('', views.index, name='index'),
    # path('', views.calendar_view, name='index'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('choice_page/', views.choice_page, name='choice_page'),
    path('production_data/', ProductionCreateView.as_view() , name='production_data'),
    path('rejected_data/', RejectedDataCreateView.as_view() , name='rejected_data'),
    path('download_excel_report/', views.download_excel_report, name='download_excel_report' ),
    path('production_data_report/', views.production_report, name='production_data_report'),
    path('rejected_data_report/', views.rejection_report, name='rejected_data_report'), 
    path('report_choice_page/', views.report_choice_page, name='report_choice_page'),   
    path('profile/', views.user_details, name='profile'),
    path('user/<int:pk>/update/', UserDetailUpdateView.as_view(),name='update_user'),
    path('generate_qr_code/<int:pk>/', GenerateQRCodeView.as_view(), name='generate_qr_code'),
    path('activate/<str:uidb64>/<str:token>/', PasswordResetConfirmView.as_view(), name='activate_account'),
    # path('activation-success/', views.activation_success, name='custom_activation_success'),
    # path('activation-error/', views.activation_error, name='activation_error'),


]
