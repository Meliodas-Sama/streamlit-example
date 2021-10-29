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
    from nltk import PorterStemmer, WordNetLemmatizer

    ps = PorterStemmer()
    wnl = WordNetLemmatizer()
    

    stop_words = set(stopwords.words(lang))
    stop_words = [w for w in stop_words if not w in ['and','or','not']]
    
    st_query = [wnl.lemmatize(ps.stem(w)) for w in clean(query).split() if not w in stop_words and len(w)>1]
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

def print_docs(sim,query,ans):
    from nltk import PorterStemmer, WordNetLemmatizer
    ps = PorterStemmer()
    wnl = WordNetLemmatizer()
    
    print ('Accepted documents:\n'
           ,' '.join(['D'+str(i) for i in range(len(sim)) if sim[i] == True])
           ,'\nFirst accepted answer:\n')
    output = []
    stemmed_ans =  [(wnl.lemmatize(ps.stem(clean(term))),term) for term in ans.split() ]
    for term in stemmed_ans:
        if term[0] in query:
            output.append(term[1].upper())
        else:
            output.append(term[1])
    output_text = ' '.join(output)
    print(output_text)
    return

# stemmed_cleaned_en = stem_text(data_en, 'English')
# unique_words_en = unique_terms(stemmed_cleaned_en)
# model = Bool_Model (unique_words_en, stemmed_cleaned_en)
# model_t = Bool_Model_t(unique_words_en, stemmed_cleaned_en)

# q = query_preprocess('not food or vegetables', lang='english')
# sim = bool_sim(q,model_t)
# ans = ans_en[sim.index(True)]

# print_docs(sim,q,ans)