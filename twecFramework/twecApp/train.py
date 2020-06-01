"""
    Package to train model with aligned_word_embedding
"""
from cade.cade import CADE
from background_task import background
from .models import Task
from .preprocessing import SimpleSpacyCleaner


def create_config_options(task):
    """
        Create an dictionary with all config options to use in Preprocessing phase
        :param task: current Task object
    """
    options = {}
    options['lemmatization'] = task.config.lemmatization
    options['digit_masking'] = task.config.digit_masking
    options['stemming'] = task.config.stemming
    options['lowercasing'] = task.config.lowercasing
    return options

@background(schedule=10)
def train(task_id):
    """
        Train new Task with a preprocessing phase and using CADE
        :param task_id: ID of Task to train
    """
    preproc = SimpleSpacyCleaner("en_core_web_sm")
    task = Task.objects.last()
    config = create_config_options(task)
    for document in task.document_set.all():
        print("A")
        with open(document.document.path, "r") as doc:
            contents = doc.read()
        with open("compass.txt", "w") as doc:
            doc.write(preproc.clean(contents, config))
    print("D")
    aligner = CADE(size=30, siter=10, diter=10, workers=4)

    merge_document(task)
    aligner.train_compass("compass.txt", overwrite=False)

    for document in task.document_set.all():
        aligner.train_slice(document.document.path, save=True)
        path = "model/" + document.document.name + ".model"
        task.model_set.create(model=path)

    task.status = True
    task.save()

def merge_document(task):
    """
        Merge documents to create the compass document(concatenation of all document)
        :param task: current Task object
    """
    contents = ""
    for document in task.document_set.all():
        with open(document.document.path, "r") as document_file:
            contents += document_file.read()
    file_merge = open("compass.txt", "w")
    file_merge.write(contents)
    file_merge.close()
