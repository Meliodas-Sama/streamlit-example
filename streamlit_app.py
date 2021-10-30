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

import inspect
import textwrap
from collections import OrderedDict

import streamlit as st
from streamlit.logger import get_logger
import pages

LOGGER = get_logger(__name__)



# Dictionary of
# page_name -> (page_function, page_description)
PAGES = OrderedDict(
    [
        ("Intro", (pages.intro, None)),
        (
            "Upload",
            (
                pages.upload,
                """
                #### Here you can upload a csv file (from a valid URL, or from your files):  
                """,
            ),
        ),
        (
            "COVID-19 Query",
            (
                pages.covid,
                """
                Here you can ask one of our pre-trained COVID-19 Models, after choosing one from the sidebar along with the language.
                """,
            ),
        ),
    ]
)

def run():
    page_name = st.sidebar.selectbox("Choose a page", list(PAGES.keys()), 0)
    page = PAGES[page_name][0]

    if page_name == "Intro":
        show_code = False
        st.write("# Welcome to our IR project! 👋")
    else:
        show_code = st.sidebar.checkbox("Show code", False)
        st.markdown("# %s" % page_name)
        description = PAGES[page_name][1]
        if description:
            st.write(description)
        # Clear everything from the intro page.
        # We only have 4 elements in the page so this is intentional overkill.
        for i in range(15):
            st.empty()

    page()

    if show_code:
        st.markdown("## Code")
        sourcelines, _ = inspect.getsourcelines(page)
        st.code(textwrap.dedent("".join(sourcelines[1:])))


if __name__ == "__main__":
    run()
