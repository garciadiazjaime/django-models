import nltk

nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")


def remove_location(value):
    words = nltk.tokenize.word_tokenize(value)
    tag = nltk.pos_tag(words)

    prepositions = [
        i for i, x in enumerate(tag) if x[1] == "IN" and x[0].lower() == "at"
    ]

    if len(prepositions):
        index = prepositions[0]
        words = [x[0] for i, x in enumerate(tag) if i < index]

        return " ".join(words)

    return value


def split_performers(value):
    values = value.split(",")
    if len(values) < 2:
        return values

    performers = values[0:-1]

    words = nltk.tokenize.word_tokenize(values[-1])
    tag = nltk.pos_tag(words)

    if tag[0][1] == "CC":
        words = [x[0] for i, x in enumerate(tag) if i > 0]
        performers.append(" ".join(words))

    return performers


def get_performer(value):
    without_location = remove_location(value)

    performers = split_performers(without_location)

    return performers
