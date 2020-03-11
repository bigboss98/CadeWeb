from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import TaskModelForm
from twec.twec import TWEC
from gensim.models.word2vec import Word2Vec

# Create your views here.


def index(request):
    if request.method == 'POST':
        form = TaskModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            train(form)
            return HttpResponseRedirect('result.html')
    else:
        form = TaskModelForm()
    return render(request, 'index.html', {'form': form})    

def train(form):
    aligner = TWEC(size=30, siter=10, diter=10, workers=4)
    
    mergeDocument(form)
    aligner.train_compass("compass.txt", overwrite = False)

    slice_one = aligner.train_slice(form.field['document1'], save=True)
    slice_two = aligner.train_slice(form.field['document2'], save=True)

def result(form):
    return HttpResponse("Hello World")

def mergeDocument(form):
    f1 = open(form.field['document1'], "r")
    f1_contents = f1.read()
    f1.close()

    f2 = open(form.field['document2'], "r")
    f2_contents = f2.read()
    f2.close()

    f3 = open("compass.txt", "w")
    f3.write(f1_contents + f2_contents)
    f3.close()


    
