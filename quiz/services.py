from quizapp.models import Choice
from .dto import QuizDTO, AnswersDTO


class QuizResultService:
    def __init__(self, quiz_dto: QuizDTO, answers_dto: AnswersDTO):
        self.quiz_dto = quiz_dto
        self.answers_dto = answers_dto

    def get_result(self) -> float:
        length: int = len(self.answers_dto.answers)
        right_answers: int = 0

        for answer in self.answers_dto.answers:
            right_choices = Choice.objects \
                .filter(is_correct=True) \
                .filter(question_id=answer.question_uuid) \
                .values_list("uuid")
            right_choices = {str(choice[0]) for choice in right_choices}
            selected_choices = {choice[0] for choice in answer.choices}

            if all(choice in right_choices for choice in selected_choices):
                right_answers += 1

        result = right_answers / length

        return round(result, 2)
