from django import forms
from django.forms import modelformset_factory
from .models import Document


class DocumentModelForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['document_path', ]
        widgets = {
                'document_path': forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Select Document File here'
                    })
                }
        labels = {
                'document_path': 'Select Document file here'
            }
        
DocumentModelFormSet = modelformset_factory(Document, fields= ("document_path", ), extra = 2)
