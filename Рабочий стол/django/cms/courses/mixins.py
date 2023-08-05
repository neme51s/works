from django.urls import reverse_lazy 
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Course


class OwnerMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin:
    def form_valid(self, form):
        form.instance.owner = self.request.user 
        return super().form_valid(form)
    

class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin, PermissionRequiredMixin): 
    model = Course
    fields = ['subject', 'title', 'slug', 'overview'] 
    success_url = reverse_lazy('manage_course_list')


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin): 
    template_name = 'course/form.html'