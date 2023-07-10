# from django.urls import path
from . import views

from django.contrib import admin
from django.urls import path,include
# from api.views import CompanyViewSet,EmployeeViewSet
from api.views import IDataViewSet
from rest_framework import routers

router= routers.DefaultRouter()
router.register(r'datas', IDataViewSet)

urlpatterns = [
    path('insert/', views.insert_data, name='insert_data'),
    path('',include(router.urls))
]
