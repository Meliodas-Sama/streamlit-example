from utils import *

def Inverse_Document_Frequency (df, docs_count):
    import numpy as np
    return np.log2(float(docs_count) / (df))

def TF_IDF (terms, documents):
    """
    Calculating the TF-IDF for unique terms in documents
    1. calculate the count of terms and documents
    2. initalize tf, idf, TF-IDF matrices
    3. calculate the tf, idf for each term
    4. normalize the tfs for each document by dividing it by the max tf in the document
    5. calculate the TF-IDF by multiplaying tf and idf
    """
    import numpy as np
    
    terms_count = len (terms)
    docs_count = len (documents)
    
    tf = np.zeros((docs_count, terms_count))
    idf = np.zeros((terms_count))
    TF_IDF = np.zeros((docs_count, terms_count))
    
    for term in range(terms_count):
        df = 0
        for doc in range(docs_count):
            tf[doc][term] = documents[doc].count(terms[term])
            if terms[term] in documents[doc]:
                df += 1
        idf[term] = Inverse_Document_Frequency(df, docs_count)
    for doc in range(docs_count):
        tf[doc] = tf[doc] / float(tf[doc].max())
    
    TF_IDF = tf * idf
    return TF_IDF, idf, tf

def query_to_vector(query, IDF, words):
    """
    Transforming the query to a vector for calculating the similarity with other documents
    1. initializing the query vector
    2. calculating the values for each unique term in query that's in words
    returns the query vector
    """
    import numpy as np
    
    queryVector = np.zeros(len(IDF))
    max_term_count = 1
    
    for term in np.unique(query):
        if term in words:
            tf = query.count(term)
            if max_term_count <= tf:
                max_term_count = tf
            queryVector[words.index(term)] = tf * IDF[words.index(term)]
    queryVector = queryVector / float(max_term_count)
    return queryVector

def vector_length(vec):
    """
    calculate the length of the given vector
    """
    import numpy as np
    length = np.sqrt(np.sum(np.power(vec,2)))
    return length

def cos_sim (query, documents):
    """
    calculate the cosine similarity between the query and each of the documents
    1. calculate the inner product of the query and each of the documents
    2. calculate the product of the query length and the length of each of the documents
    3. divid the values 
    return the cos result
    """
    import numpy as np
    if np.shape(query)[0] == np.shape(documents)[0]:
        documents = np.swapaxes(documents, 0, 1)
    enum = np.array([np.dot(query, documents[doc]) for doc in range(len(documents))])
    denom = np.array([vector_length(query) * vector_length(documents[doc]) for doc in range(len(documents))])
    cos = enum / denom
    return cos

def query_preprocess(query,lang):
    stemmed_query = stem_text([query], lang)
    return stemmed_query

def print_docs(cos,query,ans):
    from nltk import PorterStemmer, WordNetLemmatizer
    ps = PorterStemmer()
    wnl = WordNetLemmatizer()
    
    cos_list = cos.tolist()
    cos = sorted(cos,reverse=True)
    print ('Sorted documents in descending order:\n'
           ,' '.join(['D'+str(cos_list.index(i)+1) for i in cos])
           ,'\nMost accepted answer with the KeyWords in the query in uppercase:\n')
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
# tf_idf, idf, tf = TF_IDF (unique_words_en, stemmed_cleaned_en)

# query = query_preprocess('can i get covid-19 from unwashed vegetables','english')
# qv = query_to_vector(query, idf, unique_words_en)
# cos = cos_sim(qv, tf_idf)

# ans_index = cos.tolist().index(cos.max())
# print_docs(cos,query,ans_en[ans_index])

