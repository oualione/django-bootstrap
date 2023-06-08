from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContactForm, CourseForm
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.urls import reverse_lazy
#from django.contrib import messages
from django.views.generic import ListView, DetailView, DeleteView
from courses.models import Course, Tag
from django.http import HttpResponse, Http404
import sweetify

# Create your views here.


title = "Hello Python"
description = "This is a Python Course"




# get_all_courses = [
#     {
#         "title": "MERN STACK APPLICATION",
#         "description": "Learn how to create MERN STACK Application",
#         "image": "https://process.fs.teachablecdn.com/ADNupMnWyR7kCWRvm76Laz/resize=width:705/https://cdn.filestackcontent.com/ndgpEj1YRAqrlS0gNZBb",
#         "price": 0
#     },
#     {
#         "title": "ANGULAR APPLICATION",
#         "description": "Learn how to create ANGULAR Application",
#         "image": "https://process.fs.teachablecdn.com/ADNupMnWyR7kCWRvm76Laz/resize=width:705/https://cdn.filestackcontent.com/PU65W4VzTB205p8JT7PG",
#         "price": 40
#     },
#     {
#         "title": "PHP LARAVEL APPLICATION",
#         "description": "Learn how to create LARAVEL Application",
#         "image": "https://process.fs.teachablecdn.com/ADNupMnWyR7kCWRvm76Laz/resize=width:705/https://cdn.filestackcontent.com/nSksEHOHQLSteJPjCg9t",
#         "price": 25
#     },
#     {
#         "title": "PHP LARAVEL APPLICATION",
#         "description": "Learn how to create LARAVEL Application",
#         "image": "https://process.fs.teachablecdn.com/ADNupMnWyR7kCWRvm76Laz/resize=width:705/https://cdn.filestackcontent.com/nSksEHOHQLSteJPjCg9t",
#         "price": 25
#     },
#     {
#         "title": "PHP LARAVEL APPLICATION",
#         "description": "Learn how to create LARAVEL Application",
#         "image": "https://process.fs.teachablecdn.com/ADNupMnWyR7kCWRvm76Laz/resize=width:705/https://cdn.filestackcontent.com/nSksEHOHQLSteJPjCg9t",
#         "price": 25
#     },
#     {
#         "title": "PHP LARAVEL APPLICATION",
#         "description": "Learn how to create LARAVEL Application",
#         "image": "https://process.fs.teachablecdn.com/ADNupMnWyR7kCWRvm76Laz/resize=width:705/https://cdn.filestackcontent.com/nSksEHOHQLSteJPjCg9t",
#         "price": 25
#     },

# ]

class HomeView(ListView):
   model = Course
   # Specify the template to use for rendering the list
   template_name = 'courses/course_list.html'
   context_object_name = 'courses'


class ShowOneCourseView(DetailView):
    model = Course
    template_name = 'courses/show.html'


class DeleteCourseView(DeleteView):
    model = Course
    template_name = 'courses/delete.html'
    success_url = reverse_lazy("course_list")

    def delete(self, request, *args, **kwargs):
        # Get the object being deleted
        self.object = self.get_object()

        # Add Sweetify flash message
        sweetify.success(request, 'Object deleted successfully.', icon='success')

        # Call the delete() method to perform the deletion
        return super().delete(request, *args, **kwargs)



def get_courses(request):

    search = ""
    tags = []

    if request.GET.get("search"):
        search = request.GET.get("search")
        tags = Tag.objects.filter(label__icontains=search)

    data = Course.objects.distinct().filter(
        Q(title__icontains=search)|
        Q(description__icontains=search)|
        Q(user__name__icontains=search)|
        Q(category__label__icontains=search)|
        Q(tags__in = tags)
        )

    items_per_page = 3

    paginator = Paginator(data, items_per_page)
    page = request.GET.get('page')
    courses = paginator.get_page(page)

    return render(request, "courses/index.html", {"title": title,
                                                  "description": description,
                                                  "courses": courses,
                                                  "search" : search,
                                                  "paginator" :paginator
                                                  })

def get_one_course(request, id):
    # data = Course.objects.get(pk=id)

    # return render(request, "courses/show.html", {"course" : data})

    data = get_object_or_404(Course, pk=id)
    return render(request, "courses/show.html", {"course" : data})

def contact_us(request):

    if request.method == "POST":
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            print(contact_form.cleaned_data)
    else:
        contact_form = ContactForm()
    return render(request, "courses/contact.html", {"form" : contact_form})

# def create_course(request):
#     # if request.method == "POST":
#     #     course_form = CourseForm(request.POST)
#     #     if course_form.is_valid():
#     #         print(course_form.cleaned_data)
#     # else:
#         course_form = CourseForm()
#         return render(request, "courses/create.html", {"form" : course_form})


@login_required(login_url='/login')
@permission_required("courses.add_course", raise_exception=True)
def create_course(request):

    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.user = request.user.profile
            course.save()
            sweetify.success(request, 'Course Added Successfully')
            return redirect("course_list")
        else :
            return HttpResponse("Course not saved")
    else:
        form = CourseForm()
    return render (request, "courses/create.html", {"form": form})


@login_required(login_url='/login')
def edit_course(request, id):

    if not request.user.has_perm("courses.change_course"):
        return redirect("/courses")

    course = Course.objects.get(pk=id)

    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            sweetify.success(request, 'Course Updated Successfully')
            return redirect("show_course", pk=id)
        else:
            return HttpResponse("Course not saved")
    else:
        form = CourseForm(instance=course)
    return render(request, "courses/edit.html", {"form": form})


@login_required(login_url='/login')
def delete_course(request, id):

    course = Course.objects.get(pk=id)
    
    if request.method == 'POST':
        course.delete()
        sweetify.success(request, 'Course Deleted Successfully')
        return redirect("course_list")
    return render(request, 'courses/delete.html', {"course" : course})




