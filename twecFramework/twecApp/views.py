"""
    Views used by twecApp done with Django
"""
from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from background_task import background
from twec.twec import TWEC
from .models import Document, Configuration, Model
from .forms import ConfigModelForm, DocumentModelFormSet
from .preprocessing import SimpleSpacyCleaner


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
        docu_form = self.document_class()
        config_form = self.config_class()
        return render(request, 'index.html', {
            'config_form': config_form,
            'docu_form': docu_form,
            'config_options': ['lowercasing', 'lemmatization', 'stemming', 'digit_masking']})

    def post(self, request):
        """
            Post function used for train a new model with document given and configuration choosen
            :param self:current object of TrainView
            :param request: request file
        """
        config_form = self.config_class(request.POST, request.FILES)
        docu_form = self.document_class(request.POST, request.FILES)
        config_form.save()
        model = Model(config=Configuration.objects.last())
        model.save()
        if docu_form.is_valid():
            for doc in request.FILES:
                model.document_set.create(document=request.FILES[doc])
            model.save()
        train(1)
        Document.objects.all().delete()
        return render(request, 'result.html', {'formset': docu_form})

def TaskView(View):
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
        task_form = self.model_class()
        return render(request, 'task.html', {'task_form': task_form})

def TaskDelete(View):
    model_class = TaskModelFormSet

    def post(self, request):
        task_form = self.model_class(request.POST)

def TaskAdd(View):
    """
        TaskAdd is a View class used for create a new task
        :param model_class: indicate name of Form class used
    """
    model_class = TaskModelFormSet

    def post(self, request):
        task_form = self.model_class(request.POST)
        return render(request, 'index.html', {})

def create_config_options(model):
    options = {}
    options['lemmatization'] = model.config.lemmatization
    options['digit_masking'] = model.config.digit_masking
    options['stemming'] = model.config.stemming
    options['lowercasing'] = model.config.lowercasing
    return options

@background(schedule=10)
def train(user_id):
    preproc = SimpleSpacyCleaner("en_core_web_sm")
    model = Model.objects.last()
    config = create_config_options(model)
    for document in model.document_set.all():
        with open(document.document.path, "r") as doc:
            contents = doc.read()
        with open("compass.txt", "w") as doc:
            doc.write(contents)
            doc.write(preproc.clean(contents, config))
    aligner = TWEC(size=30, siter=10, diter=10, workers=4)

    merge_document(model)
    aligner.train_compass("compass.txt", overwrite=False)

    for document in model.document_set.all():
        slice_document = aligner.train_slice(document.document.path, save=True)


def merge_document(model):
    contents = ""
    for document in model.document_set.all():
        with open(document.document.path, "r") as document_file:
            contents += document_file.read()
    file_merge = open("compass.txt", "w")
    file_merge.write(contents)
    file_merge.close()

def add_document(request):
    if request.method == 'POST':
        config = Configuration()
        config.save()
        model = Model(config = config)
        model.save()
        Document(model=model).save()
        docu_form = DocumentModelFormSet()
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
