from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from uuid import uuid4

# Create your models here.



class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=50, null=True)
    description = models.TextField(null=True) 
    image_url = models.ImageField(null=True, upload_to="profile/")
    resume_url = models.URLField(null=True)
    id = models.UUIDField(unique=True, primary_key=True, default=uuid4)

    def __str__(self):
        return f"{self.name}"
    
# def CreateProfile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(
#             user = instance,
#             name = instance.username
#         )
#     else:
#         profile = instance.profile
#         profile.name = f"{instance.first_name.title()} {instance.last_name.title()}"
#         profile.save()

# post_save.connect(CreateProfile, sender=User)



# def DeleteUser(sender, instance, **kwargs):

#     user = instance.user
#     if not user.is_staff:
#         user.delete()


# post_delete.connect(DeleteUser, sender=Profile)



