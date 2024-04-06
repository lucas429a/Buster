from django.db import models


class Rating_choices(models.TextChoices):
    G = "G"
    PG = "PG"
    PG_13 = "PG-13"
    R = "R"
    NC_17 = "NC-17"


class Movie(models.Model):
    title = models.CharField(max_length=127)
    duration = models.CharField(max_length=10, blank=True, default="")
    rating = models.CharField(
        max_length=20, choices=Rating_choices, default=Rating_choices.G
    )
    synopsis = models.TextField(blank=True, default="")
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="movies"
    )
