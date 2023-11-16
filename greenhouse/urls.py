from django.urls import path
from django.contrib.auth.views import PasswordResetConfirmView

from . import views
from .views import GenerateQRCodeView,CustomLoginView, UserDetailUpdateView, ProductionCreateView, ProductionDataCSVView, RejectedDataCreateView

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.calendar_view, name='index'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('choice_page/', views.choice_page, name='choice_page'),
    path('production_data/', ProductionCreateView.as_view() , name='production_data'),
    path('rejected_data/', RejectedDataCreateView.as_view() , name='rejected_data'),
    path('reports/', views.generate_report, name='reports'),
    path('profile/', views.user_details, name='profile'),
    path('user/<int:pk>/update/', UserDetailUpdateView.as_view(),name='update_user'),
    path('generate_qr_code/<int:pk>/', GenerateQRCodeView.as_view(), name='generate_qr_code'),
    path('download-production-csv/', ProductionDataCSVView.as_view(), name='download_production_csv'),
    path('activate/<str:uidb64>/<str:token>/', PasswordResetConfirmView.as_view(), name='activate_account'),
    # path('activation-success/', views.activation_success, name='custom_activation_success'),
    # path('activation-error/', views.activation_error, name='activation_error'),


]
