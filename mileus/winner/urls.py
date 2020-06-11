from django.urls import path

from . import views

urlpatterns = [
    path('winner/', views.WinnerView.as_view()),
]
