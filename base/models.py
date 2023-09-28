from django.db import models

# Create your models here.
class Dataset(models.Model):
  title = models.CharField(max_length=200)
  overview = models.TextField()
  file = models.FileField(upload_to="uploads/")
  
  def __str__(self):
    return str(self.title)