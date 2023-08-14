from typing import List
import cv2
import pyautogui
import numpy as np

import sys
import pytesseract
import cv2


def create_screenshot(mode: str | None = None) -> np.ndarray:
    base_screen = np.array(pyautogui.screenshot())
    if mode == "bgr":
        return cv2.cvtColor(base_screen, cv2.COLOR_RGB2BGR)
    else:
        return cv2.cvtColor(base_screen, cv2.COLOR_RGB2GRAY)


def detect_window(base_screen_bgr: np.ndarray) -> np.ndarray:
    try:
        base_screen_hsv = cv2.cvtColor(base_screen_bgr, cv2.COLOR_BGR2HSV)
        upper = np.array([135, 255, 255])
        lower = np.array([130, 125, 30])
        mask = cv2.inRange(base_screen_hsv, lower, upper)
        ret, threshhold4 = cv2.threshold(mask, 125, 255, cv2.THRESH_TOZERO)

        countours, h = cv2.findContours(
            threshhold4, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
        )
        window_points = []
        for contour in countours:
            if cv2.contourArea(contour) > 300:
                x, y, w, h = cv2.boundingRect(contour)
                window_points.append((x, y, x + w, y + h))

        window_points = sorted(
            window_points, key=lambda item: item[3] - item[1], reverse=True
        )
        x1 = window_points[1][2]
        y1 = window_points[1][1]
        x2 = window_points[0][0]
        y2 = window_points[0][3]
        return base_screen_bgr[y1:y2, x1:x2], (x1, y1, x2, y2)
    except Exception as exc:
        print(f"Вікно не було знайдено: {exc}")
        sys.exit()


def detect_numbers_on_energy(img, psm: int = 6) -> List[dict]:
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    scale_percent = 800
    width = int(img_gray.shape[1] * scale_percent / 100)
    height = int(img_gray.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized_img = cv2.resize(img_gray, dim, interpolation=cv2.INTER_CUBIC)
    blur_img = cv2.GaussianBlur(resized_img, (9, 9), 0)
    upper = np.array([104, 255, 255])
    lower = np.array([100, 5, 187])
    mask = cv2.inRange(blur_img, lower, upper)

    kernel_open = np.ones((5, 5), np.uint8)
    kernel_close = np.ones((3, 3), np.uint8)
    thresh, new_img = cv2.threshold(
        mask, 160, 255, 1, cv2.THRESH_OTSU | cv2.THRESH_BINARY
    )
    blur_img = cv2.medianBlur(new_img, 5)
    opening = cv2.morphologyEx(blur_img, cv2.MORPH_OPEN, kernel_open)
    close = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel_close)

    new_img = cv2.bitwise_not(close)
    custom_config = f"--oem 3 --psm {psm} -c tessedit_char_whitelist=0123456789/"
    data = pytesseract.image_to_data(new_img, lang="eng", config=custom_config)
    result = list()
    for number, el in enumerate(data.splitlines()):
        if number == 0:
            continue
        el = el.split()
        if el[10] != "-1":
            result.append(
                {
                    "left": el[6],
                    "top": el[7],
                    "width": el[8],
                    "height": el[9],
                    "text": el[11] if len(el) > 11 else None,
                }
            )
    return result


def detect_text(
    img, threshold: float = 15, psm: int = 6, allowlist: list = None
) -> List[str]:
    scale_percent = 500
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized_img = cv2.resize(img, dim, interpolation=cv2.INTER_CUBIC)
    blur_img = cv2.GaussianBlur(resized_img, (3, 3), 0)
    blur_img = cv2.medianBlur(blur_img, 5)
    ret, threshold_image = cv2.threshold(
        blur_img, 154, 255, 3, cv2.THRESH_OTSU | cv2.THRESH_BINARY
    )
    config = f"--oem 3 --psm {psm}{(' -c tessedit_char_whitelist=' + ('').join(allowlist)) if allowlist else ''}"
    data = pytesseract.image_to_data(threshold_image, config=config, lang="eng")
    result = list()
    for number, el in enumerate(data.splitlines()):
        if number == 0:
            continue
        el = el.split()
        if float(el[10]) > threshold:
            result.append(
                {
                    "left": el[6],
                    "top": el[7],
                    "width": el[8],
                    "height": el[9],
                    "text": el[11] if len(el) > 11 else None,
                }
            )
    return result


def move_to_text(main_coords, text_point):
    x1, y1, x2, y2 = main_coords
    x_avg, y_avg = text_point
    pyautogui.moveTo(x_avg + x1, y_avg + y1)


def get_energy(main_window, main_coords):
    x1, y1, x2, y2 = main_coords
    energy_section = main_window[
        0 : int((y2 - y1) * 0.0337), int((x2 - x1) * 0.397) : int((x2 - x1) * 0.51)
    ]
    result: list = detect_numbers_on_energy(energy_section)
    try:
        energy = result[0]["text"].split("/")[0]
        # x_center = int(result[0]["left"]) + int(result[0]["width"]) // 2
        # y_center = int(result[0]["top"]) + int(result[0]["height"]) // 2
        # move_to_text(main_coords, (x_center, y_center))
        return int(energy)
    except Exception:
        print(f"Енергії в даній області не знайдено {result}")


def get_quest_status(main_window, main_coords):
    x1, y1, x2, y2 = main_coords
    quest_section = main_window[
        int((y2 - y1) * 0.47) : int((y2 - y1) * 0.59),
        int((x2 - x1) * 0.89) : int((x2 - x1) * 0.97),
    ]
    result: list = detect_text(
        quest_section, allowlist=[str(i) for i in range(10)] + ["/"]
    )
    try:
        quest_status = [i["text"] for i in result]
        return bool(quest_status)
    except Exception:
        print(f"Не вдалося отримати статус {result}")


def check_congrats(src):
    template_bgr = cv2.imread("static/templates/congrats.png")
    width1 = src.shape[1]
    height1 = src.shape[0]
    width2 = template_bgr.shape[1]
    height2 = template_bgr.shape[0]
    percentage_difference = (width2 - width1) / width2
    template_bgr = cv2.resize(
        template_bgr,
        (
            int(width2 - (width2 * percentage_difference)),
            int(height2 - (height2 * percentage_difference)),
        ),
    )

    template_hsv = cv2.cvtColor(template_bgr, cv2.COLOR_BGR2HSV)
    src_hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
    upper = np.array([32, 255, 255])
    lower = np.array([8, 1, 85])
    mask = cv2.inRange(src_hsv, lower, upper)
    template_mask = cv2.inRange(template_hsv, lower, upper)

    kernel = np.ones((6, 6), np.uint8)
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    template_opening = cv2.morphologyEx(template_mask, cv2.MORPH_OPEN, kernel)
    template_closing = cv2.morphologyEx(template_opening, cv2.MORPH_CLOSE, kernel)
    base_screen_dil = cv2.dilate(closing, kernel, iterations=1)
    template_dil = cv2.dilate(template_closing, kernel, iterations=1)

    res = cv2.matchTemplate(base_screen_dil, template_dil, cv2.TM_CCOEFF_NORMED)

    _, max_val, _, max_loc = cv2.minMaxLoc(res)

    return max_val
    # loc = np.where(res >= 0.95)
    # for pt in zip(*loc[::-1]):
    #     cv2.rectangle(src, pt,(pt[0] + w, pt[1] + h),(0,255,255), 2)
