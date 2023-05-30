from django.shortcuts import render, redirect
from django.contrib.auth import login
from users.forms import SignUpForm

# Create your views here.



def signUp(request):

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/courses")
    else:
        form = SignUpForm()


    return render(request, "registration/signup.html", {"form" : form})
