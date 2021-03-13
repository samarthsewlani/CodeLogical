from django.urls import path
from .views import home,BlogCreateView,BlogDetailView,BlogUpdateView,BlogDeleteView,BlogListView,filtered_tag_questions,TagListView,searchResult,BlogSearchListView,QuestionSearchListView
from django.views.generic import TemplateView

urlpatterns = [
    path('',home,name='home'),
    path('createblog/',BlogCreateView.as_view(),name='create-blog'),
    path('blog/<int:pk>',BlogDetailView.as_view(),name='blog-detail'),
    path('blog/update/<int:pk>',BlogUpdateView.as_view(),name='blog-update'),
    path('blog/delete/<int:pk>',BlogDeleteView.as_view(),name='blog-delete'),
    path('blog/all',BlogListView.as_view(),name='blog-list'),
    path('base/',TemplateView.as_view(template_name='blog/base.html'),name='base'),
    path('blog/tag/<str:slug>',filtered_tag_questions,name='tagged-blogs'),
    path('blog/tags/all',TagListView.as_view(),name='tag-list-blogs'),
    path('search/<str:slug>',searchResult,name='search-result'),
    path('search/<str:slug>/blogs',BlogSearchListView.as_view(),name='search-result-blogs'),
    path('search/<str:slug>/questions',QuestionSearchListView.as_view(),name='search-result-questions'),
]