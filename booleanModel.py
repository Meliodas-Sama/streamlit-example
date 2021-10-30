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

def Bool_Model_t (documents):
    """
    Builds a dictionary for documents, mapping each document with a list of its terms
    """
    import numpy as np
    model = {}
    for doc in range(len(documents)):
        model[doc]= list(np.unique(documents[doc]))
    return model

def query_preprocess(query,lang):

    stemmer, wnl, _ = getStopWordsAndStemmer(lang)
    
    st_query = [wnl.lemmatize(stemmer.stem(w)) for w in clean(query,lang).split()]
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

    stemmer, wnl, stop_words = getStopWordsAndStemmer(lang)

    output = []
    stemmed_ans =  [(wnl.lemmatize(stemmer.stem(clean(term,lang))),term) for term in ans.split()]
    for term in stemmed_ans:
        if term[0] in query and not term[0] in ['not', 'and', 'or'] and len(term[0])>1 and not term[1] in stop_words:
            output.append('`'+term[1]+'`')
        else:
            output.append(term[1])
    output_text = ' '.join(output)
    pre_text = 'Accepted answer:  '
    return pre_text, output_text

def model(dataFrame,query,lang):
    _, ans, data = get_data(dataFrame)
    stemmed_cleaned_en = stem_text(data, lang)
    model_t = Bool_Model_t(stemmed_cleaned_en)

    q = query_preprocess(query, lang)
    sim = bool_sim(q,model_t)
    
    if True in sim:
        ans = ans[sim.index(True)]
    else:
        return ('', 'There are no matching documents!! Try another query')

    answer = print_docs(q,ans,lang)
    return answer
