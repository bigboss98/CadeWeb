"""
    Models used in TwecApp application
"""
from django.db import models

class Configuration(models.Model):
    """
        Configuration class to set which preprocessing operations has to do

        Parameters:
            lowercasing: a boolean that set if we have to transform each word in a lowercase word
            lemmatization: a boolean that set if we have to do a lemmation process
            stemming: a boolean field to choose if we have to do a stemming processing
            digit_masking: a boolean field to decide if we have to do a digit masking or not
    """
    lowercasing = models.BooleanField(default=False)
    lemmatization = models.BooleanField(default=False)
    stemming = models.BooleanField(default=False)
    digit_masking = models.BooleanField(default=False)

class Task(models.Model):
    """
        Task class used to represent a single task trained by CADE,
        which contains one or more model trained
        :param num_task: used to represent number of task
        :param name_task: indicate a description name of task
        :param config: configuration used in the model
        :param status: indicate status of Model(whether or not was trained)
    """
    num_task = models.AutoField(primary_key=True, unique=True)
    name_task = models.CharField(default="New Task", max_length=200)
    config = models.OneToOneField(Configuration, on_delete=models.CASCADE, db_column='config')
    status = models.BooleanField(default=False)

class Model(models.Model):
    """
        Model class to represent a model trained with CADE

        Parameters:
        :param task: indicate number of Task, used to recognize a model in database
        :param model: path to model file trained by CADE
    """
    task = models.ForeignKey(Task, on_delete=models.CASCADE, to_field='num_task', default=0)
    name = models.CharField(default="New Model", max_length=200)
    model = models.FilePathField()

class Document(models.Model):
    """
        Document Class to rappresent Document element, used to train CADE model

        Parameters:
        :param document: a FileField used to rappresent document file
        :param task: reference to Task Class
    """
    document = models.FileField(blank=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, default=0, to_field='num_task')

    def __str__(self):
        if self.document:
            return "Name document: %", self.document
        return "Empty document"
