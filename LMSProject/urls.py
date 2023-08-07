"""LMSProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from LMSProject import views

student = views.Library()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', student.homes),
    path('returnHome', student.returnHome),
    path('signed', student.signed),
    path('signed/sign', student.sign),
    path('login', student.loged),
    path('login/signin', student.signin),
    path('issueBook', student.issuedBook),
    path('issueBook/issuedDetails', student.issuedDetails),
    path('submitBook', student.submitBook),
    path('submitBook/book', student.submitBookDetails),
    path('issueShowBook', student.issueBookShow),
    path('logout', student.logout)
]
