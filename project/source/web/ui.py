from pathlib import Path

import streamlit as st

SRC_PATH = Path(__file__).parent / "src"
DOWNLOAD_FILENAME = Path("data/file.pdf")


class Gui:
    def __init__(self):
        """
        Initialize the class Gui
        """
        st.set_page_config(layout="wide")
        self.head_container = st.container()

        self.draw_head()

    def draw_head(self) -> None:
        """
        Draw base widgets of UI

        :return:
            None
        """
        print(f"{SRC_PATH / 'img.png'}")
        with self.head_container:
            title, logo = st.columns([5, 1])
            title.title("Обработка обращений граждан «AAA IT»")
            # we.image(str(SRC_PATH / "img.png"), width=100, output_format="PNG")

            logo.image(str("src/logo.png"), width=200, output_format="PNG")

    def draw_input(self):
        pass


Gui()
