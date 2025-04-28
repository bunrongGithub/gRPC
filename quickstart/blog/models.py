from django.db import models


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Post(BaseModel):  # Inheriting from BaseModel
    title = models.TextField()
    content = models.TextField()

    class Meta:
        db_table = "blog"
        ordering = ["created"]

    def __str__(self):
        return f"{self.title}"

    def clean(self):
        if self.updated < self.created:
            print("Error !!!")
