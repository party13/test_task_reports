from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', HomePage.as_view(), name='index_page'),
    path('entities/', MyEntities.as_view(), name='my_entities'),
    path('statistics/', MyStatistics.as_view(), name='my_statistics'),
    path('info/', view_info, name='info'),
    path('create/', CreateEntity.as_view(), name='create_entity'),
    path('delete/', delete_entity, name='delete_entity'),
    path('admin/', admin.site.urls),
]
