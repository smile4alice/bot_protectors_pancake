from dataclasses import dataclass


@dataclass
class Point:
    X: int
    Y: int

    def to_tuple(self):
        return (self.x, self.y)


@dataclass
class MainButtons:
    main_city: Point
    heroes: Point
    backpack: Point
    chapter: Point
    arena: Point
    ranking: Point
    conquest: Point


@dataclass
class Sectors:
    upgrade_hero: Point
    recruit: Point
    recruit_once: Point
    medal_hall: Point
    gift_pack: Point
    gift_claim_free: Point
    battles: Point
    expedition_road: Point
    expedition_road_claim: Point
    quick_afk_claim: Point
    chapter_chest_claim: Point
    store: Point
    store_5_star_hero_fragment: Point
    store_recruitment_card: Point
    store_add_count: Point
    store_purchase: Point
    legion: Point
    legion_store: Point
    legion_5_star_hero_fragment: Point
    legion_upgrade: Point
    legion_donate: Point
    arena_challenge: Point
    arena_skip: Point
    relics_exploration: Point
    relics_first_right_challenge: Point
    relics_first_left_challenge: Point
    mission: Point
    claim_mission: Point
    mission_box_1: Point
    mission_box_2: Point
    mission_box_3: Point
    mission_box_4: Point
    mission_box_5: Point
    mine: Point
    mine_collect: Point
    mine_collect_submit: Point


