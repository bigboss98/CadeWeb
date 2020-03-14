from django.db import models

# Create your models here.
class Document(models.Model):
    document_path = models.FileField(null = True)
#    name_document = models.CharField(max_length = 100)

    def __str__(self):
        return "Document : % ", document_path




   

