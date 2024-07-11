from django.urls import path
from .views import subscription, process_subscription

urlpatterns = [
    path('subscription/', subscription, name='subscription'),
    path('process_subscription/', process_subscription, name='process_subscription')
]