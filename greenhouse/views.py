from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect, render

# Create your views here.

#Home page
def index(request):
    return HttpResponse('Welcome Home')

#Login Page
def login(request):
    return redirect('/')
