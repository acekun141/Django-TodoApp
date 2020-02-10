from django.db import models
from uuid import uuid4

class Todo(models.Model):
    """
    Todo Model
    """
    id = models.UUIDField(editable=False, primary_key=True, default=uuid4)
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=False)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
