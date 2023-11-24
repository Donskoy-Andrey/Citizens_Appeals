from pathlib import Path

import streamlit as st

from project.source.string_processing.string_processing import string_processing
from project.source.string_processing.utilities import highlight_words

SRC_PATH = "project/source/web/src/"
DOWNLOAD_FILENAME = Path("data/file.pdf")
button_style = """
        <style>
        .stButton > button
        {
            color: white;
            background: #008FD0;
            border-color: #0066cc;
        }
        .stButton > button:focus {
            border-color: #ffffff;
            box-shadow: none;
            color: #ffffff;
            background-color: #0066cc;
        }
        .stButton > button:focus {
            border-color: #ffffff;
            box-shadow: none;
            color: #ffffff;
            background-color: #0066cc;
        }
        .stButton > button:focus:not(:active) {
            color: white;
            background: #008FD0;
            border-color: #0066cc;
        }
       .stButton > button:hover{
            border-color: #0066cc;
            box-shadow: none;
            color: #ffffff;
            background-color: #0066cc;
       }

        </style>
        """


class Gui:
    def __init__(self):
        """
        Initialize the class Gui
        """
        print(f"{st.__version__=}")
        st.set_page_config(layout="wide")
        self.head_container = st.container()
        self.input_container = st.container()
        self.output_container = st.container()
        self.text_input_form: st.text_area or None = None
        self.submit_button: st.button or None = None

        st.markdown(button_style, unsafe_allow_html=True)
        self.draw_head()
        self.draw_input()

    def draw_head(self) -> None:
        """
        Draw base widgets of UI

        :return:
            None
        """
        with self.head_container:
            title, logo = st.columns([5, 1])
            title.title("Обработка обращений граждан «AAA IT»")
            # we.image(str(SRC_PATH / "img.png"), width=100, output_format="PNG")

            logo.image(
                str(SRC_PATH + "logo.png"), width=200, output_format="PNG"
            )

    def draw_input(self):
        """
        draw input box and submit button
        """
        with self.input_container:
            self.text_input_form = st.text_area(
                label="text_input_1",
                placeholder="Введите обращение...",
                label_visibility="hidden",
                height=400,
            )
            self.submit_button = st.button(
                label="Submit",
                on_click=self.submit_click,
            )

    def submit_click(self):
        self.draw_accepted(self.text_input_form)

    def draw_accepted(self, text):
        print(f"{ string_processing(text)=}")
        html = highlight_words(text)
        print(html)
        # with self.output_container:
        print(f"{html=}")
        with self.output_container:
            # print(f"{self.output_container.=}")
            st.markdown(html, unsafe_allow_html=True)

        # st.markdown(f"<div> aaa </div>", unsafe_allow_html=True)


Gui()
