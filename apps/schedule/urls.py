from django.urls import path
from .views import ScheduleListView

urlpatterns = [
    path('schedule/', ScheduleListView.as_view(), name='schedule-list'),
]