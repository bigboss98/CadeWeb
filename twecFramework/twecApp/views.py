"""
    Views used by twecApp done with Django
"""
from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse
import os
from .models import Document, Configuration, Model, Task
from .forms import ConfigModelForm, DocumentModelFormSet, TaskModelFormSet, TaskModelForm
from .train import train
from twecFramework.settings import MEDIA_ROOT


class TrainView(View):
    """
        TrainView class, used for select document file, configuration option and train a new model
        :attrib model_class: ModelModelForm  used to represent a Model form
        :attrib docu_class: DocumentModelFormSet used to represent a Document form
    """
    config_class = ConfigModelForm
    document_class = DocumentModelFormSet
    task_class = TaskModelForm

    def get(self, request):
        """
            Get function used for retrieve basic page,
            to choose document file and configuration option
            :param self:current object of TrainView
            :param request: request file
        """
        docu_form = self.document_class(queryset = Document.objects.filter(task=0))
        config_form = self.config_class()
        task_form = self.task_class()

        return render(request, 'index.html', {
            'config_form': config_form,
            'docu_form': docu_form,
            'task_form': task_form,
            })

    def post(self, request):
        """
            Post function used for train a new model with document given and configuration choosen
            :param self:current object of TrainView
            :param request: request file
        """
        config_form = self.config_class(request.POST, request.FILES)
        docu_form = self.document_class(request.POST, request.FILES)

        num_files = 0
        for doc in request.FILES:
            num_files = num_files + 1

        if docu_form.is_valid() and num_files >= 2:
            config_form.save()
            task = Task(config = Configuration.objects.last(), name_task = request.POST['name_task'])
            task.save()
            for doc in request.FILES:
                task.document_set.create(document=request.FILES[doc])
            
            task.save()
            train(task.num_task)
        return HttpResponseRedirect('task', {})

class TaskView(View):
    """
        TaskView is a View class used for views task trained
        :param model_class: indicate name of Form class used
    """
    model_class = TaskModelFormSet

    def get(self, request):
        """
            Get function used for retrieve task trained
            :param self:current object of TaskView
            :param request: request file
        """
        task_objects = Task.objects.all()
        config = [calculateConfig(task) for task in task_objects]
        return render(request, 'task.html', {
            'task_objects': task_objects,
            'config': config,
            })

def calculateConfig(task):
    temp = []
    if task.config.lowercasing:
        temp.append('lowercasing')
    if task.config.stemming:
        temp.append('stemming')
    if task.config.digit_masking:
        temp.append('digit_masking')
    if task.config.lemmatization:
        temp.append('lemmatization')
    return temp

class TaskDelete(View):

    model_class = TaskModelFormSet

    def post(self, request, num_task):
        task_form = self.model_class(request.POST)
        task = Task.objects.get(num_task = num_task)
        task.delete()
        return HttpResponseRedirect('../task', {})


class TaskAdd(View):
    """
        TaskAdd is a View class used for create a new task
        :param model_class: indicate name of Form class used
    """
    model_class = TaskModelFormSet

    def post(self, request):
        return HttpResponseRedirect('../../', {})


