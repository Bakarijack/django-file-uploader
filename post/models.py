from django.db import models

# Create your models here.
class Post(models.Model):
    name = models.CharField(max_length=200, default="")
    fileUrl = models.FileField(upload_to="pdf")
    
    cover = models.ImageField(upload_to="cover", default="")
    
    def __str__(self) -> str:
        return self.name