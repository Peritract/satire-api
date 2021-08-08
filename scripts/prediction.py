import pickle

from .text_processor import TextProcessor

with open('./models/vectoriser', 'rb') as file:
    vectoriser = pickle.load(file)

with open('./models/tree-model', 'rb') as file:
    tree_model = pickle.load(file)

with open('./models/svm-model', 'rb') as file:
    svm_model = pickle.load(file)


def predict(text, premium=False):

    X = vectoriser.transform([TextProcessor().clean_text(text)])

    if premium:
        return (['not satirical', 'satirical'][svm_model.predict(X)[0]],
                max(svm_model.predict_proba(X)[0]))

    else:
        return ['not satirical', 'satirical'][tree_model.predict(X)[0]]