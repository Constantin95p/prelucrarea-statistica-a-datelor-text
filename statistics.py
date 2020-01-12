import nltk
import re
import string


from nltk.corpus import stopwords
stopwords.words('english')

def statistics_corpus_txt():
    # citirea textului din fisier
    with open('corpus-jo.txt', 'r', encoding="utf-8") as f:
        text_articol = f.read()

    # curatarea textului - stergerea caracterelor speciale si spatiilor
    text_articol = re.sub(r'\[[0-9]*\]', ' ', text_articol)
    text_articol = re.sub(r'\s+', ' ', text_articol)

    # impartim textul in cuvinte si propozitii, ca sa putem compara cu input-ul user-ului
    sentences = nltk.sent_tokenize(text_articol)

    wnlemmatizer = nltk.stem.WordNetLemmatizer()

    def perform_lemmatization(tokens):
        lemm_tokens = []
        for token in tokens:
            lemm_tokens.append(wnlemmatizer.lemmatize(token))
        return lemm_tokens

    punctuation_removal = dict((ord(punctuation), None) for punctuation in string.punctuation)

    tokens = perform_lemmatization(nltk.word_tokenize(text_articol.lower().translate(punctuation_removal)))

    from nltk.probability import FreqDist
    wubFD = FreqDist(word for word in tokens)
    wubFD.plot(50)

    clean_tokens = tokens[:]
    for token in set(tokens):
        if token in stopwords.words('english'):
            # clean_tokens.remove(token)
            while token in clean_tokens: clean_tokens.remove(token)
            print('Removed token', token)
    freq = FreqDist(clean_tokens)
    freq.plot(50)


statistics_corpus_txt()
