"""
    Views used by twecApp done with Django
"""
from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from .models import Model, Configuration, Task
from .forms import ConfigModelForm, ModelModelFormSet, TaskModelFormSet, TaskModelForm
from .train import train


class TaskAdd(View):
    """
        TrainView class, used for select document file, configuration option and train a new model
        :attrib model_class: ModelModelForm  used to represent a Model form
        :attrib docu_class: DocumentModelFormSet used to represent a Document form
    """
    config_class = ConfigModelForm
    document_class = ModelModelFormSet
    task_class = TaskModelForm

    def get(self, request):
        """
            Get function used for retrieve basic page,
            to choose document file and configuration option
            :param self:current object of TrainView
            :param request: request file
        """
        docu_form = self.document_class(queryset=Model.objects.filter(task=0))
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
        config_form = self.config_class(request.POST)
        docu_form = self.document_class(request.POST, request.FILES)

        num_files = 0
        for doc in request.FILES:
            num_files = num_files + 1

        if docu_form.is_valid() and num_files >= 2:
            config_form.save()
            task = Task(config=Configuration.objects.last(), name_task=request.POST['name_task'])
            task.save()
            num_documents = 0
            for doc in request.FILES:
                task.model_set.create(document=request.FILES[doc],
                                      name=request.POST['form-' + str(num_documents) + "-name"])
                num_documents = num_documents + 1
            task.save()
            print("Len: ", len(task.model_set.all()))
            train(task.num_task)
        return HttpResponseRedirect('../', {})

class TaskView(View):
    """
        TaskView is a View class used for views task trained
    """

    def get(self, request):
        """
            Get function used for retrieve task trained
            :param self:current object of TaskView
            :param request: request file
        """
        task_objects = Task.objects.all()
        config = [calculate_config(task) for task in task_objects]
        return render(request, 'task.html', {
            'task_objects': task_objects,
            'config': config,
            })

class DetailsView(View):
    """
        AnalysisView is a View class used for views details of a task,
        used on understand purpose of task, configuration used
    """

    def get(self, request, num_task):
        """
            Get function used for retrieve details of a task
        """
        task_object = Task.objects.get(pk=num_task)
        for doc in task_object.model_set.all():
            config = calculate_config(task_object)
        return render(request, 'analysis.html', {
            'task': task_object,
            'config': config,
            })

def calculate_config(task):
    """
        Calculate config options used by a Task
        :param task: current object of TaskView
    """
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
    """
        TaskDelete is a View class used for delete a task
        :param model_class: indicate name of Form class used
    """
    model_class = TaskModelFormSet

    def get(self, request, num_task):
        """
            Get function that delete a Task
            :param num_task: indicate the id of task to delete
        """
        task = Task.objects.get(num_task=num_task)
        task.delete()
        return HttpResponseRedirect('../task', {})
