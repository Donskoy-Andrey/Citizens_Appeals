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

        self.uploaded_file = None
        self.button_disabled = True
        self.check_button: st.button or None = None
        self.head_container = st.container()

        self.upload_container = st.container()
        self.result_container = st.container()
        self.result_container.write("")
        self.button_container = st.container()
        self.data_container = st.container()
        self.data_container.write("")

        self.__draw_gui()

    def __draw_gui(self) -> None:
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
                str(SRC_PATH / "logo.png"), width=150, output_format="PNG"
            )

        self.draw_choose_file()

        with self.button_container:
            self.check_button = st.button(
                "Проверить",
                help="Проверить документ",
                on_click=lambda: self.run_file_processing(),
                disabled=self.button_disabled,
            )
