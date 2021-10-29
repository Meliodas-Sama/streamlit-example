from utils import *

def Bool_Model (unique_words, documents):
    """
    Builds a dictionary for terms, mapping each term with a list of the documents it's in
    """
    import numpy as np
    model = {}
    for t in unique_words:
        model[t] = []
        for doc in range(len(documents)):
            if t in np.unique(documents[doc]):
                model[t].append(doc)
    return model

def Bool_Model_t (unique_words, documents):
    """
    Builds a dictionary for documents, mapping each document with a list of its terms
    """
    import numpy as np
    model = {}
    for doc in range(len(documents)):
        model[doc]= list(np.unique(documents[doc]))
    return model

def query_preprocess(query,lang = 'English'):
    from nltk import WordNetLemmatizer

    wnl = WordNetLemmatizer()

    stemmer, stop_words  = getStopWordsAndStemmer(lang)
    stop_words = [w for w in stop_words if not w in ['and','or','not']]
    
    st_query = [wnl.lemmatize(stemmer.stem(w)) for w in clean(query,lang).split() if not w in stop_words and len(w)>1]
    return st_query

def bool_sim (query, BModel):
    """
    Calculate the similarity between the query and each of the documents:
    1. for every term in query that is not in [not, and, or] check if term in document
    2. put True or False in place of the term in the query
    3. repeat for all documents
    return the result
    """
    result = []
    for doc in BModel:
        temp = ''
        for t in query:
            if t in ['not', 'and', 'or']:
                temp += ' ' + t
            elif t in BModel[doc]:
                temp += ' True'
            else:
                temp += ' False'
        res = eval(temp)
        result.append(res)
    return result

def print_docs(query,ans,lang):
    from nltk import WordNetLemmatizer

    wnl = WordNetLemmatizer()
    stemmer ,_ = getStopWordsAndStemmer()

    output = []
    stemmed_ans =  [(wnl.lemmatize(stemmer.stem(clean(term,lang))),term) for term in ans.split()]
    for term in stemmed_ans:
        if term[0] in query and not term[0] in ['not', 'and', 'or']:
            output.append('`'+term[1]+'`')
        else:
            output.append(term[1])
    output_text = ' '.join(output)
    pre_text = 'Accepted answer:  '
    return pre_text, output_text

@st.cache
def model(dataFrame,query,lang='English'):
    _, ans, data = get_data(dataFrame)
    stemmed_cleaned_en = stem_text(data, lang)
    unique_words_en = unique_terms(stemmed_cleaned_en)
    model_t = Bool_Model_t(unique_words_en, stemmed_cleaned_en)

    q = query_preprocess(query, lang)
    sim = bool_sim(q,model_t)
    ans = ans[sim.index(True)]

    answer = print_docs(q,ans,lang)
    return answer
