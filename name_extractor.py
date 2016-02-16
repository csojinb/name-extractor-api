import io

import nltk

nltk.download('words')
nltk.download('punkt')                       # tokenizer
nltk.download('averaged_perceptron_tagger')  # part-of-speech tagger
nltk.download('maxent_ne_chunker')           # named entity chunker
pos_tagger = nltk.tag.PerceptronTagger()


def extract_person_names(text):
    sentences = nltk.sent_tokenize(text)
    tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
    tagged_sentences = [pos_tagger.tag(sentence) for sentence in tokenized_sentences]
    chunked_sentences = nltk.ne_chunk_sents(tagged_sentences)

    return set(_flat_map(extract_person_names_from_tree(tree)
                         for tree in chunked_sentences))


def extract_person_names_from_tree(tree):
    names = []

    if hasattr(tree, 'label') and tree.label:
        if tree.label() == 'PERSON':
            names.append(' '.join([child[0] for child in tree]))
        else:
            for child in tree:
                names.extend(extract_person_names_from_tree(child))

    return names


def _flat_map(list_of_lists):
    return [item for sublist in list_of_lists for item in sublist]


if __name__ == '__main__':
    with io.open('sample.txt', 'r', encoding='utf-8') as f:
        sample = f.read()

    print extract_person_names(sample)
