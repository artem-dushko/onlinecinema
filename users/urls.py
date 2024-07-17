from django.urls import path
from . import views

urlpatterns = [
    path('subscription/', views.subscription, name='subscription'),
    path('process_subscription/', views.process_subscription, name='process_subscription'),
    path('process_payment/', views.process_payment, name='process_payment'),
    path('execute_payment/', views.execute_payment, name='execute_payment'),
    path('payment_successful/', views.payment_successful, name='payment_successful'),
]