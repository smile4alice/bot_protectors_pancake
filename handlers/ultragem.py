import re
from time import sleep

import pyautogui
import pytesseract

from config.general import Config, load_config
from services.pp_compute_vision import (
    create_screenshot,
    detect_window,
    detect_text,
    get_energy,
    get_quest_status,
    check_congrats,
)


class PPHandlers:
    def __init__(self):
        self.config: Config = load_config()
        pytesseract.pytesseract.tesseract_cmd = self.config.tesseract.path
        pyautogui.PAUSE = 0.3

        base_screen_bgr = create_screenshot("bgr")
        self.main_window, self.main_coords = detect_window(base_screen_bgr)

        x1, y1, x2, y2 = self.main_coords
        self.buttons = {
            "Main City": (int(x1 + (x2 - x1) * 0.065), int(y2 - (y2 - y1) * 0.05)),
            "Heroes": (int(x1 + (x2 - x1) * 0.21), int(y2 - (y2 - y1) * 0.05)),
            "Backpack": (int(x1 + (x2 - x1) * 0.355), int(y2 - (y2 - y1) * 0.05)),
            "Chapter": (int(x1 + (x2 - x1) * 0.485), int(y2 - (y2 - y1) * 0.05)),
            "Arena": (int(x1 + (x2 - x1) * 0.645), int(y2 - (y2 - y1) * 0.05)),
            "Ranking": (int(x1 + (x2 - x1) * 0.79), int(y2 - (y2 - y1) * 0.05)),
            "Conquest": (int(x1 + (x2 - x1) * 0.935), int(y2 - (y2 - y1) * 0.05)),
        }
        self.sectors = {
            "Recruit": (int(x1 + (x2 - x1) * 0.40), int(y2 - (y2 - y1) * 0.50)),
            "Recruit Once": (int(x1 + (x2 - x1) * 0.27), int(y2 - (y2 - y1) * 0.17)),
            "Medal Hall": (int(x1 + (x2 - x1) * 0.23), int(y2 - (y2 - y1) * 0.6)),
            "Gift Pack": (int(x1 + (x2 - x1) * 0.91), int(y2 - (y2 - y1) * 0.85)),
            "Gift Pack Free": (int(x1 + (x2 - x1) * 0.23), int(y2 - (y2 - y1) * 0.62)),
            "Battles": (int(x1 + (x2 - x1) * 0.65), int(y2 - (y2 - y1) * 0.85)),
            "Expedition Road": (int(x1 + (x2 - x1) * 0.75), int(y2 - (y2 - y1) * 0.30)),
            "Expedition Road Claim": (
                int(x1 + (x2 - x1) * 0.48),
                int(y2 - (y2 - y1) * 0.37),
            ),
            "Quick AFK": (int(x1 + (x2 - x1) * 0.065), int(y2 - (y2 - y1) * 0.27)),
            "Quick AFK Claim": (int(x1 + (x2 - x1) * 0.48), int(y2 - (y2 - y1) * 0.30)),
            "Chest Claim": (int(x1 + (x2 - x1) * 0.84), int(y2 - (y2 - y1) * 0.20)),
            "Store": (int(x1 + (x2 - x1) * 0.75), int(y2 - (y2 - y1) * 0.72)),
            "5 star Hero Fragment": (
                int(x1 + (x2 - x1) * 0.2),
                int(y2 - (y2 - y1) * 0.30),
            ),
            "Recruitment Card": (
                int(x1 + (x2 - x1) * 0.81),
                int(y2 - (y2 - y1) * 0.55),
            ),
            "Store Add Count": (int(x1 + (x2 - x1) * 0.61), int(y2 - (y2 - y1) * 0.48)),
            "Store Purchase": (int(x1 + (x2 - x1) * 0.48), int(y2 - (y2 - y1) * 0.35)),
            "Legion": (int(x1 + (x2 - x1) * 0.45), int(y2 - (y2 - y1) * 0.75)),
            "Legion Store": (int(x1 + (x2 - x1) * 0.23), int(y2 - (y2 - y1) * 0.6)),
            "Legion 5 star Hero Fragment": (
                int(x1 + (x2 - x1) * 0.5),
                int(y2 - (y2 - y1) * 0.135),
            ),
            "Legion Upgrade": (int(x1 + (x2 - x1) * 0.69), int(y2 - (y2 - y1) * 0.28)),
            "Legion Donation": (int(x1 + (x2 - x1) * 0.79), int(y2 - (y2 - y1) * 0.18)),
            "Mine": (int(x1 + (x2 - x1) * 0.40), int(y2 - (y2 - y1) * 0.14)),
            "Arena Challenge": (int(x1 + (x2 - x1) * 0.57), int(y2 - (y2 - y1) * 0.34)),
            "Arena Skip": (int(x1 + (x2 - x1) * 0.095), int(y2 - (y2 - y1) * 0.16)),
            "Relics Exploration": (
                int(x1 + (x2 - x1) * 0.72),
                int(y2 - (y2 - y1) * 0.70),
            ),
            "Relics First Challenge": (
                int(x1 + (x2 - x1) * 0.655),
                int(y2 - (y2 - y1) * 0.225),
            ),
            "Relics Second Challenge": (
                int(x1 + (x2 - x1) * 0.51),
                int(y2 - (y2 - y1) * 0.31),
            ),
            "Mission": (int(x1 + (x2 - x1) * 0.08), int(y2 - (y2 - y1) * 0.88)),
            "Claim Mission": (int(x1 + (x2 - x1) * 0.85), int(y2 - (y2 - y1) * 0.59)),
            "Mission Box 1": (int(x1 + (x2 - x1) * 0.28), int(y2 - (y2 - y1) * 0.68)),
            "Mission Box 2": (int(x1 + (x2 - x1) * 0.44), int(y2 - (y2 - y1) * 0.68)),
            "Mission Box 3": (int(x1 + (x2 - x1) * 0.64), int(y2 - (y2 - y1) * 0.68)),
            "Mission Box 4": (int(x1 + (x2 - x1) * 0.80), int(y2 - (y2 - y1) * 0.68)),
            "Mission Box 5": (int(x1 + (x2 - x1) * 0.95), int(y2 - (y2 - y1) * 0.68)),
        }
        self.mine_sectors = {
            "collect": (int(x1 + (x2 - x1) * 0.50), int(y2 - (y2 - y1) * 0.40)),
            "museum": (int(x1 + (x2 - x1) * 0.35), int(y2 - (y2 - y1) * 0.70)),
            "museum_details": (int(x1 + (x2 - x1) * 0.50), int(y2 - (y2 - y1) * 0.38)),
            "collect_true_submit": (
                int(x1 + (x2 - x1) * 0.38),
                int(y2 - (y2 - y1) * 0.27),
            ),
            "collect_true_put": (
                int(x1 + (x2 - x1) * 0.75),
                int(y2 - (y2 - y1) * 0.27),
            ),
            "collect_true_put_add": (
                int(x1 + (x2 - x1) * 0.30),
                int(y2 - (y2 - y1) * 0.58),
            ),
        }

    def claim_free_recruit(self):
        print("CLAIM FREE RECRUIT")
        x1, y1, x2, y2 = self.main_coords
        pyautogui.click(*self.buttons["Main City"])
        pyautogui.click(*self.sectors["Recruit"])
        base_screen_bw = create_screenshot("bgr")
        recruit_section = base_screen_bw[
            int(y2 - (y2 - y1) * 0.135) : int(y2 - (y2 - y1) * 0.08), x1:x2
        ]
        res = detect_text(recruit_section)
        if (
            list(filter(lambda item: re.findall(r"[123]/3", item["text"]), res))
            or not res
        ):  # TODO
            print("check --> the free recruitment is available")
            pyautogui.click(*self.sectors["Recruit Once"], interval=8)
        else:
            print("check --> the free recruitment is NOT available")
        pyautogui.click(*self.buttons["Main City"], clicks=4)

    def claim_free_medal(self):
        print("CLAIM FREE MEDAL")
        x1, y1, x2, y2 = self.main_coords
        pyautogui.click(*self.buttons["Main City"])
        pyautogui.click(*self.sectors["Medal Hall"])
        pyautogui.click(*self.buttons["Conquest"])
        base_screen_bw = create_screenshot()
        medal_section = base_screen_bw[
            int(y2 - (y2 - y1) * 0.16) : int(y2 - (y2 - y1) * 0.12), x1:x2
        ]
        res = detect_text(medal_section)
        if list(filter(lambda item: item["text"].lower() == "free", res)):
            print("check --> the free medal is available")
            pyautogui.click(*self.sectors["Recruit Once"], interval=8)
        else:
            print("check --> the free medal is NOT available")
        pyautogui.click(*self.buttons["Main City"], clicks=4)

    def claim_daily_gift(self):
        print("DAILY GIFT")
        pyautogui.click(*self.buttons["Main City"])
        pyautogui.click(*self.sectors["Gift Pack"])
        pyautogui.click(*self.sectors["Gift Pack Free"], interval=3)
        pyautogui.click(*self.buttons["Main City"], clicks=4)

    def claim_free_expidition(self):
        print("CLAIM FREE EXPIDITION")
        pyautogui.click(*self.buttons["Main City"])
        pyautogui.click(*self.sectors["Battles"])
        pyautogui.click(*self.sectors["Expedition Road"])
        pyautogui.click(*self.buttons["Chapter"])
        pyautogui.click(*self.sectors["Expedition Road Claim"], interval=3)
        pyautogui.click(*self.buttons["Main City"], clicks=3)

    def claim_quick_afk(self):
        print("CLAIM QUICK AFK")
        pyautogui.click(*self.buttons["Main City"])
        pyautogui.click(*self.buttons["Chapter"])
        pyautogui.click(*self.sectors["Chest Claim"])
        pyautogui.click(*self.sectors["Quick AFK Claim"], interval=3)
        pyautogui.click(*self.buttons["Main City"])
        pyautogui.click(*self.sectors["Quick AFK"])
        pyautogui.click(*self.sectors["Quick AFK Claim"], interval=3)
        pyautogui.click(*self.buttons["Main City"], clicks=3)

    def purchase_store_items(self):
        print("PURCHASE STORE ITEMS")
        x1, y1, x2, y2 = self.main_coords

        def control_missclick():
            base_screen_bgr = create_screenshot("bgr")
            purchase_section = base_screen_bgr[
                int(y2 - (y2 - y1) * 0.36) : int(y2 - (y2 - y1) * 0.32),
                int(x1 + (x2 - x1) * 0.35) : int(x1 + (x2 - x1) * 0.66),
            ]
            res = detect_text(purchase_section)
            if list(filter(lambda item: item["text"].lower() == "purchase", res)):
                print("the purchase window is open")
                return True
            else:
                print("check --> the purchase window is closed")
                return False

        pyautogui.click(*self.buttons["Main City"])
        pyautogui.click(*self.sectors["Store"])
        pyautogui.click(*self.sectors["Recruitment Card"])
        if control_missclick():  # check if missclick
            pyautogui.click(*self.sectors["Store Purchase"], interval=3)
        pyautogui.click(*self.sectors["5 star Hero Fragment"], clicks=2)
        if control_missclick():  # check if missclick
            pyautogui.click(*self.sectors["Store Add Count"], clicks=5)
            pyautogui.click(*self.sectors["Store Purchase"], interval=3)
        pyautogui.click(*self.buttons["Main City"], clicks=4)

    def purchase_legion_items(self):
        print("PURCHASE LEGION ITEMS")
        pyautogui.click(*self.buttons["Main City"])
        pyautogui.click(*self.sectors["Legion"])
        pyautogui.click(*self.sectors["Legion Store"])
        pyautogui.moveTo(*self.sectors["Store Purchase"])
        pyautogui.scroll(clicks=-20)
        pyautogui.click(*self.sectors["Legion 5 star Hero Fragment"])
        pyautogui.click(*self.sectors["Store Add Count"], clicks=5)
        pyautogui.click(*self.sectors["Store Purchase"], interval=3)
        pyautogui.click(*self.buttons["Main City"], clicks=5)

    def purchase_legion_donation(self):
        print("PURCHASE LEGION DONATION")
        pyautogui.click(*self.buttons["Main City"])
        pyautogui.click(*self.sectors["Legion"])
        pyautogui.click(*self.sectors["Legion Upgrade"])
        pyautogui.click(*self.sectors["Legion Donation"], interval=3)
        pyautogui.click(*self.buttons["Main City"], clicks=5)

    def claim_mission(self):
        print("CLAIM MISSION")
        x1, y1, x2, y2 = self.main_coords
        pyautogui.click(*self.buttons["Main City"])
        pyautogui.click(*self.sectors["Mission"])
        for i in range(11):
            base_screen_bgr = create_screenshot("bgr")
            claim_section = base_screen_bgr[
                int(y2 - (y2 - y1) * 0.60) : int(y2 - (y2 - y1) * 0.57),
                int(x1 + (x2 - x1) * 0.79) : int(x1 + (x2 - x1) * 0.96),
            ]
            res = detect_text(claim_section)
            if list(filter(lambda item: item["text"].lower() == "claim", res)):
                pyautogui.click(*self.sectors["Claim Mission"], clicks=2, interval=2)
            else:
                break

        pyautogui.click(*self.sectors["Mission Box 1"], interval=3)
        pyautogui.click(*self.sectors["Mission Box 2"], interval=3, clicks=2)
        pyautogui.click(*self.sectors["Mission Box 3"], interval=3, clicks=2)
        pyautogui.click(*self.sectors["Mission Box 4"], interval=3, clicks=2)
        pyautogui.click(*self.sectors["Mission Box 5"], interval=3, clicks=2)
        pyautogui.click(*self.buttons["Main City"], clicks=5)

    def join_to_arena(self):
        print("JOIN TO ARENA")
        pyautogui.click(*self.buttons["Main City"])
        pyautogui.click(*self.buttons["Arena"])
        pyautogui.click(*self.sectors["Arena Challenge"])
        pyautogui.click(*self.sectors["Arena Challenge"], interval=1)
        pyautogui.click(*self.buttons["Ranking"], interval=10)
        pyautogui.click(*self.sectors["Arena Skip"])
        pyautogui.click(*self.buttons["Main City"], clicks=4)

    def joit_to_chapter(self):
        print("JOIN TO CHAPTER")
        x1, y1, x2, y2 = self.main_coords
        pyautogui.click(*self.buttons["Main City"])
        pyautogui.click(*self.buttons["Chapter"])
        pyautogui.click(*self.sectors["Arena Skip"])
        while True:
            sleep(5)
            pyautogui.click(*self.buttons["Chapter"])
            base_screen_bgr = create_screenshot("bgr")
            challenge_button = base_screen_bgr[
                int(y2 - (y2 - y1) * 0.2) : int(y2 - (y2 - y1) * 0.13),
                int(x1 + (x2 - x1) * 0.3) : int(x1 + (x2 - x1) * 0.7),
            ]
            res = detect_text(challenge_button)
            if list(filter(lambda item: item["text"] == "Challenge", res)):
                print("check --> the battle is over")
                break
            else:
                print("check --> the battle is not over")
        pyautogui.click(*self.buttons["Main City"], clicks=4)

    def joit_to_relics(self):
        print("JOIN TO RELICS")
        x1, y1, x2, y2 = self.main_coords
        pyautogui.click(*self.buttons["Main City"])
        pyautogui.click(*self.sectors["Battles"])
        pyautogui.click(*self.sectors["Relics Exploration"])
        pyautogui.click(*self.sectors["Relics First Challenge"], clicks=2)
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
                print("check --> the battle is over")
                break
            else:
                print("check --> the battle is not over")
        pyautogui.click(*self.buttons["Main City"], clicks=4)

    def farm_mine(self):
        print("FARM MINE")
        x1, y1, x2, y2 = self.main_coords
        pyautogui.click(*self.buttons["Main City"])
        pyautogui.click(*self.sectors["Mine"])
        while True:
            try:
                base_screen_bw = create_screenshot("bgr")
                main_window = base_screen_bw[y1:y2, x1:x2]
                energy_left = get_energy(main_window, self.main_coords)
                is_complete_quests = get_quest_status(main_window, self.main_coords)
                print(f"Energy: {energy_left} | Quests: {is_complete_quests}")
                if energy_left > 0 and is_complete_quests:
                    pyautogui.click(*self.mine_sectors["collect"])
                    sleep(1.5)
                    base_screen_bgr = create_screenshot("bgr")
                    congrats_section = base_screen_bgr[
                        int(y2 - (y2 - y1) * 0.785) : int(y2 - (y2 - y1) * 0.675), x1:x2
                    ]
                    collect_true_section = base_screen_bgr[
                        int(y2 - (y2 - y1) * 0.53) : int(y2 - (y2 - y1) * 0.43), x1:x2
                    ]
                    cong = round(check_congrats(congrats_section), 2)
                    if cong > 0.50:
                        print(f"The congrats window match: {cong} > 0.50")
                        res = detect_text(collect_true_section)
                        for res_item in res:
                            if res_item["text"] in self.config.pp_bot.WHITELIST:
                                print(
                                    "BREAK --> WHITELIST: "
                                    + "\033[1m\033[31m{}".format(res_item["text"])
                                )
                                return True
                        else:
                            print("SUBMIT AND CONTINUE")
                            pyautogui.click(*self.mine_sectors["collect_true_submit"])
                            continue
                    else:
                        print(f"The congrats window match: {cong} < 0.50")
                else:
                    print("IT's OVER")
                    break
            except Exception as exc:
                print(exc)
