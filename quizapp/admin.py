from django.contrib import admin

from .models import Quiz, Question, QuestionAnswer


class QuestionAnswerInline(admin.TabularInline):
    model = QuestionAnswer
    extra = 1


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    """Manage Quiz model"""
    list_display = ('title', 'level', 'views', 'date',)
    list_filter = ('date', 'level',)
    search_fields = ['title', 'body']
    readonly_fields = ('date',)

    fieldsets = [
        ('Главное', {'fields': ['title', 'body', 'slug', 'date', 'level', 'photo']}),
        ('Показатели', {'fields': ['views', 'likes', 'completed']})
    ]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Manage Question model"""
    list_display = ('title', 'quiz',)
    search_fields = ['title', 'quiz']

    fieldsets = [
        ('Главное', {'fields': ['title', 'quiz']})
    ]

    inlines = [QuestionAnswerInline]


@admin.register(QuestionAnswer)
class QuestionAnswerAdmin(admin.ModelAdmin):
    """Manage QuestionAnswer model"""
    list_display = ('value', 'question', 'is_correct')
    list_filter = ('is_correct',)
    search_fields = ['value', 'question']

    fieldsets = [
        ('Главное', {'fields': ['question', 'value', 'is_correct']})
    ]


admin.site.site_header = 'Викторины'
