import nltk
import random
import string
import re
import wikipedia

from nltk.tokenize import sent_tokenize

TOPIC = 'olympic games'
NR_INTREBARI = 5

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

    global questions
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
    qno = 0
    resp_map = {}
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
                try:
                    nr_responses = generate_responses(nr, value[index][0])
                    responses = []
                    for resp in range(len(nr_responses)):
                        responses.append(nr_responses[resp] + ' ' + ' '.join(value[index][1].split(' ')[1:]))
                except:
                    continue
            else:
                # sarim peste intrebarea aceasta daca nu se pot genera grilele
                continue

        # cream un dictionar cu fiecare intrebare de forma:
        #    a -> raspuns 1
        #    b -> raspuns 2
        #    c -> raspuns 3
        #    d -> raspuns 4
        #    QUESTION -> intrebarea
        #    CORRECT -> raspunsul corect
        resp_map[qno] = {}

        resp_map[qno]['QUESTION'] = q
        resp_map[qno]['CORRECT'] = value[index][1]
        resp_map[qno]['a'] = responses[0]
        resp_map[qno]['b'] = responses[1]
        resp_map[qno]['c'] = responses[2]
        resp_map[qno]['d'] = responses[3]

        qno += 1
        # daca s-a ajuns la nr maxim de intrebari, se opreste
        if qno == NR_INTREBARI:
            break

    return resp_map


#########################################
# Interfata grafica #####################
#########################################

'''
Vor fi 3 ferestre:
1. Intro: de aici se pot genera intrebari in functie de un topic introdus
2. Intrebari: afisarea intrebarilor grila
3. Final: afisarea scorului si posibilitatea de a genera un alt set de intrebari pentru un alt topic
'''

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.clock import Clock

class WindowManager(ScreenManager):
    intro = ObjectProperty(None)
    intrebari = ObjectProperty(None)

class Intro(Screen):
    '''
    Fereastra de introducere, care contine:
    - mesajul de introducere al botului
    - input-ul de introdus topicul pentru care sa fie generate intrebarile
    - butonul care genereaza intrebarile
    '''
    
    bot = ObjectProperty(None)

    def generate(self):
        '''
        Genereaza setul de intrebari, in functie de topicul ales de utilizator
        '''
        topic = Intro.current = self.topic.text
        try:
            found_sentences = get_wiki_page(TOPIC + ' ' + topic)
            questions = generate_questions_for(found_sentences)
        except Exception as e:
            # in caz ca apare o eroare in timpul generarii intrebarilor, afiseaza un mesaj si ramane pe aceeasi fereastra
            print(e)
            self.bot.text = 'JO: Sorry! I found nothing about ' + topic + '. Please try something else.'
        else:
            # daca intrebarile au fost generate corect, se trece la fereastra urmatoare, care le afiseaza
            sm.current = 'intrebari'

