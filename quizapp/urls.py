from django.urls import path

from quizapp.views import QuizView

qv = QuizView()
urlpatterns = [
    path("quiz/<str:quiz_uuid>/question/<int:question_id>", qv.question, name='quiz'),
    path("", qv.welcome, name="welcome")
]
