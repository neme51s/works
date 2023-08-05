from typing import Optional
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Articles
from django.urls import reverse_lazy, reverse
from .forms import CommentForm
from django.views import View

class ArticlesListView(LoginRequiredMixin, ListView): 
    model = Articles
    template_name = 'article_list.html'


class ArticleCreateView(LoginRequiredMixin, CreateView): 
    model = Articles
    template_name = "article_new.html"
    fields = (
        "title",
        "body",
    )

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticlesDetailView(LoginRequiredMixin, DetailView): 
    model = Articles
    template_name = 'article_detail.html'


class ArticlesUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): 
    model = Articles
    fields = ('title', 'body',)
    template_name = 'article_edit.html'
    success_url = reverse_lazy('article_list')

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user
    

class ArticlesDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Articles
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user
    

class CommentGet(DetailView): 
    model = Articles
    template_name = "article_detail.html"
    success_url = reverse_lazy('article_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context
    
    
class CommentPost(SingleObjectMixin, FormView):
    model = Articles
    form_class = CommentForm
    template_name = "article_detail.html"
    success_url = reverse_lazy('article_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)
    
    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.article = self.object   
        comment.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        article = self.get_object()
        return reverse("article_detail", kwargs={"pk": article.pk})


class ArticlesDetailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        view = CommentGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentPost.as_view()
        return view(request, *args, **kwargs)
