from django.urls import path
from django.urls import include

from . import views

import datetime

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.calendar_view, name='index'),
    path('production_data/', views.production_data, name='production_data'),


]
