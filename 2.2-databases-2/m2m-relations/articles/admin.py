from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from articles.models import Article, Relationship, Object


class RelationshipInlineFormset(BaseInlineFormSet):
    def clean(self):
        all_tag_count = list(form.cleaned_data['tag'].id
                             for form in self.forms
                             if form.cleaned_data)
        main_tag_count = list(form.cleaned_data['tag'].id
                              for form in self.forms
                              if form.cleaned_data
                              if form.cleaned_data['is_main']
                              is True)

        if len(main_tag_count) > 1:
            raise ValidationError('Основной раздел может быть только один!')

        if len(all_tag_count) > 0 and len(main_tag_count) < 1:
            raise ValidationError('Выберите один основной раздел!')

        if len(all_tag_count) != len(set(all_tag_count)):
            raise ValidationError('Тут всегда ошибка!')

        return super().clean()


class RelationshipInline(admin.TabularInline):
    model = Relationship
    formset = RelationshipInlineFormset
    extra = 1


@admin.register(Object)
class ObjectAdmin(admin.ModelAdmin):
    inlines = [RelationshipInline]


@admin.register(Article)
class Article(admin.ModelAdmin):
    verbose_name = ['title', 'text', 'published_at', 'image']
    ordering = ['-published_at']
    inlines = [RelationshipInline]

    class Meta(admin.ModelAdmin):
        verbose_name = ['Статьи']
        verbose_name_plural = ['Статьи']
        inlines = [RelationshipInline]
