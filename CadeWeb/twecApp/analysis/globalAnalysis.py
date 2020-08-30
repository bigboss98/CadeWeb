from django.views import View
from django.shortcuts import render
from gensim.models.word2vec import Word2Vec
from cade.metrics.stability import jumpers, stables
from twecApp.forms import WordForm
from twecApp.models import Task
from .localAnalysis import calculate_comparable_models

class JumpersView(View):
    """
        JumpersView used to conduct an jumpers analysis
        :param word_class: Form Class used to collect data for analysis
    """
    word_class = WordForm

    def get(self, request, num_task):
        """
            Get function used to retrieve information useful for analysis
            :param request: request Object
            :param num_task: ID of task used
        """
        word_form = self.word_class()
        task = Task.objects.get(pk=num_task)
        comparable_models = calculate_comparable_models(task)

        return render(request, "jumpers.html", {
            'task': task,
            'word_form': word_form,
            'comparable_models': comparable_models,
            })

    def post(self, request, num_task):
        """
            Post function used to calculate top n Jumpers between two models chosen
            :param request: request Object
            :param num_task: ID of task used
        """
        word_form = self.word_class()
        task = Task.objects.get(pk=num_task)
        comparable_models = calculate_comparable_models(task)
        topn = int(request.POST['topn'])
        chosen_models_name = request.POST['modelChoice'].split("-")

        models = [Word2Vec.load(model.model) for model in task.model_set.all()
                                             for model_name in chosen_models_name
                                             if model.name == model_name]
        if len(models) == 2:
            top_jumpers = jumpers(models[0], models[1], topn)
        else:
            top_jumpers = []
        return render(request, "jumpers.html", {
            'task': task,
            'word_form': word_form,
            'comparable_models': comparable_models,
            'top_jumpers': top_jumpers,
            'topn': topn,
            'modelChoice': request.POST['modelChoice'],
            })

class StablesView(View):
    """
        StablesView is a View used to stables analysis
        :param word_class: Form object used to achieve information
    """
    word_class = WordForm

    def get(self, request, num_task):
        """
            Get function used to retrieve information for analysis
            :param request: request Object
            :param num_task: ID of task used
        """
        task = Task.objects.get(pk=num_task)
        word_form = self.word_class()
        comparable_models = calculate_comparable_models(task)
        return render(request, "stables.html", {
            'task': task,
            'word_form': word_form,
            'comparable_models': comparable_models,
            })

    def post(self, request, num_task):
        """
            Post function used to conduct an stables analysis
            :param request: request Object
            :param num_task: ID of task used
        """
        task = Task.objects.get(pk=num_task)
        word_form = self.word_class()
        comparable_models = calculate_comparable_models(task)
        topn = int(request.POST['topn'])
        chosen_models_name = request.POST['modelChoice'].split("-")

        models = [Word2Vec.load(model.model) for model in task.model_set.all()
                                             for model_name in chosen_models_name
                                             if model.name == model_name]

        if len(models) == 2:
            top_stables = stables(models[0], models[1], topn)
        else:
            top_stables = []
        return render(request, "stables.html", {
            'task': task,
            'word_form': word_form,
            'comparable_models': comparable_models,
            'top_stables': top_stables,
            'topn': topn,
            'modelChoice': request.POST['modelChoice'],
            })

