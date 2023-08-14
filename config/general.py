from dataclasses import dataclass


@dataclass
class PPBot:
    WHITELIST: str


@dataclass
class PyTesseract:
    path: str


@dataclass
class Config:
    pp_bot: PPBot
    tesseract: PyTesseract


def load_config() -> Config:
    try:
        with open("WHITELIST.txt", "r") as f:
            WHITELIST: list = [item.strip() for item in f.readlines()]
    except:
        WHITELIST = None
        print("В кореневій директорії не знайдено файл < WHITELIST.txt > ")

    return Config(
        pp_bot=PPBot(
            WHITELIST=WHITELIST,
        ),
        tesseract=PyTesseract(path="services/Tesseract-OCR/tesseract.exe"),
    )
