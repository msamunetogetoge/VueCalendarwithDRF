from django.urls import path
from schedule import views

urlpatterns = [
    path('schedules/', views.schedule_list),
    path('schedules_detail/<int:planid>/', views.schedule_detail),
]
