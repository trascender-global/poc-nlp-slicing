"""webnlp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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

from core import views as core_views

urlpatterns = [
    path('', core_views.home,name='home'),
    path('base/', core_views.base,name='base'),
    path('info/', core_views.info,name='info'),
    path('slicing/', core_views.slicing,name='slicing'),
    path('results/', core_views.results,name='results'),
    path('team/', core_views.team,name='team'),
    path('text-analytics-details/', core_views.textAnalyticsDetails,name='textAnalyticsDetails'),
    path('admin/', admin.site.urls),
]
