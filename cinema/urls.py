from django.urls import path
from . import views

urlpatterns = [
    path('detail/<int:video_id>/', views.detail, name='cinema-detail'),
    path('', views.home, name='cinema-home')
]
