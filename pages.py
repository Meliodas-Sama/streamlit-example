# Copyright 2018-2021 Streamlit Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.



def intro():
    import streamlit as st

    st.sidebar.success("Select a page above.")

    st.markdown(
        """
        ##### Using **_Streamlit_**, **_NLTk_**, and **_RE_** **_Python_** libraries our project can:
        
        * Index a given set of questions and answers to build a mini search-engine using one of the following models:
            * Boolean Model
            * Extended Boolean Model
            * Vector Space (TF-IDF) Model

        * Answer a query (Boolean query, Normal query) about the given questions and answers or about COVID-19 using
        our pre-trained Models about COVID-19 questions.
        
        * **👈 Select a page from the dropdown on the left** to choose what to do!  
            * **Intro**: Current page  
            * **Upload**: To upload Q & A files  
            * **COVID-19 Query**: Ask a question about COVID-19  
    
        Made with :heart: as a HomeWork for MWS_AIR by Ahmad_155511, Walid_164688
        
        [Visit our project repo on GitHub](https://github.com/Meliodas-Sama/streamlit-example)
        
    """
    )
    
def upload():
    import streamlit as st
    import booleanModel, extendedBooleanModel, TF_IDF, utils

    st.write('1. Choose the language of the csv file and the query from the sidebar.  ')
    language = st.sidebar.selectbox('Select language',['_','Arabic','English'],0)
    if not language == '_':
        st.write("""2. Upload a csv file with two columns named Questions, and Answers (or keep the same order).  """)
        uploadMethod =  st.radio('How do you want to upload your file:',['From my files','From a valid URL'],0)
        if uploadMethod == 'From my files':
            uploadedFile = st.file_uploader('Upload your CSV file here:','csv')
        else:
            uploadedFile = st.text_input('Upload your CSV file here:',help='Put a valid URL here')
        algo = st.sidebar.empty()
        inputQuery = st.empty()
        if uploadedFile:
            st.write('3. Now you can choose the Algorithm from the sidebar.')
            algo = st.sidebar.selectbox('Select the Algorithm',['Boolean','Extended Boolean','TF-IDF'],0)
            inputQuery = st.text_input('Enter your query here! (Boolean or Normal)','')
            if inputQuery:
                if algo in ['Boolean','Extended Boolean'] and utils.checkBoolQuery(inputQuery.lower().split()):
                    algos = {'Boolean':booleanModel.model,'Extended Boolean':extendedBooleanModel.model,'TF-IDF':TF_IDF.model}
                    text, answer = algos[algo](uploadedFile, inputQuery, language)
                    st.write(text)
                    st.markdown(answer)
                else:
                    st.markdown('Please enter a valid Boolean query containing terms and boolean operators [Not,And,Or] e.x `not food or vegetables`')
        
def covid():
    import streamlit as st
    import booleanModel, extendedBooleanModel, TF_IDF, utils


    from urllib.error import URLError

    st.write('1. Choose the language of the query from the sidebar.  ')
    language = st.sidebar.selectbox('Select language',['_','Arabic','English'],0)
    if not language == '_':
        st.write('2. Now you can change the Algorithm from the sidebar and then enter a query.')
        inputQuery = st.text_input('Enter your query here! (Boolean or Normal)','')
        algo = st.sidebar.selectbox('Select the Algorithm',['Boolean','Extended Boolean','TF-IDF'],0)
    
        if inputQuery:
            if language == 'English':
                url = 'https://github.com/Meliodas-Sama/streamlit-example/raw/master/covid_data/data_en.csv'
            else:
                url = 'https://github.com/Meliodas-Sama/streamlit-example/raw/master/covid_data/data_ar.csv'

            if algo in ['Boolean','Extended Boolean'] and utils.checkBoolQuery(inputQuery.lower().split()):
                algos = {'Boolean':booleanModel.model,'Extended Boolean':extendedBooleanModel.model,'TF-IDF':TF_IDF.model}
                text, answer = algos[algo](url, inputQuery, language)
                st.write(text)
                st.markdown(answer)
            else:
                st.markdown("""Please enter a valid Boolean query containing terms and boolean operators [Not,And,Or]  
                e.x `not food or vegetables`""")
