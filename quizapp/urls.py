from django.urls import path

from quizapp.views import QuizView

qv = QuizView()
urlpatterns = [
    path("question/<int:question_id>", qv.index, name='index'),
    # path("done/<int:result>", qv.done, name='done'),
]
