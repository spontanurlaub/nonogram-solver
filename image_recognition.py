# Image recognition to detect the numbers on the sides of the nonogram puzzle

import cv2
import numpy as np
import matplotlib.pyplot as plt

# What number is shown in which picture?
numbers = {
    "zero.png": 0,
    "one.png": 1,
    "one_.png": 1,
    "one__.png": 1,
    "two.png": 2,
    "two_.png": 2,
    "two__.png": 2,
    "three.png": 3,
    "three_.png": 3,
    "four.png": 4,
    "four_.png": 4,
    "five.png": 5,
    "six.png": 6,
    "seven.png": 7,
    "eight.png": 8,
    "nine.png": 9,
    "cross.png": -1
}

number_positions = []

def find_template(image, image_gray, template_path):
    template = cv2.imread(f"img/{template_path}", 0)
    w, h = template.shape[::-1]
    threshold = 0.88
    res = cv2.matchTemplate(image_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(image, pt, (pt[0] + w, pt[1]+h), (0, 0, 255), 2)
        number_positions.append((pt[0], pt[1], numbers[template_path]))

def analyze_number_positions():
    # cleanup
    n = 0
    while n < len(number_positions)-1:
        item = number_positions[n]
        duplicates = filter(lambda x: abs(x[0]-item[0]) < 3 and abs(x[1]-item[1] < 3 and x[2]==item[2]), number_positions[n+1:])
        for d in duplicates:
            number_positions.remove(d)
        n+=1
    
    row_numbers = []
    column_numbers = []
    # get row numbers
    r_numbers = list(filter(lambda x: x[0] < 170, number_positions))
    for n in range(10):
        y_pos = 201 + 88*n
        nums = sorted(filter(lambda x: y_pos < x[1] < y_pos+88, r_numbers), key=lambda x: x[0])
        nums = [x[2] for x in nums]
        if 0 in nums:
            nums = [10]
        row_numbers.append(nums)
    
    # get column numbers
    c_numbers = list(filter(lambda x: x[1] < 195, number_positions))
    for n in range(10):
        x_pos = 175 + 88*n
        nums = sorted(filter(lambda x: x_pos < x[0] < x_pos+88, c_numbers), key=lambda x: x[1])
        nums = [x[2] for x in nums]
        if 0 in nums:
            nums = [10]
        column_numbers.append(nums)
    return row_numbers, column_numbers


def analyze_photo():
    number_positions.clear()
    img = cv2.imread("img/screenshot.png")
    img = img[575:1645, 20:-20]
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    for num in numbers:
        find_template(img, img_gray, num)
    cv2.imwrite("img/output.png", img)
    return analyze_number_positions()
