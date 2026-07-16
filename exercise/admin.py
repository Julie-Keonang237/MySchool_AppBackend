from django.contrib import admin

from exercise.models import Exercise, Question


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]


admin.site.register(Question)
