from django.urls import path
from .views import get_courses, contact_us, create_course, ShowOneCourseView, edit_course, DeleteCourseView


urlpatterns = [
    path('', get_courses, name="course_list"),
    path('contact/', contact_us, name="contact"),
    path('create/', create_course, name="create_course"),
    path('<int:pk>/', ShowOneCourseView.as_view(), name="show_course"),
    path('<int:id>/edit', edit_course, name="edit_course"),
    path('<int:pk>/delete', DeleteCourseView.as_view(), name="delete_course")

    # path('create/', create_course)
    # path('<int:id>', get_one_course)


]
