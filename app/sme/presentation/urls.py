from django.urls import path
from sme.presentation.views import IndexView

app_name = 'index'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    
   
]
