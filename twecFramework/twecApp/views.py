from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files import File
from .forms import DocumentModelFormSet, DocumentModelForm
from .models import Document
from twec.twec import TWEC
from gensim.models.word2vec import Word2Vec

# Create your views here.

"""
  Associate 
"""
def index(request):
    if request.method == 'POST':
        formset = DocumentModelFormSet(request.POST, request.FILES)
        if formset.is_valid():
            for form in formset:
                form.save()
            train(formset)
            Document.objects.all().delete()#Reset Document queryset
            return HttpResponseRedirect('result.html')
    else:
        formset = DocumentModelFormSet()
    return render(request, 'index.html', {'formset': formset})    

def train(form):
    aligner = TWEC(size=30, siter=10, diter=10, workers=4)
    
    mergeDocument(form)
    aligner.train_compass("compass.txt", overwrite = False)

    for document in Document.objects.all():
        slice_document = aligner.train_slice(document.document_path.path, save = True)

def result(form):
    return HttpResponse("Hello World")

def mergeDocument(formset):
    contents = ""
    for document in Document.objects.all():
        with open(document.document_path.path, "r") as f:
            contents += f.read()
    file_merge = open("compass.txt", "w")
    file_merge.write(contents)
    file_merge.close()

def add_document(request):
    if request.method == 'POST':
        Document().save()
        formset = DocumentModelFormSet()
        return HttpResponseRedirect('../', {'formset': formset}) 
