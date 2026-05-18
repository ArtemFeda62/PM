from django.urls import path
from . import views

app_name = 'fandom'

urlpatterns = [
    path('', views.anomalie_list, name='anomalie_list'),
    path('<int:pk>/', views.anomalie_detail, name='anomalie_detail'),
    path('create/', views.create_anomalie, name='create'),
    path('<int:pk>/edit/', views.anomalie_edit, name='anomalie_edit'),
    path('<int:pk>/delete/', views.anomalie_delete, name='anomalie_delete'),
    path('check-code/', views.check_code_uniqueness, name='check_code_uniqueness'),
    path('<int:pk>/delete-ajax/', views.delete_anomaly_ajax, name='delete_anomaly_ajax'),
]