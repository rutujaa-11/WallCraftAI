from django.db import models


class GeneratedImage(models.Model):

    CATEGORY_CHOICES = [
        ('Mural', 'Mural'),
        ('Painting', 'Painting'),
        ('General', 'General'),
    ]

    prompt = models.TextField()

    image_url = models.URLField()

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return self.category + " - " + self.prompt[:30]