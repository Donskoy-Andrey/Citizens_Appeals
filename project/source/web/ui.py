import time
from pathlib import Path
import pandas as pd
import streamlit as st

from project.source.inference import TemplateModel

SRC_PATH = "project/source/web/src/"
DOWNLOAD_FILENAME = Path("data/file.pdf")
button_style = """
        <style>
        .stButton > button
        {
            color: white;
            background: #008FD0;
            width: 100
            px;
            height: 50;
        }
        </style>
        """


class Gui:
    def __init__(self):
        """
        Initialize the class Gui
        """
        self.model = TemplateModel()
        st.set_page_config(layout="wide")
        self.head_container = st.container()
        self.input_container = st.container()
        self.output_container = st.container()
        self.text_input_form: st.text_area or None = None
        self.submit_button: st.button or None = None
        self.output_table: st.table or None = None
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
        with self.input_container:
            self.text_input_form = st.text_area(
                label="text_input_1",
                placeholder="Введите обращение...",
                label_visibility="hidden",
                height=400,
                key="text",
            )
            self.submit_button = st.button(
                label="Submit",
                on_click=self.submit_click,
            )

    def submit_click(self):
        gif_path = "https://donskow.com/train4"
        with self.input_container:
            gif_runner = st.image(gif_path)
        self.draw_accepted(self.text_input_form)
        gif_runner.empty()

    def draw_accepted(self, text):
        """
        YOUR CODE HERE
        """
        # time.sleep(2)
        st.text(self.model.predict(text))
        df = pd.DataFrame(columns=["Параметр", "Значение"])
        df.loc[len(df.index)] = [0, 0]
        # self.draw_table(df)

    # def draw_table(self, df):
    #     if self.submit_button:
    #         with self.output_container:
    #             self.output_table = st.table(df)

    #
    # with self.output_container:
    #     st.markdown('<h2> Ваше заявление принято </h2>', unsafe_allow_html=True)
    #     st.markdown(f'<div> {text} </div>', unsafe_allow_html=True)


Gui()
