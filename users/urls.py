from django.urls import path
from .views import signUp


urlpatterns = [
    path('signup/', signUp),
    

    # path('create/', create_course)
    # path('<int:id>', get_one_course)


]
