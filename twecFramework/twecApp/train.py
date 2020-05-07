"""
    Package to train model with aligned_word_embedding
"""
from aligned_word_embeddings.aligned_word_embeddings import  AlignedWordEmbeddings
from aligned_word_embeddings.spatial.distances import most_similar_from_model
from cade.cade import CADE
from gensim.models.word2vec import Word2Vec
from background_task import background
from .models import Model, Document, Task
from .preprocessing import SimpleSpacyCleaner


def create_config_options(task):
    options = {}
    options['lemmatization'] = task.config.lemmatization
    options['digit_masking'] = task.config.digit_masking
    options['stemming'] = task.config.stemming
    options['lowercasing'] = task.config.lowercasing
    return options

@background(schedule=10)
def train(user_id):
    preproc = SimpleSpacyCleaner("en_core_web_sm")
    task = Task.objects.last()
    config = create_config_options(task)
    for document in task.document_set.all():
        with open(document.document.path, "r") as doc:
            contents = doc.read()
        with open("compass.txt", "w") as doc:
            doc.write(preproc.clean(contents, config))
    aligner = CADE(size=30, siter=10, diter=10, workers=4)

    merge_document(task)
    aligner.train_compass("compass.txt", overwrite=False)

    for document in task.document_set.all():
        slice_document = aligner.train_slice(document.document.path, save=True)
        path = "model/" + document.document.name[:-4] + ".model"
        task.model_set.create(model=path)

    task.status = True
    task.save()

def merge_document(task):
    contents = ""
    for document in task.document_set.all():
        with open(document.document.path, "r") as document_file:
            contents += document_file.read()
    file_merge = open("compass.txt", "w")
    file_merge.write(contents)
    file_merge.close()
