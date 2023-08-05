from typing import Any, Dict
from django.forms.models import modelform_factory 
from django.apps import apps
from django.views.generic import CreateView, \
    UpdateView, DeleteView, ListView
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View 
from django.core.cache import cache

from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from .forms import ModuleFormSet
from .mixins import OwnerCourseEditMixin, OwnerCourseMixin
from .models import Module, Content, Course
from students.forms import CourseEnrollForm

class ManageCourseListView(OwnerCourseMixin, ListView): 
    template_name = 'course/list.html'
    permission_required = 'courses.view_course'


class CourseCreateView(OwnerCourseEditMixin, CreateView): 
    permission_required = 'courses.add_course'


class CourseUpdateView(OwnerCourseEditMixin, UpdateView): 
    permission_required = 'courses.change_course'


class CourseDeleteView(OwnerCourseMixin, DeleteView): 
    template_name = 'course/delete.html'
    permission_required = 'courses.delete_course'


class CourseModuleUpdateView(TemplateResponseMixin, View): 
    template_name = 'course/formset.html' 
    course = None
    
    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course, data=data)

    def dispatch(self, request, pk): 
        self.course = get_object_or_404(
            Course, pk=pk, owner=request.user) 
        return super().dispatch(request, pk)

    def get(self, request, *args, **kwargs): 
        formset = self.get_formset()
        return self.render_to_response(
            {'course': self.course, 'formset': formset}
        )

    def post(self, request, *args, **kwargs): 
        formset = self.get_formset(data=request.POST) 
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')

        return self.render_to_response({
            'course': self.course, 'formset': formset})




class ContentCreateUpdateView(TemplateResponseMixin, View): 
    module = None
    model = None
    obj = None
    template_name = 'courses/form.html'

    def get_model(self, model_name):
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(app_label='courses', 
                model_name=model_name)
        return None

    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(model, 
            exclude=['owner', 'order', 'created', 'updated'])
        return Form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id=None): 
        self.module = get_object_or_404(Module,
            id=module_id,
            course__owner=request.user) 
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(
                self.model, id=id, owner=request.user) 
                
        return super().dispatch(request, module_id, model_name, id)

    def get(self, request, module_id, model_name, id=None): 
        form = self.get_form(self.model, instance=self.obj) 
        return self.render_to_response(
            {'form': form, 'object': self.obj})

    def post(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model,
                             instance=self.obj,
                             data=request.POST,
                             files=request.FILES)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                # new content
                Content.objects.create(module=self.module,
                                       item=obj)
            return redirect('module_content_list', self.module.id)
        return self.render_to_response({'form': form,
                                        'object': self.obj})


class ContentDeleteView(View): 
    def post(self, request, id):
        content = get_object_or_404(Content, id=id,
            module__course__owner=request.user) 
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('module_content_list', module.id)
    
class ModuleContentListView(TemplateResponseMixin, View): 
    template_name = 'courses/content_list.html'
    
    def get(self, request, module_id): 
        module = get_object_or_404(Module, id=module_id, 
            course__owner=request.user) 
        
        return self.render_to_response({'module': module})


class ModuleOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def post(self, request):
        for id, order in self.request_json.items():
            Module.objects.filter(id=id,
                course__owner=request.user).update(order=order)

        return self.render_json_response({'saved': 'OK'})


class ContentOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def post(self, request):
        for id, order in self.request_json.items():
            Content.objects.filter(id=id,
                module__course__owner=request.user) \
                .update(order=order)

        return self.render_json_response({'saved': 'OK'})


from django.db.models import Count 
from .models import Subject


class CourseListView(TemplateResponseMixin, View): 
    model = Course
    template_name = 'courses/list.html'

    def get(self, request, subject=None):
        subjects = Subject.objects.annotate(
            total_courses=Count('courses'))
        courses = Course.objects.annotate(
            total_modules=Count('modules'))
        
        subjects = cache.get('all_subjects')
        if not subjects:
            subjects = Subject.objects.annotate(
                total_courses=Count('courses'))
            cache.set('all_subjects', subjects)
            
        if subject:
            subject = get_object_or_404(Subject, slug=subject)
            courses = courses.filter(subject=subject)
        
        return self.render_to_response(
            {'subjects': subjects, 'subject': subject,
                'courses': courses})

from django.views.generic.detail import DetailView

class CourseDetailView(DetailView): 
    model = Course
    template_name = 'courses/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enroll_form'] = CourseEnrollForm(initial={'course':self.get_object})
        return context