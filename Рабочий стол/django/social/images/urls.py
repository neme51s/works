from django.urls import path
from .views import image_create, image_detail, image_like, image_list, image_ranking


urlpatterns = [
    path('create/', image_create, name='create'),
    path('detail/<int:id>/<slug:slug>/', image_detail, name='detail'),
    path('like/', image_like, name='like'),
    path('', image_list, name='list'),
    path('ranking/', image_ranking, name='ranking'),
]