import cv2 as cv
import json
import numpy as np
import time
from urllib.request import urlopen


def get_item_icon(url):
    try:
        resp = urlopen(url)
        item_raw = np.asarray(bytearray(resp.read()), dtype="uint8")
        return cv.imdecode(item_raw, 1)
    except Exception:
        return None


def get_prices_store(path):
    with open(path) as json_file:
        return json.load(json_file)


def is_near(first, second, thresh=10):
    return (first[0] + thresh > second[0] and first[0] - thresh < second[0]) and (first[1] + thresh > second[1] and first[1] - thresh < second[1])


def filter_neighbors(points, thresh=10):
    result = []

    for point in points:

        is_near_point = False
        for pres in result:
            if is_near(pres, point):
                is_near_point = True
                break

        if not is_near_point:
            result.append(point)

    return result


def parse_screenshot(screenshot_path, store_path):
    screenshot_rgb = cv.imread(screenshot_path)

    store_file = get_prices_store(store_path)

    for i, item in enumerate(store_file):
        item_icon = get_item_icon(item["wikiIcon"])
        if item_icon is None:
            continue

        coords = search_for_item(screenshot_rgb, item_icon)
        icon_h, icon_w, _ = item_icon.shape
        found = len(coords)

        if found > 0:
            for pt in coords:
                cv.rectangle(screenshot_rgb, pt,
                             (pt[0] + icon_w, pt[1] + icon_h), (0, 0, 255), 2)

    cv.imwrite('result.png', screenshot_rgb)


def search_for_item(screen_rgb, item_icon, threshold=0.75):
    res = cv.matchTemplate(
        screen_rgb, item_icon, cv.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)

    return filter_neighbors(list(zip(*loc[::-1])))


print(f"started at {time.strftime('%X')}")
parse_screenshot("./img.png", "./data.json")
print(f"finished at {time.strftime('%X')}")
