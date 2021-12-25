from typing import List
from copy import deepcopy
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from quiz.dto import QuestionDTO, ChoiceDTO, QuizDTO, AnswersDTO, AnswerDTO
from quiz.services import QuizResultService
from quizapp.models import Quiz, Question, Choice
from quizapp.settings import DEFAULT_QUIZ_UUID


def get_quiz(quiz_uuid: str) -> QuizDTO:
    quiz = Quiz.objects.get(uuid=quiz_uuid)
    questions = Question.objects.filter(quiz_id=quiz_uuid)
    questions_dto = [
        QuestionDTO(uuid=question.uuid, text=question.text, choices=[
            ChoiceDTO(text=choice.text, uuid=choice.uuid, is_correct=choice.is_correct)
            for choice in
            Choice.objects.filter(question_id=question.uuid)
        ])
        for question in questions
    ]
    quiz_dto = QuizDTO(title=quiz.title, uuid=quiz.uuid, questions=questions_dto)

    return quiz_dto


class QuizView:
    def __init__(self):
        self.set_quiz(quiz_uuid=DEFAULT_QUIZ_UUID)
        self.answers_dto = AnswersDTO(quiz_uuid=DEFAULT_QUIZ_UUID, answers=[])
        self.quiz_dto: QuizDTO = get_quiz(DEFAULT_QUIZ_UUID)
        self.questions = self.quiz_dto.questions
        self.quizzes = Quiz.objects.all()
        self.answers: List[AnswerDTO] = []

    def set_quiz(self, answers=None, quiz_uuid: str = DEFAULT_QUIZ_UUID) -> None:
        if answers is None:
            answers = []
        self.answers_dto = AnswersDTO(quiz_uuid, answers=answers)
        self.quiz_dto: QuizDTO = get_quiz(quiz_uuid)
        self.questions = self.quiz_dto.questions

    def welcome(self, request: HttpRequest) -> HttpRequest:
        context = {
            "quizzes": self.quizzes
        }

        return render(request, "index.html", context)

    def done(self, request: HttpRequest) -> HttpResponse:
        result = QuizResultService(self.quiz_dto, deepcopy(self.answers_dto)).get_result()
        context = {
            "result": result,
            "quizzes": self.quizzes
        }
        self.answers_dto.answers.clear()
        self.answers.clear()
        return render(request, "done.html", context)

    def append_answer(self, question_id: int, choices: List[str]) -> None:

        question = self.questions[question_id - 1]

        answer = AnswerDTO(
            question_uuid=question.uuid, choices=choices
        )
        self.answers.append(answer)

    def question(self, request: HttpRequest, quiz_uuid: str, question_id: int) -> HttpResponse:
        self.set_quiz(self.answers, quiz_uuid)
        choices = list(request.GET.items())

        if question_id >= len(self.questions):
            self.append_answer(question_id, choices)
            return self.done(request)
        if len(request.GET):
            self.append_answer(question_id, choices)

        context = {
            "question": self.questions[question_id],
            "choices": zip(self.questions[question_id].choices, "ABCD"),
            "quiz_uuid": quiz_uuid,
            "next": question_id + 1,
            "quizzes": self.quizzes
        }
        return render(request, "question.html", context)
