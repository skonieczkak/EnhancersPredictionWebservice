from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard_view, name='dashboard_view'),
    path('submit', views.handle_form_submission, name='handle_form_submission'),
    path('download-data/', views.download_data, name='download_data'),
]
