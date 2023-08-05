from django.urls import path, include
from rest_framework import routers
from .views import SubjectListView, SubjectDetailView, CourseViewSet


router = routers.DefaultRouter()
router.register('courses', CourseViewSet)

app_name = 'courses'


urlpatterns = [
    path('subjects/', SubjectListView.as_view(), name='subject_list'),
    path('subjects/<pk>/', SubjectDetailView.as_view(), name='subject_detail'),
    path('', include(router.urls)),
]