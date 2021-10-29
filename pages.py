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


from pandas.core.arrays import boolean


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
            * **Query Input**: Search the uploaded questions  
            * **COVID-19 Query**: Ask a question about COVID-19  
    
        Made with :heart: as a HomeWork for MWS_AIR by Ahmad_155511, Walid_164688
        
    """
    )
    
def upload():
    import streamlit as st
    import pandas as pd

    uploadedFile = st.file_uploader('Upload your CSV file here:','csv')
    language = st.sidebar.empty()
    algo = st.sidebar.empty()
    query = st.empty()
    if uploadedFile:
        st.write('Now you can choose the the lanuage and the algorithm from the sidebar')
        language = st.sidebar.selectbox('Select query language',['English','Arabic'],0)
        algo = st.sidebar.selectbox('Select the algorithm',['Boolean','Extended Boolean','TF-IDF'],0)
        
def covid():
    import streamlit as st
    import pandas as pd
    import altair as alt
    import pickle
    import booleanModel, extendedBooleanModel, TF_IDF


    from urllib.error import URLError

    inputQuery = st.text_input('Enter your query here!')
    language = st.sidebar.selectbox('Select query language',['English','Arabic'],0)
    algo = st.sidebar.selectbox('Select the algorithm',['Boolean','Extended Boolean','TF-IDF'],0)
 
    if inputQuery:
        # @st.cache
        st.write('Done')
