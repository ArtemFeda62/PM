from . import views

app_name = 'fandom'

urlpatterns = [
    path('create/', views.create_anomalie, name='create'),
    path('', views.anomalie_list, name='anomalie_list'),
    path('edit/', views.anomalie_edit, name='anomalie_edit'),
    path('delete/', views.anomalie_delete, name='anomalie_delete'),
]