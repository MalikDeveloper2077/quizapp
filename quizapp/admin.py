from django.contrib import admin

from .models import Quiz, Category, Question, QuestionAnswer, Comment, Bookmark, QuizManager


class QuestionAnswerInline(admin.TabularInline):
    model = QuestionAnswer
    extra = 1


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    """Manage Quiz models"""
    list_display = ('title', 'level', 'views', 'date',)
    list_filter = ('date', 'level', 'category')
    search_fields = ['title', 'body']
    readonly_fields = ('date',)

    fieldsets = [
        ('Главное',    {'fields': ['title', 'body', 'date',
                                   'slug', 'level', 'category', 'photo']}),
        ('Автор',      {'fields': ['author']}),
        ('Показатели', {'fields': ['views', 'likes', 'completed']})
    ]

    inlines = [CommentInline]


@admin.register(QuizManager)
class QuizManagerAdmin(admin.ModelAdmin):
    """Manage Quiz managers"""
    list_display = ('quiz', 'completed',)
    list_filter = ('date', 'quiz', 'completed',)
    readonly_fields = ('date',)
    actions = ['mark_as_complete', 'mark_as_incomplete']

    fieldsets = [
        ('Главное', {'fields': ['quiz', 'user', 'date']}),
        ('Данные',  {'fields': ['correct_answers', 'completed']})
    ]

    def mark_as_complete(self, request, queryset):
        queryset.update(completed=True)

    def mark_as_incomplete(self, request, queryset):
        queryset.update(completed=False)

    mark_as_complete.short_description = 'Пометить как завершенные'
    mark_as_incomplete.short_description = 'Пометить как незавершенные'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Manage categories (for quizzes)"""
    list_display = ('name',)
    search_fields = ('name',)

    fieldsets = [
        ('Главное', {'fields': ['name']}),
    ]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Manage comments (for quizzes)"""
    list_display = ('body', 'author', 'quiz', 'date',)
    list_filter = ('date', 'quiz',)
    search_fields = ('body',)
    readonly_fields = ('date',)

    fieldsets = [
        ('Главное', {'fields': ['body', 'date']}),
        ('Автор', {'fields': ['author']}),
        ('Викторина', {'fields': ['quiz']})
    ]


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    """Manage bookmarks (for quizzes)"""
    list_display = ('user', 'quiz',)
    list_filter = ('date',)
    readonly_fields = ('date',)

    fieldsets = [
        ('Главное', {'fields': ['user', 'quiz', 'date']})
    ]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Manage Questions (for quizzes)"""
    list_display = ('title', 'quiz',)
    search_fields = ['title', 'quiz']

    fieldsets = [
        ('Главное', {'fields': ['title', 'quiz']})
    ]

    inlines = [QuestionAnswerInline]


@admin.register(QuestionAnswer)
class QuestionAnswerAdmin(admin.ModelAdmin):
    """Manage QuestionAnswers (for questions)"""
    list_display = ('value', 'question', 'is_correct')
    list_filter = ('is_correct',)
    search_fields = ['value', 'question']

    fieldsets = [
        ('Главное', {'fields': ['question', 'value', 'is_correct']})
    ]


admin.site.site_header = 'Викторины'
