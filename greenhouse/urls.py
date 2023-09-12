from django.urls import path
from django.urls import include

from . import views

import datetime

urlpatterns = [
    # path('', views.index, name='index'),
    path('calendar/<int:year>/<int:month>/', views.calendar_view, name='index'),

]
