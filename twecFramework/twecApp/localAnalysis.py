from django.views import View
from django.shortcuts import render
from gensim.models.word2vec import Word2Vec
from cade.metrics.comparative import lncs2, c_measure, get_neighbors_set
from .forms import WordForm, WordNeighForm
from .models import Task

class CorrespondanceView(View):
    word_class = WordForm

    def get(self, request, num_task):
        word_form = self.word_class()
        task = Task.objects.get(pk=num_task)

        return render(request, 'correspondance.html', {
            'word_form': word_form,
            'task': task,
            })            

    def post(self, request, num_task):
        word_form = self.word_class()
        word = request.POST['word']
        words = [word, word.lower(), word.upper()]
        task = Task.objects.get(pk=num_task)

        models = [Word2Vec.load(model.model) for model in task.model_set.all()]

        results = [(c_measure(word, models), word) for word in words]
        return render(request, 'correspondance.html', {
            'results': results,
            'task': task,
            'word_form': word_form,
            })

class NeighborsView(View):
    word_class = WordNeighForm

    def get(self, request, num_task):
         word_form = self.word_class()
         task = Task.objects.get(pk=num_task)

         return render(request, 'neighbors.html', {
             'word_form': word_form,
             'task': task,
             })

    def post(self, request, num_task, topn=10):
        word_form = self.word_class()
        word = request.POST['word']
        topn = int(request.POST['topn'])
        task = Task.objects.get(pk=num_task)

        models = [Word2Vec.load(model.model) for model in task.model_set.all()]

        results = get_neighbors_set(word, models[0], topn)
        return render(request, 'neighbors.html', {
            'results': results,
            'word': word,
            'task': task,
            'word_form': word_form,
            })

class SimilarityView(View):
    word_class = WordNeighForm

    def get(self, request, num_task):
        word_form = self.word_class()
        task = Task.objects.get(pk=num_task)

        return render(request, 'similarity.html', {
            'word_form': word_form,
            'task': task,
            })

    def post(self, request, num_task):
        word_form = self.word_class()
        word = request.POST['word']
        topn = int(request.POST['topn'])
        task = Task.objects.get(pk=num_task)

        models = [Word2Vec.load(model.model) for model in task.model_set.all()]

        result = lncs2(word, models[0], models[1], topn)

        return render(request, 'similarity.html', {
            'result': result,
            'word_form': word_form,
            'task': task,
            })
