import nltk
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
from nltk.collocations import BigramCollocationFinder 
from nltk.metrics import BigramAssocMeasures 
import numpy as np
from nltk.corpus import stopwords 
from nltk.collocations import TrigramCollocationFinder 
from nltk.metrics import TrigramAssocMeasures 
nltk.download('punkt')
from nltk.corpus import stopwords
from textblob import TextBlob
import networkx as nx
def trascender_summary(text):

    # Read String
    def read_article(text):
        text=text.rstrip()
        text = text.replace('\n', ' ').replace('\r', '')
        article = text.split(". ")
        # text=text.rstrip() # Eliminate \n
        # sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        # article = sentence_tokenizer.tokenize(text) #Token by sentence
        sentences = []

        pattern = r'''(?x)                 # set flag to allow verbose regexps
                (?:[A-Z]\.)+         # abbreviations, e.g. U.S.A.
                | \w+(?:-\w+)*       # words with optional internal hyphens
                | \$?\d+(?:\.\d+)?%? # currency and percentages, e.g. $12.40, 82%
                | \.\.\.             # ellipsis
                | [][.,;"'?():-_`]   # these are separate tokens; includes ], ['''
        

        for sentence in article:
            sentences.append(nltk.regexp_tokenize(sentence, pattern))
            # sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))
        # sentences.pop() 
        
        return sentences

    # Calculate the similarity
    def sentence_similarity(sent1, sent2, stopwords=None):
        if stopwords is None:
            stopwords = []
    
        sent1 = [w.lower() for w in sent1]
        sent2 = [w.lower() for w in sent2]
    
        all_words = list(set(sent1 + sent2))
    
        vector1 = [0] * len(all_words)
        vector2 = [0] * len(all_words)
    

        for w in sent1:
            if w in stopwords:
                continue
            vector1[all_words.index(w)] += 1
    
        for w in sent2:
            if w in stopwords:
                continue
            vector2[all_words.index(w)] += 1
    
        return 1 - cosine_distance(vector1, vector2)

    # Matrix of similarity
    def build_similarity_matrix(sentences, stop_words):
        similarity_matrix = np.zeros((len(sentences), len(sentences)))
    
        for idx1 in range(len(sentences)):
            for idx2 in range(len(sentences)):
                if idx1 == idx2: #ignore if both are same sentences
                    continue 
                similarity_matrix[idx1][idx2] = sentence_similarity(sentences[idx1], sentences[idx2], stop_words)

        return similarity_matrix

        ## Generate Summary
    def generate_summary(file_name, top_n=5):
        nltk.download("stopwords")
        stop_words = stopwords.words('english')
        summarize_text = []

        # Step 1 - Read text anc split it
        sentences =  read_article(file_name)

        # Step 2 - Generate Similary Martix across sentences
        sentence_similarity_martix = build_similarity_matrix(sentences, stop_words)

        # Step 3 - Rank sentences in similarity martix
        sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)
        scores = nx.pagerank(sentence_similarity_graph)

        # Step 4 - Sort the rank and pick top sentences
        ranked_sentence = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)    
        # print("Indexes of top ranked_sentence order are ", ranked_sentence)    

        # print("="*200)
        # print(len(ranked_sentence))


        for i in range(top_n):
            summarize_text.append(" ".join(ranked_sentence[i][1]))

        # Step 5 - Offcourse, output the summarize texr
        return "".join(summarize_text)

    # Linguistic Wealth
    def lin_wealth(texto):
        if len(texto)!=0:
            return len(set(texto))/len(texto)
        else:
            return 0

    summary=generate_summary(text, 1)


    pattern = r'''(?x)                 # set flag to allow verbose regexps
              (?:[A-Z]\.)+         # abbreviations, e.g. U.S.A.
              | \w+(?:-\w+)*       # words with optional internal hyphens
              | \$?\d+(?:\.\d+)?%? # currency and percentages, e.g. $12.40, 82%
              | \.\.\.             # ellipsis
              | [][.,;"'?():-_`]   # these are separate tokens; includes ], ['''
    token_text = nltk.regexp_tokenize(text, pattern)


    clean_tokens = token_text[:]
    
    for token in token_text:
    
        if token in stopwords.words('english'):
    
            clean_tokens.remove(token)
    biagram_collocation = BigramCollocationFinder.from_words(token_text) 
    biagram_collocation.nbest(BigramAssocMeasures.likelihood_ratio, 15)


    
    stopset = set(stopwords.words('english')) 
    filter_stops = lambda w: len(w) < 3 or w in stopset 
    
    biagram_collocation.apply_word_filter(filter_stops) 
    collocation_bigram = biagram_collocation.nbest(BigramAssocMeasures.likelihood_ratio, 15) 

    trigram_collocation = TrigramCollocationFinder.from_words(token_text) 
    trigram_collocation.apply_word_filter(filter_stops) 
    trigram_collocation.apply_freq_filter(1) 
    
    collocation_trigram = trigram_collocation.nbest(TrigramAssocMeasures.likelihood_ratio, 15)


    testimonial = TextBlob(text)
    sentiment = testimonial.sentiment.polarity

    return summary,(lin_wealth(text),lin_wealth(summary)),collocation_bigram,collocation_trigram,sentiment

def union_bigram(cb):
    if len(cb)==0:
        cb= [['Title','not'],['Title','not']]
    elif len(cb)==1:
        cb.append(['Title','not'])

    cb_1=[]
    cont=0
    for element in cb[1:]:
        cb_1.append(element[0]+' '+element[1])
        cont+=1
        if cont>2:
            break
    title = cb[0]
    title = title[0]+ ' '+title[1]
    return title.upper(), cb_1

def union_trigram(ct):
    if len(ct)==0:
        ct= [['Title','not','found'],['Title','not','found']]
    elif len(ct)==1:
        ct.append(['Title','not','found'])
    ct_1=[]
    cont=0

    for element in ct[1:]:
        ct_1.append(element[0]+' '+element[1]+ ' '+element[2])
        cont+=1
        if cont>2:
            break
    title = ct[0]
    title = title[0]+ ' '+title[1]+' '+title[2]  
    return title.upper(), ct_1

def sentiment(s):
    if s<-0.2:
        return "NEGATIVE"
    elif s>0.2:
        return "POSITIVE"
    else:
        return "NEUTRAL"