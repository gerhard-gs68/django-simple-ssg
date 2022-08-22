from django.db import models
from django.conf import settings 
from django.contrib.auth import get_user_model


# Create your models here.
class FilledContactForm(models.Model):
    name = models.CharField(max_length=128)
    email = models.EmailField()
    subject = models.CharField(default='', max_length=128)
    message = models.TextField()
    message_saved = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}, {self.subject} ({self.email}) "


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f"files/users/user_{instance.user.id}/{filename}"

class Files(models.Model):
    file_name = models.CharField(max_length=128)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
    the_file = models.FileField(upload_to=user_directory_path, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now=True)


