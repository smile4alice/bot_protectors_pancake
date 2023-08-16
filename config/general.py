from dataclasses import dataclass
from config.coordinates import load_coords, MainButtons, Sectors
from services.logger import logger


@dataclass
class PPBot:
    WHITELIST: str
    main_buttons: MainButtons
    sectors: Sectors


@dataclass
class PyTesseract:
    path: str


@dataclass
class Config:
    pp_bot: PPBot
    tesseract: PyTesseract


def load_config(main_coords) -> Config:
    try:
        with open("WHITELIST.txt", "r") as f:
            WHITELIST: list = [item.strip() for item in f.readlines()]
    except:
        WHITELIST = None
        logger.error("В кореневій директорії не знайдено файл < WHITELIST.txt > ")

    coords = load_coords(main_coords)

    return Config(
        pp_bot=PPBot(
            WHITELIST=WHITELIST,
            main_buttons=coords["main_buttons"],
            sectors=coords["sectors"],
        ),
        tesseract=PyTesseract(path="services/Tesseract-OCR/tesseract.exe"),
    )
