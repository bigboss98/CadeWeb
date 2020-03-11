from django.db import models

# Create your models here.
class Document(models.Model):
    document = models.FileField()
    name_document = models.CharField(max_length = 100)

    def __str__(self):
        return "Document : % saved on %", name_document, document


class Task(models.Model):
    documents = models.ForeignKey(Document, on_delete = models.CASCADE)
    time_required = models.TimeField()

    def __str__(self):
        return "Twec training was done in % seconds" % time_required


   

