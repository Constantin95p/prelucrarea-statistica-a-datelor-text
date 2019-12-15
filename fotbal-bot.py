import nltk
import numpy as np
import random
import string
import re

########################
# Prelucrarea textului #
########################
	
# citirea textului din fisier
with open('corpus.txt', 'r', encoding="utf-8") as f:
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

def get_processed_text(document):
    return perform_lemmatization(nltk.word_tokenize(document.lower().translate(punctuation_removal)))


#########################################
# Interactiunea botului cu utilizatorul #
#########################################

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def generate_response(user_input):
    robo_response = ''
    sentences.append(user_input)

    word_vectorizer = TfidfVectorizer(tokenizer=get_processed_text)
    all_word_vectors = word_vectorizer.fit_transform(sentences)
    similar_vector_values = cosine_similarity(all_word_vectors[-1], all_word_vectors)
    similar_sentence_number = similar_vector_values.argsort()[0][-2]

    matched_vector = similar_vector_values.flatten()
    matched_vector.sort()
    vector_matched = matched_vector[-2]

    if vector_matched == 0:
        robo_response = robo_response + "Nothing found"
        return robo_response
    else:
        robo_response = robo_response + sentences[similar_sentence_number]
        return robo_response


continue_dialogue = True
print("Hello. I am Messy. You can ask me any question about football")
while(continue_dialogue == True):
    human_text = input()
    human_text = human_text.lower()
    if human_text != 'bye':
        if human_text == 'thanks' or human_text == 'thank you very much' or human_text == 'thank you':
            continue_dialogue = False
            print("Messy: Most welcome")
        else:
            print("Messy: ", end="")
            print(generate_response(human_text))
            sentences.remove(human_text)
    else:
        continue_dialogue = False
        print("Messy: Bye!")
