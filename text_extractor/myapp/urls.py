from django.urls import path
from myapp.views import upload_file

urlpatterns = [
    path('text-extractor',view = upload_file,name = 'text-extractor')
   
    ]