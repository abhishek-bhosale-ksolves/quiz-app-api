from django.urls import path
from quiz.views import AttendQuizView, HomeScreen, QuestionDetailView, QuestionListCreateView, QuizListCreateView, QuizDetailView, ScoreView

urlpatterns = [
    path('',HomeScreen.as_view()),
    path('attend-quiz/<int:quiz_id>/', AttendQuizView.as_view(), name='attend-quiz'),
    path('score/<int:quiz_id>/', ScoreView.as_view(), name='get-score'),
    path('quizzes/', QuizListCreateView.as_view(), name='quiz-list-create'),
    path('quizzes/<int:pk>/', QuizDetailView.as_view(), name='quiz-detail'),
    path('quizzes/<int:quiz_id>/questions/', QuestionListCreateView.as_view(), name='question-list-create'),
    path('quizzes/<int:quiz_id>/questions/<int:pk>/', QuestionDetailView.as_view(), name='question-detail'),
]