class Intrebari(Screen):
    '''
    Fereastra cu intrebarile, care contine:
    - intrebarea
    - grilele (a, b, c, d)
    - un buton de finalizare imediata a testului
    '''

    question = ObjectProperty(None)
    ans1 = ObjectProperty(None)
    ans2 = ObjectProperty(None)
    ans3 = ObjectProperty(None)
    ans4 = ObjectProperty(None)
    questions = ObjectProperty(None)

    def on_enter(self, *args):
        '''
        Prima data cand se intra pe aceasta fereastra, se genereaza dictionarul cu intrebarile si raspunsurile grila
        '''
        self.resp_map = display_questions(questions)

        self.question.text = 'Q1/' + str(len(self.resp_map)) + ' - ' + self.resp_map[0]['QUESTION']
        self.ans1.text = self.resp_map[0]['a']
        self.ans2.text = self.resp_map[0]['b']
        self.ans3.text = self.resp_map[0]['c']
        self.ans4.text = self.resp_map[0]['d']
        self.last_question = 0
        
        global right_answers
        right_answers = 0
        global len_questions
        len_questions = len(self.resp_map)

    def answer(self, ans):
        '''
        Fiecare buton cu raspunsurile grila (a, b, c, d) apeleaza functia aceasta care:
        1. verifica raspunsul
        2. afiseaza intrebarea urmatoare
        '''
        if self.resp_map[self.last_question][ans] == self.resp_map[self.last_question]['CORRECT']:
            # daca raspunsul este corect, se adauga la numaratoarea raspunsurilor corecte, pentru a fi afisate la final
            global right_answers
            right_answers += 1

        self.last_question += 1
        if self.last_question == len(self.resp_map):
            # daca s-a ajuns la ultima intrebare, se trece la urmatoarea fereastra, numita "final"
            sm.current = 'final'
        else:
            # daca nu s-a ajuns la ultima intrebare, toate campurile sunt populate cu detaliile intrebarii urmatoare
            self.question.text = 'Q' + str(self.last_question+1) + '/' + str(len(self.resp_map)) + ' - ' + self.resp_map[self.last_question]['QUESTION']
            self.ans1.text = self.resp_map[self.last_question]['a']
            self.ans2.text = self.resp_map[self.last_question]['b']
            self.ans3.text = self.resp_map[self.last_question]['c']
            self.ans4.text = self.resp_map[self.last_question]['d']

    def finish_test(self):
        '''
        Functie apelata la apasarea butonului "Finish test"
        Finalizeaza testul oricand, indiferent de intrebarea la care s-a ajuns, si trece la urmatoarea fereastra care arata scorul
        '''
        global len_questions
        len_questions = self.last_question
        sm.current = 'final'

class Final(Screen):
    '''
    Fereastra finala care arata:
    - Scorul
    - Posibilitatea de a genera un alt set de intrebari pentru un nou topic
    '''
    
    bot = ObjectProperty(None)

    def on_pre_enter(self, *args):
        '''
        Functie apelata inainte de a fi afisata fereastra "final", pentru a calcula scorul si a sti ultimul topic introdus
        '''
        # extragerea ultimului topic introdus
        self.last_topic = sm.screens[0].ids.topic.text
        if self.last_topic == '':
            try:
                self.last_topic = sm.screens[2].ids.topic.text
            except:
                self.last_topic = TOPIC
        
        # calcularea scorului
        global right_answers, len_questions
        if len_questions != 0:
            ratio = (right_answers * 100) / len_questions
        else:
            ratio = 0
        self.scor.text = 'JO: You answered to {} of {} questions. Your ratio is {}'.format(right_answers, len_questions, ratio)

    def generate(self):
        '''
        Genereaza setul de intrebari, in functie de topicul ales de utilizator
        '''
        topic = Intro.current = self.topic.text
        try:
            found_sentences = get_wiki_page(TOPIC + ' ' + topic)
            questions = generate_questions_for(found_sentences)
        except Exception as e:
            # in caz ca apare o eroare in timpul generarii intrebarilor, afiseaza un mesaj si ramane pe aceeasi fereastra
            print(e)
            self.scor.text = 'JO: Sorry! I found nothing about ' + topic + '. Please try something else.'
        else:
            # daca intrebarile au fost generate corect, se trece la fereastra urmatoare, care le afiseaza
            sm.current = 'intrebari'
    


# construieste interfata setata in fisierul "interfata.kv"
kv = Builder.load_file("interfata.kv")

sm = WindowManager()
# adauga in interfata cele 3 ferestre: Intro, Intrebari si Final
screens = [Intro(name='intro'), Intrebari(name='intrebari'), Final(name='final')]
for screen in screens:
    sm.add_widget(screen)

# seteaza prima pagina
sm.current = "intro"

class MyMainApp(App):
    def build(self):
        return sm

# variabile globale pentru a retine nr raspunsurilor corecte si nr intrebarilor
global right_answers
global len_questions

if __name__ == "__main__":
    MyMainApp().run()

