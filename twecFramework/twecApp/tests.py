from twecApp.preprocessing import SimpleSpacyCleaner
from django.test import TestCase
from .models import Document

# Create your tests here.
class PreprocessingTestCase(TestCase):
    """
        PreprocessingTestCase is a preprocessing test case done using django testcase
    """
    def setUp(self):
        spacy = SimpleSpacyCleaner("en_core_web_sm")

    def test_no_preprocessing(self):
        config = {
                'lowercasing': False,
                'stemming': False,
                'digit_masking': False,
                'lemmatization': False
                }
        for name_file in ['file1.txt', 'file2.txt']:
            with open("Tests/Preprocessing/NoPreprocessing/" + name_file, "r") as doc:
                contents = doc.read()
                text = self.spacy.clean(contents, config)
                self.assertEqual(contents, text)

    def test_preprocessing_lower(self):
        config = {
                'lowercasing': True,
                'stemming': False,
                'lemmatization': False,
                'digit_masking': False
                }
        for name_file in ['file1.txt', 'file2.txt']:
            with open("Tests/Preprocessing/LowerPreprocessing/" + name_file, "r") as doc:
                contents = doc.read()
                text = self.spacy.clean(contents, config)
                self.assertEqual(contents, text)

    def test_preprocessing_stemming(self):
        config = {
                'lowercasing': False,
                'stemming': True,
                'lemmatization': False,
                'digit_masking': False
                }
        for name_file in ['file1.txt', 'file2.txt']:
            with open("Tests/Preprocessing/StemmingPreprocessing/" + name_file, "r") as doc:
                contents = doc.read()
                text = spacy.clean(contents, config)
                self.assertEqual(contents, text)

    def test_preprocessing_lemmatization(self):
        config = {
                'lowercasing': False,
                'stemming': False,
                'lemmatization': True,
                'digit_masking': False
                }
        for name_file in ['file1.txt', 'file2.txt']:
            with open("Tests/Preprocessing/LemmaPreprocessing/" + name_file, "r") as doc:
                contents = doc.read()
                text = spacy.clean(contents, config)
                self.assertEqual(contents, text)

    def test_preprocessing_digit_masking(self):
        config = {
                'lowercasing': False,
                'stemming': False,
                'lemmatization': False,
                'digit_masking': True
                }
        for name_file in ['file1.txt', 'file2.txt']:
            with open("Tests/Preprocessing/DigitPreprocessing/" + name_file, "r") as doc:
                contents = doc.read()
                text = spacy.clean(contents, config)
                self.assertEqual(contents, text)

    def complete_preprocessing(self):
        config = {
                'lowercasing': True,
                'stemming': True,
                'lemmatization': True,
                'digit_masking': True
                }
        for name_file in ['file1.txt', 'file2.txt']:
            with open("Tests/Preprocessing/CompletePreprocessing/" + name_file) as doc:
                contents = doc.read()
                texts = spacy.clean(contents, config)
                self.assertEqual(contents, texts)


