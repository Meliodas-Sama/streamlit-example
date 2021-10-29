from utils import *

def Bool_Model (unique_words, documents):
    """
    Builds a dictionary for terms, mapping each term with a list of the documents it's in and the count of the term
    """
    import numpy as np
    model = {}
    for t in unique_words:
        model[t] = []
        for doc in range(len(documents)):
            if t in np.unique(documents[doc]):
                model[t].append((doc,documents[doc].count(t)))
    return model

def Bool_Model_t (unique_words, documents):
    """
    Builds a dictionary for documents, mapping each document with a list of its terms, and the count of each term
    """
    import numpy as np
    
    terms_count = len (unique_words)
    docs_count = len (documents)
    
    tf = {}
    
    for doc in range(docs_count):
        tf[doc]={}
        max_tf=0
        for term in range(terms_count):
            if unique_words[term] in documents[doc]:
                tfi = documents[doc].count(unique_words[term])
                if tfi > max_tf:
                    max_tf = tfi
                tf[doc][unique_words[term]] = tfi
        for t in tf[doc]:
            tf[doc][t]/= max_tf
    return tf

def query_preprocess(query,lang = 'English'):
    """
    1. Initialize Word Net Lemmatizer and get stop words and Stemmer for the given language
    2. Removing the words ['and','or','not'] from the stop words so they don't get removed from the query
    3. Clean and stem the query to a list of terms
    4. Return the query list
    """
    from nltk import WordNetLemmatizer
    
    stemmer, stop_words = getStopWordsAndStemmer(lang)
    wnl = WordNetLemmatizer()
    
    stop_words = [w for w in stop_words if not w in ['and','or','not']]
    
    st_query = [wnl.lemmatize(stemmer.stem(w)) for w in clean(query,lang).split() if not w in stop_words and len(w)>1]
    return st_query

def and_sim(x):
    """
    Calculate the Similarity between two terms with the and operator
    
    """
    import numpy as np
    temp = 0
    for t in x:
        temp += (1-t)**2 
    temp /= len(x)
    sim = 1 - np.sqrt(temp)
    return sim

def or_sim (x):
    """
    Calculate the Similarity between two terms with the or operator
    """
    import numpy as np
    temp = 0
    for t in x:
        temp += t**2 
    temp /= len(x)
    sim = np.sqrt(temp)
    return sim

def not_sim(x):
    """
    Calculate the Similarity for a term with a not operator
    """
    return 1-x

def similarity(querySim):
    """
    Calculate the result of a query values:
    1. calculate the values for the NOT operator
    2. calculate the values for a sequence of AND and operator
    3. calculate the values for the sequence of the remaining OR and operator
    return the result
    """
    while('not' in querySim):
        i = querySim.index('not')
        querySim.remove('not')
        querySim[i] = not_sim(querySim[i])

    while ('and' in querySim):
        i = querySim.index('and')
        index = i-1
        and_temp = [querySim[index]]
        while (querySim[i] == 'and'):
            querySim.remove('and')
            and_temp.append(querySim[i])
            querySim.remove(querySim[i])
            if (i) == len(querySim):
                break
        querySim[index] = and_sim(and_temp)

    or_temp = [v for v in querySim if not v=='or']
    querySim = or_sim(or_temp)
    return querySim

def exBooleanSimilarity (query, BModel):
    """
    Calculate the similarity between the query and each of the documents:
    1. for every term in query that is not in [not, and, or] check if term in document
    2. put tf in place of the term in the query
    3. repeat for all documents
    4. Calculate the similarity for each document
    5. return the similarity list
    """
    result = []
    for doc in BModel:
        temp = []
        for t in query:
            if t in ['not', 'and', 'or']:
                temp.append(t)
            elif t in BModel[doc]:
                temp.append(BModel[doc][t])
            else:
                temp.append(0)
        res = similarity(temp)
        result.append(res)
    return result

def print_docs(sim,query,ans,lang='English'):
    from nltk import WordNetLemmatizer
    
    stemmer, _ = getStopWordsAndStemmer(lang)
    wnl = WordNetLemmatizer()
    
    sim_list = sim.tolist()
    sim = sorted(sim,reverse=True)
    print ('Sorted documents in descending order:\n'
           ,' '.join(['D'+str(sim_list.index(i)+1) for i in sim])
           ,'\nMost accepted answer with a similarity of',round(sim[0],2),'% with the query KeyWords in uppercase:\n')
    output = []
    stemmed_ans =  [(wnl.lemmatize(stemmer.stem(clean(term))),term) for term in ans.split() ]
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

# q = query_preprocess('not food or vegetables', 'english')
# s = exBooleanSimilarity(q,model_t)


# s = np.array(s)
# max_ind = s.tolist().index(s.max())
# ans = ans_en[max_ind]

# print_docs(s,q,ans,'english')