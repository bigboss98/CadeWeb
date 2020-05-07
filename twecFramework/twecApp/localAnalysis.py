from django.views import View
from django.shortcuts import render
from gensim.models.word2vec import Word2Vec
from cade.metrics.stability import jumpers, stables
from .models import Task

class LocalView(View):

    def post(self, request, num_task):
        task = Task.objects.get(pk=num_task)
        
        model1 = Word2Vec.load(task.model_set.all()[0].model)
        model2 = Word2Vec.load(task.model_set.all()[1].model)

        top_jumpers = jumpers(model1, model2)
        top_stables = stables(model1, model2)

        return render(request, "local.html", {
            'top_jumpers': top_jumpers, 
            'top_stables': top_stables
            })


