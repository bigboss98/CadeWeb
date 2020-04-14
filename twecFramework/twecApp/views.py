"""
    Views used by twecApp done with Django
"""
from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse
from .models import Document, Configuration, Model, Task
from .forms import ConfigModelForm, DocumentModelFormSet, TaskModelFormSet
from .train import train


class TrainView(View):
    """
        TrainView class, used for select document file, configuration option and train a new model
        :attrib model_class: ModelModelForm  used to represent a Model form
        :attrib docu_class: DocumentModelFormSet used to represent a Document form
    """
    config_class = ConfigModelForm
    document_class = DocumentModelFormSet

    def get(self, request):
        """
            Get function used for retrieve basic page,
            to choose document file and configuration option
            :param self:current object of TrainView
            :param request: request file
        """
        docu_form = self.document_class(queryset = Document.objects.filter(task=Task.objects.last()))
        config_form = self.config_class()
        return render(request, 'index.html', {
            'config_form': config_form,
            'docu_form': docu_form,
            })

    def post(self, request):
        """
            Post function used for train a new model with document given and configuration choosen
            :param self:current object of TrainView
            :param request: request file
        """
        config_form = self.config_class(request.POST, request.FILES)
        docu_form = self.document_class(request.POST, request.FILES)
        config_form.save()
        task = Task(config = Configuration.objects.last())
        task.save()
        if docu_form.is_valid():
            for doc in request.FILES:
                task.document_set.create(document=request.FILES[doc])
                Model(task=Task.objects.last()).save()
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
        return render(request, 'task.html', {'task_objects': task_objects})

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


def add_document(request):
    if request.method == 'POST':
        task = Task.objects.last()
        task.document_set.create()
        docu_form = DocumentModelFormSet(queryset=Document.objects.filter(task=task))
        config_form = ConfigModelForm()
    return HttpResponseRedirect('../', {'docu_form': docu_form, 'config_form': config_form})


def remove_document(request):
    """
        Remove a Document from model database and model formset
        :param request file
        :return HttpResponse and redirect to ''
    """
    if request.method == 'POST':
        if Document.objects.count() > 0: 
            Document.objects.last().delete()
    formset = DocumentModelFormSet()
    return HttpResponseRedirect('../', {'formset': formset})
