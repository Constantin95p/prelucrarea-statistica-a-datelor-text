import nltk
import random
import string
import re
import wikipedia

from nltk.tokenize import sent_tokenize

TOPIC = 'olympic games'

YEARS = ['1896', '1900', '1904', '1908', '1912', '1916', '1920', '1924', '1928', '1932', '1936', '1940', '1944', '1948', '1952', '1956', '1960', '1964', '1968', '1972', '1976', '1980', '1984', '1988', '1992', '1996', '2000', '2002', '2004', '2006', '2008', '2010', '2012', '2014', '2016', '2018', '2020', '2022']


########################
# Prelucrarea textului #
########################

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

def get_processed_text(document):
    return perform_lemmatization(nltk.word_tokenize(document.lower().translate(punctuation_removal)))

#########################################
# Extragerea Locatiilor #################
#########################################

import json

with open('locatii.json') as json_file:
    LOCATII = json.loads(json_file.read())

#########################################
# Interactiunea botului cu utilizatorul #
#########################################

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def generate_response_more_details(user_input):
    '''
    Functie folosita pentru a cauta mai multe detalii despre un topic
    '''
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
        return []

    sentences_list = []
    index = -2
    sent = sentences[similar_vector_values.argsort()[0][index]]
    while len(sentences_list) < 4:
        if user_input in sent:
            sentences_list.append(sent)
        index -= 1
        sent = sentences[similar_vector_values.argsort()[0][index]]

    if vector_matched == 0:
        robo_response = robo_response + "Nothing found"
        return []

    robo_response = robo_response + sentences[similar_sentence_number]
    return robo_response


#################################################

def get_wiki_page(context):
    '''
    Folosim libraria wikipedia pentru a extrage detalii despre un context. De aici vom genera intrebarile
    '''
    global wiki_text
    wiki_text = wikipedia.page(context)
    return wiki_text.content.encode('ascii', 'ignore')

def get_question_data(section):
    '''
    Tokenizarea si tag-uirea corpusului, pentru a putea extrage numerele si locatiile din text
    '''
    tokens = nltk.word_tokenize(section)
    tagged = nltk.pos_tag(tokens)
    grammar = """
              NUMBER: {<$>*<CD>+<NN>*}
              LOCATION: {<IN><NNP>+<,|IN><NNP>+}
              """

    chunker = nltk.RegexpParser(grammar)
    result = chunker.parse(tagged)
    return result

def generate_questions_for(sec):
    '''
    Tokenizarea si tag-uirea fiecarei fraze din corpus
    '''

    # Stergem toate parantezele din text, pentru a procesa mai usor
    _sec = "".join(re.split('\(', sec.decode("utf-8").replace(")", "("))[0::2])

    questions = {}
    # pentru fiecare fraza, o tokenizam si generam posibile intrebari
    # din fiecare fraza, cu ajutorul procesarii NLTK, scoatem numerele si locatiile, din care vom genera apoi intrebarile
    for sentence in sent_tokenize(_sec):
        # '==' se refera la titlurile sectiunilor din pagina de wikipedia si le vom elimina
        if "==" not in sentence:
            # tokenizare
            qdata = get_question_data(sentence)
            if len(qdata) >= 75 and len(qdata) <= 150:
                qdata = []
            # generarea intrebarii
            questions.update(create_questions(sentence, qdata))
    return questions


def create_questions(sentence, chunked):
    '''
    Generarea intrebarii pentru o anumita fraza, in functie de tokenizarea obtinuta.
    Fiecare numar si locatie sunt luate in calcul pentru a fi "sectiunea lipsa" din intrebare
    '''
    gaps = []
    for word in chunked:
        if type(word) != tuple:
            target = []
            for y in word:
                target.append(y[0])
            orig_phrase = " ".join(target)
            gaps.append((word.label(), orig_phrase, orig_phrase))

    # dictionar ce contine:
    #   cheie: fraza
    #   valoare: potentiale "sectiuni lipsa"
    questions = {}
    if len(gaps) >= 2 and len(gaps) == len(set(gaps)):
        gaps_filtered = [gap for gap in gaps if gap[0] == 'NUMBER' or gap[0] == 'LOCATION']
        questions[sentence] = gaps_filtered
    return questions

def choose_hidden(value):
    '''
    Din lista de potentiale "sectiuni lipsa", alegem una care va fi folosita pentru a crea intrebarea
    '''

    # Locatiile au prioritate pentru a ridica dificultatea intrebarilor
    # (altfel am avea teste cu multi ani si numere)
    for val_index in range(len(value)):
        if value[val_index][0] == 'LOCATION':
            return val_index
    return 0

def generate_responses(value, type, prefix=''):
    '''
    Generam lista de grile de raspunsuri
    '''

    # raspunsul corect trebuie mereu sa fie in lista
    response = [value]
    # daca raspsunul este un an, atunci vom selecta aleatoriu 3 ani diferiti in care s-au jucat JO si ii adaugam in lista de grile
    if type == 'NUMBER' and (1896 < int(value) < 2030):
        while len(response) < 4:
            wrong_resp = random.choice(YEARS)
            if wrong_resp not in response:
                response.append(wrong_resp)
    # daca raspunsul este o locatie, vom selecta aleatoriu 3 locatii diferite in care s-au jucat JO si le adaugam in lista de grile
    elif type == 'LOCATION':
        while len(response) < 4:
            wrong_resp = random.choice(list(LOCATII.keys()))
            if wrong_resp not in response:
                response.append(prefix + ' ' + wrong_resp + ' , ' + LOCATII[wrong_resp])
    # daca raspunsul este un numar oarecare, generam alte 3 numere apropiate de raspunsul corect si le adaugam in lista de grile
    elif type == 'NUMBER':
        response.append(str(int(value) + 5))
        response.append(str(int(value) - 5))
        response.append(str(int(value) + 10))

    # amestecam lista de grile inainte de a returna utilizatorului
    random.shuffle(response)
    return response

