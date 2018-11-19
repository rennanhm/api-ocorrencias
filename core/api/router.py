from django.urls import path
from .viewsets import TotalOccurrencesAPIView

urlpatterns = [
    path('occurrence/', TotalOccurrencesAPIView.as_view()),
]