def load_coords(main_coords) -> dict[MainButtons, Sectors]:
    x1, y1, x2, y2 = main_coords
    return {
        "main_buttons": MainButtons(
            main_city=Point(
                int(x1 + (x2 - x1) * 0.0698),
                int(y1 + (y2 - y1) * 0.959),
            ),
            heroes=Point(
                int(x1 + (x2 - x1) * 0.216),
                int(y1 + (y2 - y1) * 0.959),
            ),
            backpack=Point(
                int(x1 + (x2 - x1) * 0.355),
                int(y1 + (y2 - y1) * 0.959),
            ),
            chapter=Point(
                int(x1 + (x2 - x1) * 0.485),
                int(y1 + (y2 - y1) * 0.959),
            ),
            arena=Point(
                int(x1 + (x2 - x1) * 0.645),
                int(y1 + (y2 - y1) * 0.959),
            ),
            ranking=Point(
                int(x1 + (x2 - x1) * 0.79),
                int(y1 + (y2 - y1) * 0.959),
            ),
            conquest=Point(
                int(x1 + (x2 - x1) * 0.935),
                int(y1 + (y2 - y1) * 0.959),
            ),
        ),
        "sectors": Sectors(
            upgrade_hero=Point(
                int(x1 + (x2 - x1) * 0.516),
                int(y1 + (y2 - y1) * 0.882),
            ),
            recruit=Point(
                int(x1 + (x2 - x1) * 0.40),
                int(y1 + (y2 - y1) * 0.50),
            ),
            recruit_once=Point(
                int(x1 + (x2 - x1) * 0.27),
                int(y1 + (y2 - y1) * 0.83),
            ),
            medal_hall=Point(
                int(x1 + (x2 - x1) * 0.23),
                int(y1 + (y2 - y1) * 0.40),
            ),
            gift_pack=Point(
                int(x1 + (x2 - x1) * 0.91),
                int(y1 + (y2 - y1) * 0.15),
            ),
            gift_claim_free=Point(  # Gift Pack Free #TODO
                int(x1 + (x2 - x1) * 0.23),
                int(y1 + (y2 - y1) * 0.38),
            ),
            battles=Point(
                int(x1 + (x2 - x1) * 0.65),
                int(y1 + (y2 - y1) * 0.15),
            ),
            expedition_road=Point(
                int(x1 + (x2 - x1) * 0.75),
                int(y1 + (y2 - y1) * 0.70),
            ),
            expedition_road_claim=Point(
                int(x1 + (x2 - x1) * 0.48),
                int(y2 - (y2 - y1) * 0.37),
            ),
            quick_afk_claim=Point(
                int(x1 + (x2 - x1) * 0.48),
                int(y1 + (y2 - y1) * 0.70),
            ),
            chapter_chest_claim=Point(
                int(x1 + (x2 - x1) * 0.84),
                int(y1 + (y2 - y1) * 0.80),
            ),
            store=Point(
                int(x1 + (x2 - x1) * 0.75),
                int(y1 + (y2 - y1) * 0.28),
            ),
            store_5_star_hero_fragment=Point(
                int(x1 + (x2 - x1) * 0.20),
                int(y1 + (y2 - y1) * 0.70),
            ),
            store_recruitment_card=Point(
                int(x1 + (x2 - x1) * 0.81),
                int(y1 + (y2 - y1) * 0.45),
            ),
            store_add_count=Point(
                int(x1 + (x2 - x1) * 0.61),
                int(y1 + (y2 - y1) * 0.52),
            ),
            store_purchase=Point(
                int(x1 + (x2 - x1) * 0.48),
                int(y1 + (y2 - y1) * 0.65),
            ),
            legion=Point(
                int(x1 + (x2 - x1) * 0.45),
                int(y1 + (y2 - y1) * 0.25),
            ),
            legion_store=Point(
                int(x1 + (x2 - x1) * 0.23),
                int(y1 + (y2 - y1) * 0.40),
            ),
            legion_5_star_hero_fragment=Point(
                int(x1 + (x2 - x1) * 0.50),
                int(y1 + (y2 - y1) * 0.865),
            ),
            legion_upgrade=Point(
                int(x1 + (x2 - x1) * 0.69),
                int(y1 + (y2 - y1) * 0.72),
            ),
            legion_donate=Point(
                int(x1 + (x2 - x1) * 0.79),
                int(y1 + (y2 - y1) * 0.82),
            ),
            arena_challenge=Point(
                int(x1 + (x2 - x1) * 0.57),
                int(y1 + (y2 - y1) * 0.66),
            ),
            arena_skip=Point(
                int(x1 + (x2 - x1) * 0.095),
                int(y1 + (y2 - y1) * 0.84),
            ),
            relics_exploration=Point(
                int(x1 + (x2 - x1) * 0.72),
                int(y1 + (y2 - y1) * 0.30),
            ),
            relics_first_right_challenge=Point(
                int(x1 + (x2 - x1) * 0.655),
                int(y1 + (y2 - y1) * 0.775),
            ),
            relics_first_left_challenge=Point(
                int(x1 + (x2 - x1) * 0.37),
                int(y1 + (y2 - y1) * 0.726),
            ),
            mission=Point(
                int(x1 + (x2 - x1) * 0.08),
                int(y1 + (y2 - y1) * 0.12),
            ),
            claim_mission=Point(
                int(x1 + (x2 - x1) * 0.85),
                int(y1 + (y2 - y1) * 0.41),
            ),
            mission_box_1=Point(
                int(x1 + (x2 - x1) * 0.28),
                int(y1 + (y2 - y1) * 0.32),
            ),
            mission_box_2=Point(
                int(x1 + (x2 - x1) * 0.44),
                int(y1 + (y2 - y1) * 0.32),
            ),
            mission_box_3=Point(
                int(x1 + (x2 - x1) * 0.64),
                int(y1 + (y2 - y1) * 0.32),
            ),
            mission_box_4=Point(
                int(x1 + (x2 - x1) * 0.80),
                int(y1 + (y2 - y1) * 0.32),
            ),
            mission_box_5=Point(
                int(x1 + (x2 - x1) * 0.95),
                int(y1 + (y2 - y1) * 0.32),
            ),
            mine=Point(
                int(x1 + (x2 - x1) * 0.40),
                int(y1 + (y2 - y1) * 0.86),
            ),
            mine_collect=Point(
                int(x1 + (x2 - x1) * 0.50),
                int(y1 + (y2 - y1) * 0.60),
            ),
            mine_collect_submit=Point(
                int(x1 + (x2 - x1) * 0.38),
                int(y1 + (y2 - y1) * 0.73),
            ),
        ),
    }
