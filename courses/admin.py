from django.contrib import admin
from .models import Course,Category,Tag

# Register your models here.


# admin.site.register([Course, Tag, Category])

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "description",
        "price",
        "user",
        "is_published",
        "slug",
        "updated_at"
    )

    search_fields = (
        "title",
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
