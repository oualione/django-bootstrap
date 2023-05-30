from users.models import Profile
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete





def CreateProfile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance,
            name=instance.username
        )
    else:
        profile = instance.profile
        profile.name = f"{instance.first_name.title()} {instance.last_name.title()}"
        profile.save()


post_save.connect(CreateProfile, sender=User)


def DeleteUser(sender, instance, **kwargs):

    user = instance.user
    if not user.is_staff:
        user.delete()


post_delete.connect(DeleteUser, sender=Profile)
