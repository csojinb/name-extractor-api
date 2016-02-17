import string

from genderize import Genderize
import nltk
import numpy as np

from utils import flatmap


def predict_genders(name_phrases):
    # note: without an API key, this API is limited to 1000 requests/day
    genderizer = Genderize(user_agent='GenderizeDocs/0.0', api_key='')

    tokenized = [nltk.word_tokenize(name_phrase) for name_phrase in name_phrases]
    index_pairs = _create_index_pairs(tokenized)

    genderized = genderizer.get(flatmap(tokenized))

    return _select_best_gender_predictions(name_phrases, index_pairs, genderized)


def _select_best_gender_predictions(name_phrases, index_pairs, genderized):
    genders = {}
    for name_phrase, (start, end) in zip(name_phrases, index_pairs):
        single_genderized = genderized[start:end]
        genders[name_phrase] = _select_result_with_highest_count(single_genderized)

    return genders


def predict_gender(name_phrase):
    # note: without an API key, this API is limited to 1000 requests/day
    genderizer = Genderize(user_agent='GenderizeDocs/0.0', api_key='')

    names = nltk.word_tokenize(name_phrase)
    if not names:
        return ''

    genderized = genderizer.get(names)

    return _select_result_with_highest_count(genderized).get('gender', '')


def _create_index_pairs(tokenized_names):
    lengths = [len(tokenized_name) for tokenized_name in tokenized_names]
    indicies = np.cumsum([0] + lengths)
    return zip(indices[:-1], indices[1:])


def _select_result_with_highest_count(genderized):
    return sorted(genderized, key=lambda x: x.get('count'), reverse=True)[0]
