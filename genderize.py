import string

from gender_detector import GenderDetector


def predict_gender(name_phrase):
    detector = GenderDetector(country='us', unknown_value='')

    names = _strip_punctuation(name_phrase).split(' ')
    genders = [g for g in [detector.guess(name) for name in names] if g]

    if genders and all(gender == 'male' for gender in genders):
        return 'male'
    if any(gender == 'female' for gender in genders):
        return 'female'
    return ''


def _strip_punctuation(text):
    # assumes ASCII input
    return text.translate(string.maketrans('', ''), string.punctuation)
