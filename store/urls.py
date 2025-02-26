from django.urls import path
from .views import HomePageView


urlpatterns = [
    #path('',)
    path('',HomePageView.as_view(), name='home'),
]