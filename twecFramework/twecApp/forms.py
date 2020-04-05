"""
    Forms package to indicate forms object used in twecApp application
"""
from django import forms
from django.forms import modelformset_factory
from .models import Document, Configuration, Task

class ConfigModelForm(forms.ModelForm):
    """
        ConfigurationModelForm used to represent a Configuration object on a form
    """
    class Meta:
        model = Configuration
        fields = '__all__'

class DocumentModelForm(forms.ModelForm):
    """
        DocumentModelForm used to represent a single Document object on a form
    """
    class Meta:
        model = Document
        fields = ['document']

class TaskModelForm(forms.ModelForm):
    """
        TaskModelForm used to represent a single Task object on a form
    """
    class Meta:
        model = Task
        fields = '__all__'

#represent a formset of Document object
DocumentModelFormSet = modelformset_factory(Document, fields=("document", ), extra=2)
TaskModelFormSet = modelformset_factory(Task, fields=("num_task", "model"))
