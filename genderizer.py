import string

from genderize import Genderize
import nltk


def predict_gender(name_phrase):
    # note: without an API key, this API is limited to 1000 requests/day
    genderizer = Genderize(user_agent='GenderizeDocs/0.0', api_key='')

    names = nltk.word_tokenize(name_phrase)
    if not names:
        return ''

    genderized = genderizer.get(names)

    return _select_result_with_highest_count(genderized).get('gender', '')


def _select_result_with_highest_count(genderized):
    return sorted(genderized, key=lambda x: x.get('count'), reverse=True)[0]
