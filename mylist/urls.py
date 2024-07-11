from django.urls import path
from . import views

app_name = 'mylist'

urlpatterns = [
    path('toggle_watch_list/<int:video_id>/', views.toggle_watch_list, name='toggle-watch-list'),
    path('', views.mylist, name='mylist'),
]