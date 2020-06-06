"""
    Forms package to indicate forms object used in twecApp application
"""
from django import forms
from django.forms import modelformset_factory
from .models import Model, Configuration, Task

class ConfigModelForm(forms.ModelForm):
    """
        ConfigurationModelForm used to represent a Configuration object on a form
    """
    class Meta:
        model = Configuration
        fields = '__all__'

class ModelModelForm(forms.ModelForm):
    """
        ModelModelForm used to represent a single Model object on a form
    """
    class Meta:
        model = Model
        fields = ['name', 'document']

class TaskModelForm(forms.ModelForm):
    """
        TaskModelForm used to represent a single Task object on a form
    """
    class Meta:
        model = Task
        fields = 'name_task',

class WordForm(forms.Form):
    word = forms.CharField(max_length=200)
    topn = forms.IntegerField()

#represent a formset of Document object
ModelModelFormSet = modelformset_factory(Model, fields=("name", "document"), extra=2)
TaskModelFormSet = modelformset_factory(Task, fields=("name_task", "status"))
