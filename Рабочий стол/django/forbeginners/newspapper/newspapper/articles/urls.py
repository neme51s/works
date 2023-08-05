from django.urls import path

from articles.views import (ArticlesListView,
                            ArticlesUpdateView,
                            ArticlesDetailView,
                            ArticlesDeleteView,
                            ArticleCreateView,
                            )

urlpatterns = [
    path('', ArticlesListView.as_view(), name='article_list'),
    
    path('<int:pk>/',
        ArticlesDetailView.as_view(), name='article_detail'),

    path('<int:pk>/edit/',
        ArticlesUpdateView.as_view(), name='article_edit'),

    path('<int:pk>/delete/',
        ArticlesDeleteView.as_view(), name='article_delete'),
    
    path("new/", ArticleCreateView.as_view(), name="article_new")

]