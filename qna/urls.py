from django.urls import path,include
from .views import QuestionCreateView,QuestionDeleteView,QuestionDetailView,QuestionListView,add_anwer_to_question,AnswerDeleteView,upvoteAnswer,downvoteAnswer,filtered_tag_questions,TagListView

urlpatterns = [
    path('question/new',QuestionCreateView.as_view(),name='new-question'),
    path('question/<int:pk>',add_anwer_to_question,name="question-detail"),
    path('question/all',QuestionListView.as_view(),name='question-list'),
    path('question/delete/<int:pk>',QuestionDeleteView.as_view(),name='question-delete'),
    path('question/answer/<int:pk>',add_anwer_to_question,name='question-answer'),
    path('question/answer/delete/<int:pk>',AnswerDeleteView.as_view(),name='delete-answer'),
    path('question/answer/upvote/<int:pk>',upvoteAnswer,name='upvote-answer'),
    path('question/answer/downvote/<int:pk>',downvoteAnswer,name='downvote-answer'),
    path('question/tag/<str:slug>',filtered_tag_questions,name='tagged-questions'),
    path('question/tags/all',TagListView.as_view(),name='tag-list'),
]