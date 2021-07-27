from django.urls import path
from . import views

urlpatterns = [
    path('',views.requestDashboard,name = "requestDashboard"),
    path('processfile',views.processfile,name = "processfile"),
    path('updatelist',views.updatelist,name = "updatelist"),
    path('plotchart',views.plotchart,name = "plotchart"),
    path('dashboard',views.dashboard,name = "dashboard"),
]
