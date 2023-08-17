import re
from time import sleep
from random import uniform

import pyautogui
import pytesseract

from services.logger import logger
from config.general import Config, load_config
from services.opencv_helpers import (
    create_screenshot,
    detect_lvl_hero,
    detect_window,
    detect_text,
    get_energy,
    get_quest_status,
    check_congrats,
)


class PPHandlers:
    def __init__(self):
        logger.info("game window: search..")
        base_screen_bgr = create_screenshot("bgr")
        self.main_window, self.main_coords = detect_window(base_screen_bgr)
        logger.info("game window: OK")

        self.config: Config = load_config(self.main_coords)
        pytesseract.pytesseract.tesseract_cmd = self.config.tesseract.path
        pyautogui.PAUSE = uniform(0.25, 0.4)

        self.main_buttons = self.config.pp_bot.main_buttons
        self.sectors = self.config.pp_bot.sectors
        logger.info("load coords: OK")

    def upgrade_hero(self):
        logger.warning(" UPGRADE HERO ".center(40, "-"))
        x1, y1, x2, y2 = self.main_coords
        pyautogui.click(self.main_buttons.main_city.X, self.main_buttons.main_city.Y)
        pyautogui.click(self.main_buttons.heroes.X, self.main_buttons.heroes.Y)
        pyautogui.moveTo(self.sectors.store_purchase.X, self.sectors.store_purchase.Y)
        pyautogui.scroll(clicks=-500)

        logger.info("heroes < 80 lvl: search..")
        sleep(0.5)
        base_screen_bgr = create_screenshot("bgr")
        hero_section = base_screen_bgr[int(y1 + (y2 - y1) * 0.15) : int(y1 + (y2 - y1) * 0.90), x1:x2]
        res = detect_lvl_hero(hero_section)
        res = list(filter(lambda item: re.findall(r"(?:lv\.[1-7][0-9]?$|lv\.[8-9]$|lv\.79$)", item["text"].lower()), res))
        if res:
            logger.info(f"heroes < 80 lvl: {len(res)} pcs.")
            res.sort(key=lambda item: re.findall(r"\.(\d+)", item["text"].lower())[0])
            x_center = res[0]["left"] + res[0]["width"] // 2
            y_center = int((y2 - y1) * 0.15) + (res[0]["top"] + res[0]["height"] // 2)
            pyautogui.click(x1 + x_center, y1 + y_center, interval=1)
            pyautogui.click(self.sectors.upgrade_hero.X, self.sectors.upgrade_hero.Y)
            logger.info("upgrade hero --> DONE")
        else:
            logger.error("heroes < 80 lvl: not found")
        for _ in range(4):
            pyautogui.click(self.main_buttons.main_city.X, self.main_buttons.main_city.Y)

    def claim_free_recruit(self):
        logger.warning(" CLAIM FREE RECRUIT ".center(40, "-"))
        x1, y1, x2, y2 = self.main_coords
        pyautogui.click(self.main_buttons.main_city.X, self.main_buttons.main_city.Y)
        pyautogui.click(self.sectors.recruit.X, self.sectors.recruit.Y)
        logger.info("free recruitment: search..")
        sleep(0.5)
        base_screen_bw = create_screenshot("bgr")
        recruit_section = base_screen_bw[
            int(y1 + (y2 - y1) * 0.877) : int(y1 + (y2 - y1) * 0.90), int(x1 + (x2 - x1) * 0.05) : int(x1 + (x2 - x1) * 0.60)
        ]
        res = detect_text(recruit_section)
        if list(filter(lambda item: re.findall(r"[123]/3", item["text"]), res)) or not res:
            logger.info("free recruitment: is available")
            pyautogui.click(self.sectors.recruit_once.X, self.sectors.recruit_once.Y, interval=8)
            logger.info("claim free recruit --> DONE")
        else:
            logger.error("free recruitment: is NOT available")
        for _ in range(4):
            pyautogui.click(self.main_buttons.main_city.X, self.main_buttons.main_city.Y)

    def claim_free_medal(self):
        logger.warning(" CLAIM FREE MEDAL ".center(40, "-"))
        x1, y1, x2, y2 = self.main_coords
        pyautogui.click(self.main_buttons.main_city.X, self.main_buttons.main_city.Y)
        pyautogui.click(self.sectors.medal_hall.X, self.sectors.medal_hall.Y)
        pyautogui.click(self.main_buttons.conquest.X, self.main_buttons.conquest.Y)
        logger.info("free medal: search..")
        sleep(0.5)
        base_screen_bw = create_screenshot()
        medal_section = base_screen_bw[
            int(y2 - (y2 - y1) * 0.158) : int(y2 - (y2 - y1) * 0.125), int(x1 + (x2 - x1) * 0.03) : int(x1 + (x2 - x1) * 0.60)
        ]
        res = detect_text(medal_section)
        if list(filter(lambda item: item["text"].lower() == "free", res)):
            logger.info("free medal: is available")
            pyautogui.click(self.sectors.recruit_once.X, self.sectors.recruit_once.Y, interval=8)
            logger.info("claim medal --> DONE")
        else:
            logger.error("free medal: is NOT available")
        for _ in range(4):
            pyautogui.click(self.main_buttons.main_city.X, self.main_buttons.main_city.Y)

    def claim_daily_gift(self):
        logger.warning(" CLAIM DAILY GIFT ".center(40, "-"))
        pyautogui.click(self.main_buttons.main_city.X, self.main_buttons.main_city.Y)
        pyautogui.click(self.sectors.gift_pack.X, self.sectors.gift_pack.Y)
        pyautogui.click(self.sectors.gift_claim_free.X, self.sectors.gift_claim_free.Y, interval=3)
        logger.info("claim daily gift --> DONE")
        for _ in range(4):
            pyautogui.click(self.main_buttons.main_city.X, self.main_buttons.main_city.Y)

    def claim_free_expidition(self):
        logger.warning(" CLAIM FREE EXPEDITION ".center(40, "-"))
        pyautogui.click(self.main_buttons.main_city.X, self.main_buttons.main_city.Y)
        pyautogui.click(self.sectors.battles.X, self.sectors.battles.Y)
        pyautogui.click(self.sectors.expedition_road.X, self.sectors.expedition_road.Y)
        pyautogui.click(self.main_buttons.chapter.X, self.main_buttons.chapter.Y)
        pyautogui.click(self.sectors.expedition_road_claim.X, self.sectors.expedition_road_claim.Y, interval=3)
        logger.info("claim free expedition --> DONE")
        for _ in range(4):
            pyautogui.click(self.main_buttons.main_city.X, self.main_buttons.main_city.Y)

    def claim_quick_afk(self):
        logger.warning(" CLAIM QUICK AFK ".center(40, "-"))
        x1, y1, x2, y2 = self.main_coords
        pyautogui.click(self.main_buttons.main_city.X, self.main_buttons.main_city.Y)
        pyautogui.click(self.main_buttons.chapter.X, self.main_buttons.chapter.Y)
        pyautogui.click(self.sectors.chapter_chest_claim.X, self.sectors.chapter_chest_claim.Y)
        pyautogui.click(self.sectors.quick_afk_claim.X, self.sectors.quick_afk_claim.Y, interval=3)
        pyautogui.click(self.main_buttons.main_city.X, self.main_buttons.main_city.Y)

        logger.info("[Quick AFK]: search..")
        sleep(0.5)
        base_screen_bw = create_screenshot()
        quick_buttons = base_screen_bw[int(y1 + (y2 - y1) * 0.64) : int(y1 + (y2 - y1) * 0.87), x1 : int(x1 + (x2 - x1) * 0.15)]
        res = detect_text(quick_buttons)
        res = list(filter(lambda item: item["text"].lower() == "afk", res))
        if res:
            logger.info("[Quick AFK]: were found")
            x_center = res[0]["left"] + res[0]["width"] // 2
            y_center = int((y2 - y1) * 0.64) + (res[0]["top"] + res[0]["height"] // 2)
            pyautogui.click(x1 + x_center, y1 + y_center)
            logger.info("[Free]: search..")
            sleep(1)
            base_screen_bw = create_screenshot()
            free_button = base_screen_bw[
                int(y1 + (y2 - y1) * 0.669) : int(y1 + (y2 - y1) * 0.71), int(x1 + (x2 - x1) * 0.336) : int(x1 + (x2 - x1) * 0.646)
            ]
            res = detect_text(free_button)
            res = list(filter(lambda item: item["text"].lower() == "free", res))
            if res:
                logger.info("[Free]: were found")
                pyautogui.click(self.sectors.quick_afk_claim.X, self.sectors.quick_afk_claim.Y, interval=3)
            else:
                logger.error("[Free]: NOT found")
        else:
            logger.error("[Quick AFK]: NOT found")
        logger.info("quick afk claim --> DONE")
        for _ in range(4):
            pyautogui.click(self.main_buttons.main_city.X, self.main_buttons.main_city.Y)

    def purchase_store_items(self):
        logger.warning(" PURCHASE STORE ITEMS ".center(40, "-"))
        x1, y1, x2, y2 = self.main_coords

        def control_store_missclick():
            sleep(0.5)
            base_screen_bgr = create_screenshot("bgr")
            purchase_section = base_screen_bgr[
                int(y1 + (y2 - y1) * 0.64) : int(y1 + (y2 - y1) * 0.68),
                int(x1 + (x2 - x1) * 0.35) : int(x1 + (x2 - x1) * 0.66),
            ]
            res = detect_text(purchase_section)
            return list(filter(lambda item: item["text"].lower() == "purchase", res))

        pyautogui.click(self.main_buttons.main_city.X, self.main_buttons.main_city.Y)
        pyautogui.click(self.sectors.store.X, self.sectors.store.Y)
        pyautogui.click(self.sectors.store_recruitment_card.X, self.sectors.store_recruitment_card.Y)
        if control_store_missclick():
            pyautogui.click(self.sectors.store_purchase.X, self.sectors.store_purchase.Y, interval=3)
            logger.info("purchase: Recruitment Card --> DONE")
        else:
            logger.error("purchase: Recruitment Card --> FAILED")
        for _ in range(2):
            pyautogui.click(self.sectors.store_5_star_hero_fragment.X, self.sectors.store_5_star_hero_fragment.Y)
        if control_store_missclick():
            for _ in range(5):
                pyautogui.click(self.sectors.store_add_count.X, self.sectors.store_add_count.Y, interval=0.15)
            pyautogui.click(self.sectors.store_purchase.X, self.sectors.store_purchase.Y, interval=3)
            logger.info("purchase: 5 star Hero Fragment --> DONE")
        else:
            logger.error("purchase: 5 star Hero Fragment --> FAILED")
        for _ in range(4):
            pyautogui.click(self.main_buttons.main_city.X, self.main_buttons.main_city.Y)

    def legion_donate(self):
        logger.warning(" LEGION DONATE ".center(40, "-"))
        pyautogui.click(self.main_buttons.main_city.X, self.main_buttons.main_city.Y)
        pyautogui.click(self.sectors.legion.X, self.sectors.legion.Y)
        pyautogui.click(self.sectors.legion_upgrade.X, self.sectors.legion_upgrade.Y)
        pyautogui.click(self.sectors.legion_donate.X, self.sectors.legion_donate.Y, interval=3)
        logger.info("legion donate --> DONE")
        for _ in range(5):
            pyautogui.click(self.main_buttons.main_city.X, self.main_buttons.main_city.Y)

    def purchase_legion_items(self):
        logger.warning(" PURCHASE LEGION ITEMS ".center(40, "-"))
        pyautogui.click(self.main_buttons.main_city.X, self.main_buttons.main_city.Y)
        pyautogui.click(self.sectors.legion.X, self.sectors.legion.Y)
        pyautogui.click(self.sectors.legion_store.X, self.sectors.legion_store.Y)
        pyautogui.moveTo(self.sectors.store_purchase.X, self.sectors.store_purchase.Y)
        pyautogui.scroll(clicks=-150)
        sleep(0.5)
        pyautogui.click(self.sectors.legion_5_star_hero_fragment.X, self.sectors.legion_5_star_hero_fragment.Y)
        for _ in range(5):
            pyautogui.click(self.sectors.store_add_count.X, self.sectors.store_add_count.Y, interval=0.15)
        pyautogui.click(self.sectors.store_purchase.X, self.sectors.store_purchase.Y, interval=3)
        logger.info("purchase legion items --> DONE")
        for _ in range(5):
            pyautogui.click(self.main_buttons.main_city.X, self.main_buttons.main_city.Y)

    def join_to_arena(self):
        logger.info(" JOIN TO ARENA ".center(40, "-"))
        pyautogui.click(self.main_buttons.main_city.X, self.main_buttons.main_city.Y)
        pyautogui.click(self.main_buttons.arena.X, self.main_buttons.arena.Y)
        pyautogui.click(self.sectors.arena_challenge.X, self.sectors.arena_challenge.Y)
        pyautogui.click(self.sectors.arena_challenge.X, self.sectors.arena_challenge.Y, interval=2)
        pyautogui.click(self.main_buttons.ranking.X, self.main_buttons.ranking.Y, interval=17)
        pyautogui.click(self.sectors.arena_skip.X, self.sectors.arena_skip.Y)
        logger.info("area battle --> DONE")
        for _ in range(4):
            pyautogui.click(self.main_buttons.main_city.X, self.main_buttons.main_city.Y)

    def joit_to_chapter(self):
        logger.warning(" JOIN TO CHAPTER ".center(40, "-"))
        x1, y1, x2, y2 = self.main_coords
        pyautogui.click(self.main_buttons.main_city.X, self.main_buttons.main_city.Y)
        pyautogui.click(self.main_buttons.chapter.X, self.main_buttons.chapter.Y)
        logger.info("[Auto Challenge]: search..")
        sleep(0.5)
        base_screen_bw = create_screenshot()
        chapter_buttons = base_screen_bw[int(y1 + (y2 - y1) * 0.64) : int(y1 + (y2 - y1) * 0.87), x1 : int(x1 + (x2 - x1) * 0.15)]
        res = detect_text(chapter_buttons)
        res = list(filter(lambda item: item["text"].lower() == "auto", res))
        if res:
            x_center = res[0]["left"] + res[0]["width"] // 2
            y_center = int(int(y2 - y1) * 0.64) + (res[0]["top"] + res[0]["height"] // 2)
            pyautogui.click(x1 + x_center, y1 + y_center)
            logger.info("[Auto Challenge]: were found")
            while True:
                sleep(5)
                pyautogui.click(self.main_buttons.chapter.X, self.main_buttons.chapter.Y)
                sleep(0.5)
                base_screen_bgr = create_screenshot("bgr")
                challenge_button = base_screen_bgr[
                    int(y1 + (y2 - y1) * 0.83) : int(y1 + (y2 - y1) * 0.87),
                    int(x1 + (x2 - x1) * 0.38) : int(x1 + (x2 - x1) * 0.62),
                ]
                res = detect_text(challenge_button)
                if list(filter(lambda item: item["text"].lower() == "challenge", res)):
                    logger.info("battle: is OVER")
                    break
                else:
                    logger.info("battle: is NOT over")
        else:
            logger.warning("[Auto Challenge]: not found")
        for _ in range(4):
            pyautogui.click(self.main_buttons.main_city.X, self.main_buttons.main_city.Y)

    def joit_to_relics(self):
        logger.warning(" JOIN TO RELICS ".center(40, "-"))
        x1, y1, x2, y2 = self.main_coords
        pyautogui.click(self.main_buttons.main_city.X, self.main_buttons.main_city.Y)
        pyautogui.click(self.sectors.battles.X, self.sectors.battles.Y)
        pyautogui.click(self.sectors.relics_exploration.X, self.sectors.relics_exploration.Y)
        pyautogui.click(self.sectors.relics_first_right_challenge.X, self.sectors.relics_first_right_challenge.Y)
        pyautogui.click(self.sectors.relics_first_right_challenge.X, self.sectors.relics_first_right_challenge.Y)  # accept

        # if the right relics is not started battle
        pyautogui.click(self.main_buttons.chapter.X, self.main_buttons.chapter.Y)
        pyautogui.click(self.sectors.relics_first_left_challenge.X, self.sectors.relics_first_left_challenge.Y)
        pyautogui.click(self.sectors.relics_first_right_challenge.X, self.sectors.relics_first_right_challenge.Y)  # accept

        while True:
            sleep(5)
            pyautogui.click(self.main_buttons.chapter.X, self.main_buttons.chapter.Y)
            sleep(0.5)
            base_screen_bgr = create_screenshot("bgr")
            title_section = base_screen_bgr[
                int(y2 - (y2 - y1) * 0.97) : int(y2 - (y2 - y1) * 0.88),
                int(x1 + (x2 - x1) * 0.2) : int(x1 + (x2 - x1) * 0.8),
            ]
            res = detect_text(title_section)
            if list(filter(lambda item: item["text"].lower() in ["relic", "exploration"], res)):
                logger.info("battle: is over")
                break
            else:
                logger.info("battle: is NOT over")
        for _ in range(5):
            pyautogui.click(self.main_buttons.main_city.X, self.main_buttons.main_city.Y)

    def claim_mission(self):
        logger.warning(" CLAIM MISSION ".center(40, "-"))
        x1, y1, x2, y2 = self.main_coords
        pyautogui.click(self.main_buttons.main_city.X, self.main_buttons.main_city.Y)
        pyautogui.click(self.sectors.mission.X, self.sectors.mission.Y)
        for _ in range(11):
            logger.info("[Claim]: search..")
            sleep(0.5)
            base_screen_bgr = create_screenshot("bgr")
            claim_section = base_screen_bgr[
                int(y1 + (y2 - y1) * 0.40) : int(y1 + (y2 - y1) * 0.43),
                int(x1 + (x2 - x1) * 0.79) : int(x1 + (x2 - x1) * 0.96),
            ]
            res = detect_text(claim_section)
            if list(filter(lambda item: item["text"].lower() == "claim", res)):
                pyautogui.click(self.sectors.claim_mission.X, self.sectors.claim_mission.Y, interval=2)
                pyautogui.click(
                    self.sectors.claim_mission.X,
                    self.sectors.claim_mission.Y,
                )
                logger.info("[Claim]: is avalaible")
            else:
                logger.error("[Claim]: is NOT avalaible")
                break
        pyautogui.click(self.sectors.mission_box_1.X, self.sectors.mission_box_1.Y, interval=3)
        pyautogui.click(self.sectors.mission_box_2.X, self.sectors.mission_box_2.Y)
        pyautogui.click(self.sectors.mission_box_2.X, self.sectors.mission_box_2.Y, interval=3)
        pyautogui.click(self.sectors.mission_box_3.X, self.sectors.mission_box_3.Y)
        pyautogui.click(self.sectors.mission_box_3.X, self.sectors.mission_box_3.Y, interval=3)
        pyautogui.click(self.sectors.mission_box_4.X, self.sectors.mission_box_4.Y)
        pyautogui.click(self.sectors.mission_box_4.X, self.sectors.mission_box_4.Y, interval=3)
        pyautogui.click(self.sectors.mission_box_5.X, self.sectors.mission_box_5.Y)
        pyautogui.click(self.sectors.mission_box_5.X, self.sectors.mission_box_5.Y, interval=3)
        for _ in range(4):
            pyautogui.click(self.main_buttons.main_city.X, self.main_buttons.main_city.Y)

    def farm_mine(self, farm_mine_count):
        logger.warning(" FARM MINE ".center(40, "-"))
        x1, y1, x2, y2 = self.main_coords
        pyautogui.click(self.main_buttons.main_city.X, self.main_buttons.main_city.Y)
        pyautogui.click(self.sectors.mine.X, self.sectors.mine.Y)
        sleep(0.5)
        temp_energy = 999
        while True:
            try:
                base_screen_bw = create_screenshot("bgr")
                main_window = base_screen_bw[y1:y2, x1:x2]
                res, energy_left = get_energy(main_window, self.main_coords)
                is_complete_quests = get_quest_status(main_window, self.main_coords)
                if res:
                    logger.info(f"energy: {energy_left} | quests: {'is avalaible' if is_complete_quests else 'is NOT avalaible'}")
                    if is_complete_quests or (energy_left > 0 and farm_mine_count > 0):
                        if temp_energy > energy_left and farm_mine_count >= 0:
                            temp_energy = energy_left
                            farm_mine_count -= 1
                        pyautogui.click(self.sectors.mine_collect.X, self.sectors.mine_collect.Y)
                        sleep(3)
                        base_screen_bgr = create_screenshot("bgr")
                        congrats_section = base_screen_bgr[int(y2 - (y2 - y1) * 0.785) : int(y2 - (y2 - y1) * 0.675), x1:x2]
                        collect_true_section = base_screen_bgr[int(y2 - (y2 - y1) * 0.53) : int(y2 - (y2 - y1) * 0.43), x1:x2]
                        cong = round(check_congrats(congrats_section), 2)
                        if cong > 0.50:
                            logger.info(f"congrats match: {cong} > 0.50")
                            res = detect_text(collect_true_section)
                            for res_item in res:
                                if res_item["text"] in self.config.pp_bot.WHITELIST:
                                    logger.warning("BREAK --> WHITELIST: " + "\033[1m\033[31m{}".format(res_item["text"]))
                                    return True
                            else:
                                logger.info("submit")
                                pyautogui.click(self.sectors.mine_collect_submit.X, self.sectors.mine_collect_submit.Y)
                                continue
                        else:
                            logger.info(f"congrats match: {cong} < 0.50")

                    else:
                        logger.warning("BOT STOPPED")
                        break
                else:
                    logger.info("energy: not found --> repeat")
                    pyautogui.click(self.main_buttons.chapter.X, self.main_buttons.chapter.Y)
                    sleep(1)

            except Exception as exc:
                logger.error(exc)
