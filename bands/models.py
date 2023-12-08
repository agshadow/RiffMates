from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver


class Musician(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth = models.DateField()

    def __str__(self):
        return f"Musician(id={self.id}, last_name={self.last_name})\n"

    class Meta:
        ordering = ["last_name", "first_name"]


class Venue(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return f"Venue(id={self.id}, name={self.name})"

    class Meta:
        ordering = [
            "name",
        ]


class Room(models.Model):
    name = models.CharField(max_length=20)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)

    def __str__(self):
        return f"Room(id={self.id}, name={self.name})"

    class Meta:
        ordering = [
            "name",
        ]


class Band(models.Model):
    name = models.CharField(max_length=20)
    musicians = models.ManyToManyField(Musician)

    def __str__(self):
        data = f"Band(id={self.id}, name={self.name}\n"
        for i in self.musicians.all():
            data += f"{i}"
        return data

    """
    class meta:
        unique_together = [["name","venue"]]
        # alternate short-cut version as there is only one "uniqueness"
        # unique_together = ["name", "venue"]"""

    class Meta:
        ordering = [
            "name",
        ]


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    musician_profiles = models.ManyToManyField(Musician, blank=True)
    venues_controlled = models.ManyToManyField(Venue, blank=True)


@receiver(post_save, sender=User)
def user_post_save(sender, **kwargs):
    # Create UserProfile object if User object is new
    # and not loaded from fixture
    print("called post_save")
    if kwargs["created"] and not kwargs["raw"]:
        user = kwargs["instance"]
        try:
            # Double check UserProfile doesn't exist already
            # (admin might create it before the signal fires)
            UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            # No UserProfile exists for this user, create one
            UserProfile.objects.create(user=user)
