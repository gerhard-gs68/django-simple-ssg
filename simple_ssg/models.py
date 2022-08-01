from django.db import models

# Create your models here.
class FilledContactForm(models.Model):
    name = models.CharField(max_length=128)
    email = models.EmailField()
    subject = models.CharField(default='', max_length=128)
    message = models.TextField()
    message_saved = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}, {self.subject} ({self.email}) "