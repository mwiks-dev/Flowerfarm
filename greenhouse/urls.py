from django.urls import path
from django.urls import include

from . import views

import datetime

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.index, name='index'),

]