def display_questions(questions):
    # nr de raspunsuri corecte va fi 0 la inceput
    raspunsuri_corecte = 0
    # retine numarul intrebarii la care s-a ajuns
    qno = 1
    # parcurgem fiecare intrebare generata
    for key, value in questions.items():
        # daca nu exista posibile raspunsuri, sarim peste intrebare si trecem la urmatoarea fara sa afisam nimic
        if len(value) == 0:
            continue
        # alegem ce sectiune sa fie ascunsa din fraza initiala
        index = choose_hidden(value)
        # prefixul locatiilor: in, of, ... - pentru a genera raspunsurile gresite
        prefix = ''

        # sectiunea ascunsa din intrebare va fi stearsa si inlocuita cu semnul "?"
        if value[index][0] == 'LOCATION':
            # dupa tokenizare, locatiile sunt de forma "oras , tara" si ne trebuie de forma "oras, tara"
            v = value[index][1].replace(' , ', ', ')
            q = key.replace(v, '?')
            prefix = value[index][1].split(' ')[0]
        else:
            q = key.replace(value[index][1], '?')

        # generarea grilelor care vor fi folosite in intrebare
        try:
            responses = generate_responses(value[index][1], value[index][0], prefix)
        except ValueError:
            # in caz ca raspunsul contine numere si litere (ex. "20 gold") vom pastra acelasi patern si doar inlocuim numerele
            if re.match('^[0-9]+\w+', value[index][1]) and value[index][0] == 'NUMBER':
                nr = value[index][1].split(' ')[0]
                nr_responses = generate_responses(nr, value[index][0])
                responses = []
                for resp in range(len(nr_responses)):
                    responses.append(nr_responses[resp] + ' ' + ' '.join(value[index][1].split(' ')[1:]))
            else:
                # sarim peste intrebarea aceasta daca nu se pot genera grilele
                continue

        # cream un dictionar cu grilele de forma:
        #    a -> raspuns 1
        #    b -> raspuns 2
        #    c -> raspuns 3
        #    d -> raspuns 4
        resp_map = {}
        resp_map['a'] = responses[0]
        resp_map['b'] = responses[1]
        resp_map['c'] = responses[2]
        resp_map['d'] = responses[3]
        print('''Q{}/{} {}
        a. {}
        b. {}
        c. {}
        d. {} 
        '''.format(qno, len(questions), q, resp_map['a'], resp_map['b'], resp_map['c'], resp_map['d']))

        # asteptam raspunsul utilizatorului
        user_resp = input('> Your answer here (a, b, c, or d): ')
        while user_resp.lower() not in ['a', 'b', 'c', 'd', 'q']:
            # utilizatorul trebuie sa raspunda doar "a", "b", "c" sau "d", altfel va fi atentionat si nu va putea continua pana nu da un raspuns
            print('JO: Please answer with a, b, c, or d!')
            user_resp = input('> Your answer here (a, b, c, or d): ')
        # 'q' inseamna ca utilizatorul renunta sa mai raspunda
        if user_resp == 'q':
            break

        # verificarea raspunsului
        if resp_map[user_resp.lower()] == value[index][1]:
            print('JO: Correct!')
            raspunsuri_corecte += 1
        else:
            print('JO: Wrong! Correct answer is:', value[index][1])
        qno += 1

    print('JO: No more questions')
    return raspunsuri_corecte


continue_dialogue = True
print("Hello. I am JO. Write a topic to generate questions about Olympic Games.")
human_text = input()
human_text = human_text.lower()
while continue_dialogue == True:
    if human_text != 'bye':
        if human_text == 'thanks' or human_text == 'thank you very much' or human_text == 'thank you':
            continue_dialogue = False
            print("JO: Most welcome")
        else:
            print("JO: ", end="")
            try:
                found_sentences = get_wiki_page(TOPIC + ' ' + human_text)
                questions = generate_questions_for(found_sentences)
            except Exception as e:
                print('JO: Sorry! I found nothing about ' + human_text + '. Please try something else.')

            try:
                raspunsuri_corecte = display_questions(questions)
                # calculam cat la suta din raspunsuri au fost corecte
                ratio = (raspunsuri_corecte * 100) / len(questions)
                print('JO: You answered to {} of {} questions. Your ratio is {}'.format(raspunsuri_corecte, len(questions), ratio))
            except Exception as e:
                pass
            finally:
                print('JO: Write "more" to find out more details about {}. Or type another topic to generate another set of questions.\n>'.format(human_text))
                user_resp2 = input()
                if user_resp2.lower() == 'more':
                    print('JO: Ok. I am searching for more details about {}.'.format(human_text))
                    print(generate_response_more_details(human_text))
                    print('JO: Write a topic to generate questions')
                    human_text = input()
                    human_text = human_text.lower()
                else:
                    human_text = user_resp2.lower()
    else:
        continue_dialogue = False
        print("JO: Bye!")
