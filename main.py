import threading
import os
from time import sleep

import tkinter as tk
import keyboard

from handlers.ultragem import PPHandlers
from services.logger import logger

COUNT = 3

root = tk.Tk()
root.overrideredirect(1)
root.attributes("-topmost", True)
timer_label = tk.Label()
timer_label.pack()


class FunctionSelectionWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        font = ("calibri", 12, "bold")
        self.title("PP_bot config")
        try:
            self.iconbitmap("static/favicon.ico")
        except Exception as exc:
            print(exc)
        self.checkbox_var_select_all = tk.IntVar(value=0)
        self.checkbox_var_upgrade_hero = tk.IntVar(value=0)
        self.checkbox_var_claim_free_recruit = tk.IntVar(value=0)
        self.checkbox_var_claim_free_medal = tk.IntVar(value=0)
        self.checkbox_var_claim_daily_gift = tk.IntVar(value=0)
        self.checkbox_var_claim_free_expidition = tk.IntVar(value=0)
        self.checkbox_var_claim_quick_afk = tk.IntVar(value=0)
        self.checkbox_var_purchase_store_items = tk.IntVar(value=0)
        self.checkbox_var_legion_donate = tk.IntVar(value=0)
        self.checkbox_var_purchase_legion_items = tk.IntVar(value=0)
        self.checkbox_var_join_to_arena = tk.IntVar(value=0)
        self.checkbox_var_join_to_chapter = tk.IntVar(value=0)
        self.checkbox_var_join_to_relics = tk.IntVar(value=0)
        self.checkbox_var_claim_mission = tk.IntVar(value=0)
        self.checkbox_var_farm_mine = tk.IntVar(value=1)

        entry_var_join_to_arena = tk.StringVar()
        self.join_to_arena_entry = tk.Entry(
            self,
            font=font,
            textvariable=entry_var_join_to_arena,
            width=5,
            bg="light gray",
            validate="key",
        )
        self.join_to_arena_entry.insert(0, "1")
        self.join_to_arena_entry.grid(row=10, column=1, sticky="e", padx=(5, 10))

        entry_var_farm_mine = tk.StringVar()
        self.farm_mine_entry = tk.Entry(
            self,
            font=font,
            textvariable=entry_var_farm_mine,
            width=5,
            bg="light gray",
            validate="key",
        )
        self.farm_mine_entry.insert(0, "0")
        self.farm_mine_entry.grid(row=14, column=1, sticky="e", padx=(5, 10))

        def on_validate_join_to_arena(input_text):
            if all(char.isdigit() for char in input_text) and input_text and input_text != "0":
                self.join_to_arena_entry.config({"background": "light gray"})
            else:
                self.join_to_arena_entry.config({"background": "red"})

        def on_validate_farm_mine(input_text):
            if all(char.isdigit() for char in input_text) or not input_text:
                self.farm_mine_entry.config({"background": "light gray"})
            else:
                self.farm_mine_entry.config({"background": "red"})

        entry_var_join_to_arena.trace_add(
            "write", lambda name, index, mode, sv=entry_var_join_to_arena: on_validate_join_to_arena(sv.get())
        )
        entry_var_farm_mine.trace_add("write", lambda name, index, mode, sv=entry_var_farm_mine: on_validate_farm_mine(sv.get()))

        self.checkbox_select_all = tk.Checkbutton(
            self,
            text="ВИБРАТИ ВСІ" + " " * 30,
            variable=self.checkbox_var_select_all,
            font=font,
            background="aqua",
            command=self.toggle_select_all,
        )
        self.checkbox_select_all.grid(row=0, column=0, columnspan=2, sticky="w")
        self.checkbox_upgrade_hero = tk.Checkbutton(
            self,
            text="UPGRADE HERO",
            variable=self.checkbox_var_upgrade_hero,
            font=font,
        )
        self.checkbox_upgrade_hero.grid(row=1, column=0, columnspan=2, sticky="w")
        self.checkbox_claim_free_recruit = tk.Checkbutton(
            self,
            text="CLAIM FREE RECRUIT",
            variable=self.checkbox_var_claim_free_recruit,
            font=font,
        )
        self.checkbox_claim_free_recruit.grid(row=2, column=0, columnspan=2, sticky="w")
        self.checkbox_claim_free_medal = tk.Checkbutton(
            self,
            text="CLAIM FREE MEDAL",
            variable=self.checkbox_var_claim_free_medal,
            font=font,
        )
        self.checkbox_claim_free_medal.grid(row=3, column=0, columnspan=2, sticky="w")
        self.checkbox_claim_daily_gift = tk.Checkbutton(
            self,
            text="CLAIM DAILY GIFT",
            variable=self.checkbox_var_claim_daily_gift,
            font=font,
        )
        self.checkbox_claim_daily_gift.grid(row=4, column=0, columnspan=2, sticky="w")
        self.checkbox_claim_free_expidition = tk.Checkbutton(
            self,
            text="CLAIM FREE EXPIDITION",
            variable=self.checkbox_var_claim_free_expidition,
            font=font,
        )
        self.checkbox_claim_free_expidition.grid(row=5, column=0, columnspan=2, sticky="w")
        self.checkbox_claim_quick_afk = tk.Checkbutton(
            self,
            text="CLAIM QUICK AFK",
            variable=self.checkbox_var_claim_quick_afk,
            font=font,
        )
        self.checkbox_claim_quick_afk.grid(row=6, column=0, columnspan=2, sticky="w")
        self.checkbox_purchase_store_items = tk.Checkbutton(
            self,
            text="PURCHASE STORE ITEMS",
            variable=self.checkbox_var_purchase_store_items,
            font=font,
        )
        self.checkbox_purchase_store_items.grid(row=7, column=0, columnspan=2, sticky="w")
        self.checkbox_legion_donate = tk.Checkbutton(
            self,
            text="LEGION DONATE",
            variable=self.checkbox_var_legion_donate,
            font=font,
        )
        self.checkbox_legion_donate.grid(row=8, column=0, columnspan=2, sticky="w")
        self.checkbox_purchase_legion_items = tk.Checkbutton(
            self,
            text="PURCHASE LEGION ITEMS",
            variable=self.checkbox_var_purchase_legion_items,
            font=font,
        )
        self.checkbox_purchase_legion_items.grid(row=9, column=0, columnspan=2, sticky="w")
        self.checkbox_join_to_arena = tk.Checkbutton(
            self,
            text="JOIN TO ARENA:",
            variable=self.checkbox_var_join_to_arena,
            font=font,
        )
        self.checkbox_join_to_arena.grid(row=10, column=0, sticky="w")
        self.checkbox_join_to_chapter = tk.Checkbutton(
            self,
            text="JOIN TO CHAPTER",
            variable=self.checkbox_var_join_to_chapter,
            font=font,
        )
        self.checkbox_join_to_chapter.grid(row=11, column=0, columnspan=2, sticky="w")
        self.checkbox_join_to_relics = tk.Checkbutton(
            self,
            text="JOIN TO RELICS",
            variable=self.checkbox_var_join_to_relics,
            font=font,
        )
        self.checkbox_join_to_relics.grid(row=12, column=0, columnspan=2, sticky="w")
        self.checkbox_claim_mission = tk.Checkbutton(
            self,
            text="CLAIM MISSION",
            variable=self.checkbox_var_claim_mission,
            font=font,
        )
        self.checkbox_claim_mission.grid(row=13, column=0, columnspan=2, sticky="w")
        self.checkbox_claim_farm_mine = tk.Checkbutton(
            self,
            text="FARM MINE" + " " * 19,
            background="yellow",
            variable=self.checkbox_var_farm_mine,
            font=font,
        )
        self.checkbox_claim_farm_mine.grid(row=14, column=0, columnspan=2, sticky="w")

        self.start_button = tk.Button(
            self,
            text="Почати",
            bg="green",
            fg="white",
            font=font,
            command=self.countdown,
        )
        self.start_button.grid(row=15, column=0, padx=(10, 5), pady=(15, 5), sticky="w")

        self.exit_button = tk.Button(
            self,
            text="Закрити",
            bg="brown",
            fg="white",
            font=font,
            command=self.master.destroy,
        )
        self.exit_button.grid(row=15, column=1, padx=(5, 10), pady=(15, 5), sticky="e")

        self.protocol("WM_DELETE_WINDOW", self.master.destroy)

    def toggle_select_all(self):
        select_all_value = self.checkbox_var_select_all.get()
        self.checkbox_var_claim_free_recruit.set(select_all_value)
        self.checkbox_var_claim_free_medal.set(select_all_value)
        self.checkbox_var_claim_daily_gift.set(select_all_value)
        self.checkbox_var_claim_free_expidition.set(select_all_value)
        self.checkbox_var_claim_quick_afk.set(select_all_value)
        self.checkbox_var_purchase_store_items.set(select_all_value)
        self.checkbox_var_legion_donate.set(select_all_value)
        self.checkbox_var_purchase_legion_items.set(select_all_value)
        self.checkbox_var_join_to_arena.set(select_all_value)
        self.checkbox_var_join_to_relics.set(select_all_value)
        self.checkbox_var_join_to_chapter.set(select_all_value)
        self.checkbox_var_claim_mission.set(select_all_value)
        self.checkbox_var_farm_mine.set(select_all_value)
        self.checkbox_var_upgrade_hero.set(select_all_value)

    def run_selected_functions(self):
        pp_handlers = PPHandlers()
        if self.checkbox_var_upgrade_hero.get():
            pp_handlers.upgrade_hero()
        if self.checkbox_var_claim_free_recruit.get():
            pp_handlers.claim_free_recruit()
        if self.checkbox_var_claim_free_medal.get():
            pp_handlers.claim_free_medal()
        if self.checkbox_var_claim_daily_gift.get():
            pp_handlers.claim_daily_gift()
        if self.checkbox_var_claim_free_expidition.get():
            pp_handlers.claim_free_expidition()
        if self.checkbox_var_claim_quick_afk.get():
            pp_handlers.claim_quick_afk()
        if self.checkbox_var_purchase_store_items.get():
            pp_handlers.purchase_store_items()
        if self.checkbox_var_legion_donate.get():
            pp_handlers.legion_donate()
        if self.checkbox_var_purchase_legion_items.get():
            pp_handlers.purchase_legion_items()
        if self.checkbox_var_join_to_arena.get():
            try:
                join_to_arena_count = int(self.join_to_arena_count)
            except Exception:
                logger.error("JOINT TO ARENA count not found: set to 1")
                join_to_arena_count = 1
            for _ in range(join_to_arena_count):
                pp_handlers.join_to_arena()
        if self.checkbox_var_join_to_chapter.get():
            pp_handlers.joit_to_chapter()
        if self.checkbox_var_join_to_relics.get():
            pp_handlers.joit_to_relics()
        if self.checkbox_var_claim_mission.get():
            pp_handlers.claim_mission()
        if self.checkbox_var_farm_mine.get():
            try:
                farm_mine_count = int(self.farm_mine_count)
            except Exception as exc:
                print(exc)
                farm_mine_count = 0
            pp_handlers.farm_mine(farm_mine_count)
        self.master.destroy()

    def countdown(self):
        global COUNT
        if self.winfo_exists():
            self.join_to_arena_count = self.join_to_arena_entry.get()
            self.farm_mine_count = self.farm_mine_entry.get()
            self.destroy()

        if COUNT > 0:
            logger.info(f"{COUNT} seconds left")
            timer_label.config(text=str(COUNT), font=("calibri", 60, "bold"), bg="black", fg="red")
            timer_label.after(1000, self.countdown)
            COUNT -= 1
        else:
            logger.warning(f" BOT IS STARTED ".center(30, "*"))
            timer_label.config(text="BOT ON", font=("calibri", 30, "bold"), bg="blue", fg="yellow")
            timer_label.after(1000, self.run_selected_functions)


def exit_on_esc():
    while True:
        sleep(1)
        if keyboard.is_pressed("esc"):
            current_pid = os.getpid()
            logger.critical(f"pressed the [ESC] and killed the pid: {current_pid}")
            os.kill(current_pid, 15)  # 15 - control kill /  9 force kill


def main():
    FunctionSelectionWindow(root)

    exit_thread = threading.Thread(target=exit_on_esc)
    exit_thread.daemon = True
    exit_thread.start()

    root.mainloop()


if __name__ == "__main__":
    main()
