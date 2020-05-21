from nltk.corpus import stopwords
import re
import nltk
nltk.download('stopwords')
nltk.download('punkt')
stop_words_nltk = set(stopwords.words('english'))


def raw2parr(raw, voc_rich=70):
    raw = raw.replace("?", ".")
    raw = raw.replace("!", ".")
    tokens = nltk.word_tokenize(raw)
    tokens = [w for w in tokens if len(w) > 1]
    tokens = [re.sub(r'[^A-Za-z0-9]+', '', w) for w in tokens]
    tokens = [w for w in tokens if w.lower() not in stop_words_nltk]
    tokens = [w for w in tokens if w.isalpha()]
    text_splitted = raw.split()
    current_list = []
    cont = 0
    final_text = ""
    for word in text_splitted:
        final_text = final_text + " " + word
        word_clean = word.replace(".", "")
        if word_clean in tokens:
            if word_clean not in current_list:
                cont += 1
                current_list.append(word)
                if ((cont > voc_rich) & ("." in word)):
                    final_text = final_text + "<stop*mark>"
                    cont = 0
                    current_list = []

    return final_text.split("<stop*mark>")
