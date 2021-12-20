from django.contrib import admin

# Register your models here.
from quizapp.models import Choice, Question, Quiz


class ChoiceAdmin(admin.ModelAdmin):
    search_fields = ['uuid']


class QuestionAdmin(admin.ModelAdmin):
    pass


class QuizAdmin(admin.ModelAdmin):
    pass


admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Question, ChoiceAdmin)
admin.site.register(Quiz, QuizAdmin)
