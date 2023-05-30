from django import forms
from courses.models import Course


class ContactForm(forms.Form):
    name = forms.CharField(min_length=3, max_length=50, widget=forms.TextInput(attrs={"class" : "form-control"}))
    email = forms.EmailField(max_length=100, widget=forms.EmailInput(attrs={"class" : "form-control"}))
    subject = forms.CharField(min_length=2, max_length=100, widget=forms.TextInput(attrs={"class" : "form-control"}))
    message = forms.CharField(widget=forms.Textarea(attrs={"class" : "form-control", "rows" : 3}))


class CourseForm(forms.ModelForm):
    
    class Meta:
        model = Course
        exclude = ["is_published","user"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for (element, field) in self.fields.items():
            field.widget.attrs.update({"class" : "form-control"})
        # widgets = {
        #     "user": forms.SelectMultiple(attrs={"class": "form-control"}),
        #     "category": forms.SelectMultiple(attrs={"class": "form-control"}),
        #     "title" : forms.TextInput(attrs={"class" : "form-control"}),
        #     "description" : forms.Textarea(attrs={"class" : "form-control"}),
        #     "price" : forms.NumberInput(attrs={"class" : "form-control"}),
        #     "image_url" : forms.URLInput(attrs={"class" : "form-control"}),
        #     "slug": forms.TextInput(attrs={"class": "form-control"}),
        #     "tags" : forms.SelectMultiple(attrs={"class" : "form-control"})

        # }

    
