import re
from time import sleep
from random import uniform

import pyautogui
import pytesseract

from config.general import Config, load_config
from services.pp_compute_vision import (
    create_screenshot,
    detect_lvl_hero,
    detect_window,
    detect_text,
    get_energy,
    get_quest_status,
    check_congrats,
)
from services.logger import logger


class PPHandlers:
    def __init__(self):
        self.config: Config = load_config()
        pytesseract.pytesseract.tesseract_cmd = self.config.tesseract.path
        pyautogui.PAUSE = uniform(0.4, 0.6)

        base_screen_bgr = create_screenshot("bgr")
        self.main_window, self.main_coords = detect_window(base_screen_bgr)

        x1, y1, x2, y2 = self.main_coords
        self.buttons = {
            "Main City": (int(x1 + (x2 - x1) * 0.0698), int(y1 + (y2 - y1) * 0.959)),
            "Heroes": (int(x1 + (x2 - x1) * 0.216), int(y1 + (y2 - y1) * 0.959)),
            "Backpack": (int(x1 + (x2 - x1) * 0.355), int(y1 + (y2 - y1) * 0.959)),
            "Chapter": (int(x1 + (x2 - x1) * 0.485), int(y1 + (y2 - y1) * 0.959)),
            "Arena": (int(x1 + (x2 - x1) * 0.645), int(y1 + (y2 - y1) * 0.959)),
            "Ranking": (int(x1 + (x2 - x1) * 0.79), int(y1 + (y2 - y1) * 0.959)),
            "Conquest": (int(x1 + (x2 - x1) * 0.935), int(y1 + (y2 - y1) * 0.959)),
        }
        self.sectors = {
            "Recruit": (int(x1 + (x2 - x1) * 0.40), int(y1 + (y2 - y1) * 0.50)),
            "Recruit Once": (int(x1 + (x2 - x1) * 0.27), int(y1 + (y2 - y1) * 0.83)),
            "Medal Hall": (int(x1 + (x2 - x1) * 0.23), int(y1 + (y2 - y1) * 0.4)),
            "Gift Pack": (int(x1 + (x2 - x1) * 0.91), int(y1 + (y2 - y1) * 0.15)),
            "Gift Pack Free": (int(x1 + (x2 - x1) * 0.23), int(y1 + (y2 - y1) * 0.38)),
            "Battles": (int(x1 + (x2 - x1) * 0.65), int(y1 + (y2 - y1) * 0.15)),
            "Expedition Road": (int(x1 + (x2 - x1) * 0.75), int(y1 + (y2 - y1) * 0.70)),
            "Expedition Road Claim": (
                int(x1 + (x2 - x1) * 0.48),
                int(y2 - (y2 - y1) * 0.37),
            ),
            "Quick AFK": (int(x1 + (x2 - x1) * 0.065), int(y1 + (y2 - y1) * 0.73)),
            "Quick AFK Claim": (int(x1 + (x2 - x1) * 0.48), int(y1 + (y2 - y1) * 0.70)),
            "Chest Claim": (int(x1 + (x2 - x1) * 0.84), int(y1 + (y2 - y1) * 0.80)),
            "Store": (int(x1 + (x2 - x1) * 0.75), int(y1 + (y2 - y1) * 0.28)),
            "5 star Hero Fragment": (
                int(x1 + (x2 - x1) * 0.20),
                int(y1 + (y2 - y1) * 0.70),
            ),
            "Recruitment Card": (
                int(x1 + (x2 - x1) * 0.81),
                int(y1 + (y2 - y1) * 0.45),
            ),
            "Store Add Count": (int(x1 + (x2 - x1) * 0.61), int(y1 + (y2 - y1) * 0.52)),
            "Store Purchase": (int(x1 + (x2 - x1) * 0.48), int(y1 + (y2 - y1) * 0.65)),
            "Legion": (int(x1 + (x2 - x1) * 0.45), int(y1 + (y2 - y1) * 0.25)),
            "Legion Store": (int(x1 + (x2 - x1) * 0.23), int(y1 + (y2 - y1) * 0.40)),
            "Legion 5 star Hero Fragment": (
                int(x1 + (x2 - x1) * 0.5),
                int(y1 + (y2 - y1) * 0.865),
            ),
            "Legion Upgrade": (int(x1 + (x2 - x1) * 0.69), int(y1 + (y2 - y1) * 0.72)),
            "Legion Donation": (int(x1 + (x2 - x1) * 0.79), int(y1 + (y2 - y1) * 0.82)),
            "Mine": (int(x1 + (x2 - x1) * 0.40), int(y1 + (y2 - y1) * 0.86)),
            "Arena Challenge": (int(x1 + (x2 - x1) * 0.57), int(y1 + (y2 - y1) * 0.66)),
            "Arena Skip": (int(x1 + (x2 - x1) * 0.095), int(y1 + (y2 - y1) * 0.84)),
            "Relics Exploration": (
                int(x1 + (x2 - x1) * 0.72),
                int(y1 + (y2 - y1) * 0.30),
            ),
            "Relics First Challenge": (
                int(x1 + (x2 - x1) * 0.655),
                int(y1 + (y2 - y1) * 0.775),
            ),
            "Relics Second Challenge": (
                int(x1 + (x2 - x1) * 0.51),
                int(y1 + (y2 - y1) * 0.69),
            ),
            "Mission": (int(x1 + (x2 - x1) * 0.08), int(y1 + (y2 - y1) * 0.12)),
            "Claim Mission": (int(x1 + (x2 - x1) * 0.85), int(y1 + (y2 - y1) * 0.41)),
            "Mission Box 1": (int(x1 + (x2 - x1) * 0.28), int(y1 + (y2 - y1) * 0.32)),
            "Mission Box 2": (int(x1 + (x2 - x1) * 0.44), int(y1 + (y2 - y1) * 0.32)),
            "Mission Box 3": (int(x1 + (x2 - x1) * 0.64), int(y1 + (y2 - y1) * 0.32)),
            "Mission Box 4": (int(x1 + (x2 - x1) * 0.80), int(y1 + (y2 - y1) * 0.32)),
            "Mission Box 5": (int(x1 + (x2 - x1) * 0.95), int(y1 + (y2 - y1) * 0.32)),
            "Upgrade Hero": (int(x1 + (x2 - x1) * 0.516), int(y1 + (y2 - y1) * 0.882)),
        }
        self.mine_sectors = {
            "collect": (int(x1 + (x2 - x1) * 0.50), int(y1 + (y2 - y1) * 0.60)),
            "museum": (int(x1 + (x2 - x1) * 0.35), int(y1 + (y2 - y1) * 0.30)),
            "museum_details": (int(x1 + (x2 - x1) * 0.50), int(y1 + (y2 - y1) * 0.62)),
            "collect_true_submit": (
                int(x1 + (x2 - x1) * 0.38),
                int(y1 + (y2 - y1) * 0.73),
            ),
            "collect_true_put": (
                int(x1 + (x2 - x1) * 0.75),
                int(y1 + (y2 - y1) * 0.73),
            ),
            "collect_true_put_add": (
                int(x1 + (x2 - x1) * 0.30),
                int(y1 + (y2 - y1) * 0.42),
            ),
        }

    def upgrade_hero(self):
        logger.info("UPGRADE HERO")
        x1, y1, x2, y2 = self.main_coords
        pyautogui.click(*self.buttons["Main City"])
        pyautogui.click(*self.buttons["Heroes"])
        pyautogui.moveTo(*self.sectors["Store Purchase"])
        pyautogui.scroll(clicks=-500)

        base_screen_bgr = create_screenshot("bgr")
        hero_list = base_screen_bgr[int(y1 + (y2 - y1) * 0.15) : int(y1 + (y2 - y1) * 0.90), x1:x2]
        res = detect_lvl_hero(hero_list)
        res = list(filter(lambda item: re.findall(r"lv\.[1-80]", item["text"].lower()), res))
        logger.info(f"Heroes < 80 lvl were found: {len(res)}.")
        if res:
            res.sort(key=lambda item: re.findall(r"[1-80]", item["text"])[0])
            x_center = res[0]["left"] + res[0]["width"] // 2
            y_center = int((y2 - y1) * 0.15) + (res[0]["top"] + res[0]["height"] // 2)
            pyautogui.click(x1 + x_center, y1 + y_center, interval=1)
            pyautogui.click(*self.sectors["Upgrade Hero"])
            logger.info("Upgrade hero --> done")
        else:
            logger.warning("not found hero")
        for i in range(4):
            pyautogui.click(*self.buttons["Main City"])

    def claim_free_recruit(self):
        logger.info("CLAIM FREE RECRUIT")
        x1, y1, x2, y2 = self.main_coords
        pyautogui.click(*self.buttons["Main City"])
        pyautogui.click(*self.sectors["Recruit"])
        base_screen_bw = create_screenshot("bgr")
        recruit_section = base_screen_bw[int(y2 - (y2 - y1) * 0.135) : int(y2 - (y2 - y1) * 0.08), x1:x2]
        res = detect_text(recruit_section)
        if list(filter(lambda item: re.findall(r"[123]/3", item["text"]), res)) or not res:  # TODO
            logger.info("check --> the free recruitment is available")
            pyautogui.click(*self.sectors["Recruit Once"], interval=10)
            logger.info("Recruit --> done")
        else:
            logger.warning("check --> the free recruitment is NOT available")
        for i in range(4):
            pyautogui.click(*self.buttons["Main City"])

    def claim_free_medal(self):
        logger.info("CLAIM FREE MEDAL")
        x1, y1, x2, y2 = self.main_coords
        pyautogui.click(*self.buttons["Main City"])
        pyautogui.click(*self.sectors["Medal Hall"])
        pyautogui.click(*self.buttons["Conquest"])
        base_screen_bw = create_screenshot()
        medal_section = base_screen_bw[int(y2 - (y2 - y1) * 0.16) : int(y2 - (y2 - y1) * 0.12), x1:x2]
        res = detect_text(medal_section)
        if list(filter(lambda item: item["text"].lower() == "free", res)):
            logger.info("check --> the free medal is available")
            pyautogui.click(*self.sectors["Recruit Once"], interval=10)
            logger.info("claim medal --> done")
        else:
            logger.warning("check --> the free medal is NOT available")
        for i in range(4):
            pyautogui.click(*self.buttons["Main City"])

    def claim_daily_gift(self):
        logger.info("DAILY GIFT")
        pyautogui.click(*self.buttons["Main City"])
        pyautogui.click(*self.sectors["Gift Pack"])
        pyautogui.click(*self.sectors["Gift Pack Free"], interval=3)
        logger.info("claim gift --> done")
        for i in range(4):
            pyautogui.click(*self.buttons["Main City"])

    def claim_free_expidition(self):
        logger.info("CLAIM FREE EXPIDITION")
        pyautogui.click(*self.buttons["Main City"])
        pyautogui.click(*self.sectors["Battles"])
        pyautogui.click(*self.sectors["Expedition Road"])
        pyautogui.click(*self.buttons["Chapter"])
        pyautogui.click(*self.sectors["Expedition Road Claim"], interval=3)
        logger.info("Expedition Road Claim --> done")
        for i in range(4):
            pyautogui.click(*self.buttons["Main City"])

    def claim_quick_afk(self):
        logger.info("CLAIM QUICK AFK")
        x1, y1, x2, y2 = self.main_coords
        pyautogui.click(*self.buttons["Main City"])
        pyautogui.click(*self.buttons["Chapter"])
        pyautogui.click(*self.sectors["Chest Claim"])
        pyautogui.click(*self.sectors["Quick AFK Claim"], interval=3)
        pyautogui.click(*self.buttons["Main City"])
        base_screen_bw = create_screenshot()
        quick_buttons = base_screen_bw[int(y1 + (y2 - y1) * 0.61) : int(y1 + (y2 - y1) * 0.87), x1:x2]
        res = detect_text(quick_buttons)
        logger.info("search --> [Quick AFK]")
        res = list(filter(lambda item: item["text"].lower() == "afk", res))
        if res:
            x_center = res[0]["left"] + res[0]["width"] // 2
            y_center = int((y2 - y1) * 0.61) + (res[0]["top"] + res[0]["height"] // 2)
            pyautogui.click(x1 + x_center, y1 + y_center)
            logger.info("[Quick AFK] were found")
            base_screen_bw = create_screenshot()
            free_button = base_screen_bw[int(y1 + (y2 - y1) * 0.61) : int(y1 + (y2 - y1) * 0.87), x1:x2]
            res = detect_text(free_button)
            logger.info("search --> [Free]")
            res = list(filter(lambda item: item["text"].lower() == "free", res))  # TODO
            if res:
                logger.info("[Free] were found")
                pyautogui.click(*self.sectors["Quick AFK Claim"], interval=3)
            else:
                logger.warning("[Free] not found")
        else:
            logger.warning("[Quick AFK] not found")
        logger.info("Quick AFK Claim --> done")
        for i in range(3):
            pyautogui.click(*self.buttons["Main City"])

    def purchase_store_items(self):
        logger.info("PURCHASE STORE ITEMS")
        x1, y1, x2, y2 = self.main_coords

        def control_missclick():
            base_screen_bgr = create_screenshot("bgr")
            purchase_section = base_screen_bgr[
                int(y1 + (y2 - y1) * 0.64) : int(y1 + (y2 - y1) * 0.68),
                int(x1 + (x2 - x1) * 0.35) : int(x1 + (x2 - x1) * 0.66),
            ]
            res = detect_text(purchase_section)
            if list(filter(lambda item: item["text"].lower() == "purchase", res)):
                logger.info("the purchase window is open")
                return True
            else:
                logger.info("check --> the purchase window is closed")
                return False

        pyautogui.click(*self.buttons["Main City"])
        pyautogui.click(*self.sectors["Store"])
        pyautogui.click(*self.sectors["Recruitment Card"])
        if control_missclick():  # check if missclick
            pyautogui.click(*self.sectors["Store Purchase"], interval=3)
            logger.info("Recruitment Card purchase --> done")
        else:
            logger.warning("Recruitment Card purchase --> fail")
        pyautogui.click(*self.sectors["5 star Hero Fragment"])
        pyautogui.click(*self.sectors["5 star Hero Fragment"])
        if control_missclick():  # check if missclick
            for i in range(5):
                pyautogui.click(*self.sectors["Store Add Count"])
            pyautogui.click(*self.sectors["Store Purchase"], interval=3)
            logger.info("5 star Hero Fragment purchase --> done")
        else:
            logger.warning("Recruitment Card purchase --> fail")
        for i in range(4):
            pyautogui.click(*self.buttons["Main City"])

    def purchase_legion_items(self):
        logger.info("PURCHASE LEGION ITEMS")
        pyautogui.click(*self.buttons["Main City"])
        pyautogui.click(*self.sectors["Legion"])
        pyautogui.click(*self.sectors["Legion Store"])
        pyautogui.moveTo(*self.sectors["Store Purchase"])
        pyautogui.scroll(clicks=-20)
        sleep(0.5)
        pyautogui.click(*self.sectors["Legion 5 star Hero Fragment"])
        for i in range(5):
            pyautogui.click(*self.sectors["Store Add Count"])
        pyautogui.click(*self.sectors["Store Purchase"], interval=3)
        logger.info("purchase legion items --> done")
        for i in range(5):
            pyautogui.click(*self.buttons["Main City"])

    def purchase_legion_donation(self):
        logger.info("PURCHASE LEGION DONATION")
        pyautogui.click(*self.buttons["Main City"])
        pyautogui.click(*self.sectors["Legion"])
        pyautogui.click(*self.sectors["Legion Upgrade"])
        pyautogui.click(*self.sectors["Legion Donation"], interval=3)
        logger.info("legion donation --> done")
        for i in range(5):
            pyautogui.click(*self.buttons["Main City"])

    def claim_mission(self):
        logger.info("CLAIM MISSION")
        x1, y1, x2, y2 = self.main_coords
        pyautogui.click(*self.buttons["Main City"])
        pyautogui.click(*self.sectors["Mission"])
        for i in range(11):
            base_screen_bgr = create_screenshot("bgr")
            claim_section = base_screen_bgr[
                int(y1 + (y2 - y1) * 0.40) : int(y1 + (y2 - y1) * 0.43),
                int(x1 + (x2 - x1) * 0.79) : int(x1 + (x2 - x1) * 0.96),
            ]
            res = detect_text(claim_section)
            if list(filter(lambda item: item["text"].lower() == "claim", res)):
                pyautogui.click(*self.sectors["Claim Mission"], interval=2)
                pyautogui.click(*self.sectors["Claim Mission"])
                logger.info("check --> [Claim] is avalaible")
            else:
                logger.warning("check --> [Claim] is NOT avalaible")
                break
        pyautogui.click(*self.sectors["Mission Box 1"], interval=3)
        pyautogui.click(*self.sectors["Mission Box 2"])
        pyautogui.click(*self.sectors["Mission Box 2"], interval=3)
        pyautogui.click(*self.sectors["Mission Box 3"])
        pyautogui.click(*self.sectors["Mission Box 3"], interval=3)
        pyautogui.click(*self.sectors["Mission Box 4"])
        pyautogui.click(*self.sectors["Mission Box 4"], interval=3)
        pyautogui.click(*self.sectors["Mission Box 5"])
        pyautogui.click(*self.sectors["Mission Box 5"], interval=3)
        for i in range(4):
            pyautogui.click(*self.buttons["Main City"])

    def join_to_arena(self):
        logger.info("JOIN TO ARENA")
        pyautogui.click(*self.buttons["Main City"])
        pyautogui.click(*self.buttons["Arena"])
        pyautogui.click(*self.sectors["Arena Challenge"])
        pyautogui.click(*self.sectors["Arena Challenge"], interval=2)
        pyautogui.click(*self.buttons["Ranking"], interval=10)
        pyautogui.click(*self.sectors["Arena Skip"])
        logger.info("area battle --> done")
        for i in range(4):
            pyautogui.click(*self.buttons["Main City"])

    def joit_to_chapter(self):
        logger.info("JOIN TO CHAPTER")
        x1, y1, x2, y2 = self.main_coords
        pyautogui.click(*self.buttons["Main City"])
        pyautogui.click(*self.buttons["Chapter"])
        base_screen_bw = create_screenshot()
        chapter_buttons = base_screen_bw[int(y1 + (y2 - y1) * 0.71) : int(y1 + (y2 - y1) * 0.87), x1:x2]
        res = detect_text(chapter_buttons)
        logger.info("search --> [Auto Challenge]")
        res = list(filter(lambda item: item["text"].lower() == "auto", res))
        if res:
            x_center = res[0]["left"] + res[0]["width"] // 2
            y_center = int((y2 - y1) * 0.71) + (res[0]["top"] + res[0]["height"] // 2)
            pyautogui.click(x1 + x_center, y1 + y_center)
            logger.info("[Auto Challenge] were found")

            while True:
                sleep(5)
                pyautogui.click(*self.buttons["Chapter"])
                base_screen_bgr = create_screenshot("bgr")
                challenge_button = base_screen_bgr[
                    int(y1 + (y2 - y1) * 0.8) : int(y1 + (y2 - y1) * 0.87),
                    int(x1 + (x2 - x1) * 0.3) : int(x1 + (x2 - x1) * 0.7),
                ]
                res = detect_text(challenge_button)
                if list(filter(lambda item: item["text"] == "Challenge", res)):
                    logger.info("check --> the battle is OVER")
                    break
                else:
                    logger.info("check --> the battle is NOT over")
        else:
            logger.warning("Not found [Auto Challenge]")
        for i in range(4):
            pyautogui.click(*self.buttons["Main City"])

    def joit_to_relics(self):
        logger.info("JOIN TO RELICS")
        x1, y1, x2, y2 = self.main_coords
        pyautogui.click(*self.buttons["Main City"])
        pyautogui.click(*self.sectors["Battles"])
        pyautogui.click(*self.sectors["Relics Exploration"])
        pyautogui.click(*self.sectors["Relics First Challenge"])
        pyautogui.click(*self.sectors["Relics First Challenge"])
        while True:
            sleep(5)
            pyautogui.click(*self.buttons["Chapter"])
            base_screen_bgr = create_screenshot("bgr")
            title_section = base_screen_bgr[
                int(y2 - (y2 - y1) * 0.97) : int(y2 - (y2 - y1) * 0.88),
                int(x1 + (x2 - x1) * 0.2) : int(x1 + (x2 - x1) * 0.8),
            ]
            res = detect_text(title_section)
            if list(filter(lambda item: item["text"] in ["Relic", "Exploration"], res)):
                logger.info("check --> the battle is over")
                break
            else:
                logger.info("check --> the battle is not over")
        for i in range(5):
            pyautogui.click(*self.buttons["Main City"])

    def farm_mine(self):
        logger.info("FARM MINE")
        x1, y1, x2, y2 = self.main_coords
        pyautogui.click(*self.buttons["Main City"])
        pyautogui.click(*self.sectors["Mine"])
        while True:
            try:
                base_screen_bw = create_screenshot("bgr")
                main_window = base_screen_bw[y1:y2, x1:x2]
                res, energy_left = get_energy(main_window, self.main_coords)
                is_complete_quests = get_quest_status(main_window, self.main_coords)
                logger.info(f"Energy: {energy_left} | Quests: {is_complete_quests}")
                if res:
                    if energy_left > 0 and is_complete_quests:
                        pyautogui.click(*self.mine_sectors["collect"])
                        sleep(3)
                        base_screen_bgr = create_screenshot("bgr")
                        congrats_section = base_screen_bgr[int(y2 - (y2 - y1) * 0.785) : int(y2 - (y2 - y1) * 0.675), x1:x2]
                        collect_true_section = base_screen_bgr[int(y2 - (y2 - y1) * 0.53) : int(y2 - (y2 - y1) * 0.43), x1:x2]
                        cong = round(check_congrats(congrats_section), 2)
                        if cong > 0.50:
                            logger.info(f"The congrats window match: {cong} > 0.50")
                            res = detect_text(collect_true_section)
                            for res_item in res:
                                if res_item["text"] in self.config.pp_bot.WHITELIST:
                                    logger.warning("BREAK --> WHITELIST: " + "\033[1m\033[31m{}".format(res_item["text"]))
                                    return True
                            else:
                                logger.info("SUBMIT AND CONTINUE")
                                pyautogui.click(*self.mine_sectors["collect_true_submit"])
                                continue
                        else:
                            logger.info(f"The congrats window match: {cong} < 0.50")

                    else:
                        logger.warning("IT's OVER")
                        break
                else:
                    pyautogui.click(*self.buttons["Main City"])
                    logger.warning('repeat function')
                    sleep(1)
                    self.farm_mine()

            except Exception as exc:
                logger.error(exc)
