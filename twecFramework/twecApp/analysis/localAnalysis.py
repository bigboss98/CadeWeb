from django.views import View
from django.shortcuts import render
from gensim.models.word2vec import Word2Vec
import numpy as np
from cade.metrics.comparative import lncs2, c_measure, get_neighbors_set
from twecApp.forms import WordForm
from twecApp.models import Task

class CorrespondanceView(View):
    """
        CorrespondanceView is a view used to represent correspondance of a word 
        in the other model
        :param word_class: string that indicate the form object used
    """
    word_class = WordForm

    def get(self, request, num_task):
        """
            Get function used to represent correspondance page where users choose
            word, topn and model to use to obtain correspondance word
            :param request: request Object 
            :param num_task: ID of task used, where there are models to use
        """
        task = Task.objects.get(pk=num_task)
        comparable_models = calculate_comparable_models(task)
        word_form = self.word_class()
        return render(request, 'correspondance.html', {
            'word_form': word_form,
            'task': task,
            'comparable_models': comparable_models,
            })            

    def post(self, request, num_task):
        """
            Post function used to calculate correspondance word 
            :param request: request Object
            :param num_task: ID of task used to conduct correspondance analysis
        """
        word_form = self.word_class()
        word = request.POST['word']
        topn = int(request.POST['topn'])
        task = Task.objects.get(pk=num_task)
        modelChoice = request.POST['modelChoice'].split("-")
        comparable_models = calculate_comparable_models(task)
        models = [Word2Vec.load(task.model_set.get(name=modelChoice[0]).model),
                  Word2Vec.load(task.model_set.get(name=modelChoice[1]).model)]
        if len(models) == 2: 
            result = [models[1].wv.most_similar(positive=[models[0].wv[word]], topn=topn)]
            results = [(correspondance, word, value) for res in result for correspondance, value in res]
        else:
            results = []
        return render(request, 'correspondance.html', {
            'results': results,
            'task': task,
            'word_form': word_form,
            'comparable_models': comparable_models,
            })

class NeighborsView(View):
    """
        NeighborsView used to conduct Neighbors analysis of a word
        :param word_class: form object to select word 
    """
    word_class = WordForm

    def get(self, request, num_task):
        """
            Get function used to present form choice of word, topn and model
            :param request: request Object
            :param num_task: ID of task used
        """
        word_form = self.word_class()
        task = Task.objects.get(pk=num_task)

        return render(request, 'neighbors.html', {
             'word_form': word_form,
             'task': task,
             })

    def post(self, request, num_task):
        """
            Post function used to conduct neighbors analysis of a word in a model
            :param request: request Object
            :param num_task: ID of task used
        """
        word_form = self.word_class()
        word = request.POST['word']
        topn = int(request.POST['topn'])
        modelName = request.POST['modelChoice']
        task = Task.objects.get(pk=num_task)

        models = [Word2Vec.load(task.model_set.get(name=modelChoice[0]).model),
                  Word2Vec.load(task.model_set.get(name=modelChoice[1]).model)]

        results = get_neighbors_set(word, models[0], topn)
        return render(request, 'neighbors.html', {
            'results': results,
            'word': word,
            'task': task,
            'word_form': word_form,
            })

class SimilarityView(View):
    """
        SimilarityView is a View used to conduct Similarity analysis 
        :param word_class: Form object used to choose
                           word, topn and models needed
    """
    word_class = WordForm

    def get(self, request, num_task):
        """
            Get function used to choose word, topn and models to use 
            :param request: request Object
            :param num_task: ID of task used
        """
        word_form = self.word_class()
        task = Task.objects.get(pk=num_task)
        comparable_models = calculate_comparable_models(task)
        return render(request, 'similarity.html', {
            'word_form': word_form,
            'task': task,
            'comparable_models': comparable_models,
            })

    def post(self, request, num_task):
        """
            Post function used to calculate similarity between models of a word
            :param request: request Object
            :param num_task: ID of task used
        """
        word_form = self.word_class()
        word = request.POST['word']
        topn = int(request.POST['topn'])
        task = Task.objects.get(pk=num_task)
        comparable_models = calculate_comparable_models(task)
        modelChoice = request.POST['modelChoice'].split("-")
        selected_models = [Word2Vec.load(task.model_set.get(name=modelChoice[0]).model),
                           Word2Vec.load(task.model_set.get(name=modelChoice[1]).model)]
        models = [Word2Vec.load(model.model) for model in task.model_set.all()]
        results = [(word, lncs2(word, selectedModels[0], selectedModels[1], topn), c_measure(word, models))]

        return render(request, 'similarity.html', {
            'results': results,
            'word_form': word_form,
            'task': task,
            'comparable_models': comparable_models,
            })

class AnalogiesView(View):
    """
        AnalogiesView is a view used to conduct analogies analysis
        :param word_class: Object used to retrieve word, model, topn
    """
    word_class = WordForm

    def get(self, request, num_task):
        """
            Get function to retrieve information mandatory in analogies analysis
            :param request: request Object
            :param num_task: ID of task used
        """
        word_form = self.word_class()
        task = Task.objects.get(pk=num_task)
        comparable_models = calculate_comparable_models(task)
        return render(request, 'analogies.html', {
            'word_form': word_form,
            'task': task,
            'comparable_models': comparable_models,
            })

    def post(self, request, num_task):
        """
            Post function to conduct analogies analysis in two models
            :param request: request Object
            :param num_task: ID of Task used
        """
        word_form = self.word_class()
        task = Task.objects.get(pk=num_task)
        comparable_models = calculate_comparable_models(task)
        word = request.POST['word']
        topn = int(request.POST['topn'])
        modelChoice = request.POST['modelChoice'].split("-")
        results = get_analogies(task, word, topn, modelChoice)
        return render(request, 'analogies.html', {
            'word_form': word_form,
            'task': task,
            'results': results,
            'comparable_models': comparable_models,
            })


def get_analogies(task, word, topn, modelChoice):
    models = [Word2Vec.load(task.model_set.get(name=modelChoice[0]).model),
              Word2Vec.load(task.model_set.get(name=modelChoice[1]).model)]
    neighbors = list(get_neighbors_set(word, models[0], topn))
    analogies = []
    if len(models) == 2:
        correspondance_words = models[1].wv.most_similar(positive=[models[0].wv[word]], topn=topn)
        for (word, value) in correspondance_words:
            try:
                analogies_word = models[1].wv.most_similar(positive=word, negative = neighbors, topn=topn)
            except:
                print("Word not in Dictionary")
            else:
                analogies.append((word, analogies_word))
    return analogies

def calculate_comparable_models(task):
    num_model = 0
    comparable_models = []
    for model1 in task.model_set.all():
        num_model = num_model + 1
        for model2 in task.model_set.all():
            comparable_models.append((model1, model2))
    return comparable_models
