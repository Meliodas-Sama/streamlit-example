import re
import numpy as np
from nltk import ISRIStemmer, word_tokenize, PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords

def clean(text,lang = 'English'):
    """
    clean the text by:
    1. lowering the letter case
    2. replacing [@,;/(){}[]|] symbols with space
    3. removing anything but letters and spaces
    4. replacing white spaces by a single space
    5. removing spaces left at both ends of text
    """
    import re
    if lang.lower() == 'english':
        text = text.lower()
        text = re.sub(r'[@,;/(){}[]|]', ' ', text)
        text = re.sub(r'[^a-z\s]', '', text)
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        return text
    else:
        text = re.sub(r'[إأٱآا]','ا',text)
        text = re.sub(r'[ؤئ]','ء',text)
        text = re.sub('ة','ه',text)
        text = re.sub(r'[@,;/(){}[]|]', ' ', text)
        noise = re.compile("""   ّ    | # Tashdid
                                 َ    | # Fatha
                                 ً    | # Tanwin Fath
                                 ُ    | # Damma
                                 ٌ    | # Tanwin Damm
                                 ِ    | # Kasra
                                 ٍ    | # Tanwin Kasr
                                 ْ    | # Sukun
                                 ـ   | # Tatwil/Kashida
                             """, re.VERBOSE)
        text = re.sub(noise, '', text)
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        return text

def getStopWordsAndStemmer(lang='English'):
    from nltk import ISRIStemmer, PorterStemmer, WordNetLemmatizer
    from nltk.corpus import stopwords
    
    if lang.lower() == 'english':
        stemmer = PorterStemmer()
        stop_words = set(stopwords.words(lang))
    
    elif lang.lower() == 'arabic':
        stemmer = ISRIStemmer()
        with open("Arabic_StopWords.txt", "r",encoding='utf-8') as Arabic_StopWords:
            stop_words = [line for line in Arabic_StopWords]
        stop_words = set(stop_words + stopwords.words(lang))
    return stemmer, stop_words

def stem_text(data,lang='English'):
    """
    1. Initialize Word Net Lemmatizer
    2. Get stop words and Stemmer for the given language
    3. Clean the documents and then tokenize them using split method
       then stem the documents and remove stop words and the words that have 1 character (letter)
    """
    from nltk import WordNetLemmatizer
        
    wnl = WordNetLemmatizer()
    
    stemmer, stop_words = getStopWordsAndStemmer(lang)
    
    stemmed_cleaned = []
    for document in data:
        stemmed_cleaned.append([ wnl.lemmatize(stemmer.stem(w)) for w in clean(document,lang).split() if not w in stop_words and len(w)>1])
    if len(data) == 1:
        return stemmed_cleaned[0]
    return stemmed_cleaned


def unique_terms(documents):
    """
    Getting unique words from the documents to calculate the TF-IDF
    """
    unique_words = []
    for doc in documents:
        for w in doc:
            unique_words.append(w)
    unique_words = list(set(unique_words))
    unique_words.sort()
    return unique_words

