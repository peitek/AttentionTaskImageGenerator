from PIL import Image, ImageDraw, ImageFont

import random
import os
from os.path import join

MARK_VERTICAL_PADDING = 25

FONT_COLOR_TASK = (255, 255, 255)
FONT_COLOR_INSTRUCTION = (200, 200, 200)
MARK_WIDTH = 3
INSTRUCTION_TEXT = "Alle d mit genau zwei Strichen auswählen!"


def main():
    for i in range(15):
        generate_attention_task_image(i)


def generate_attention_task_image(i):
    print("generating attention task image ", i)
    lines = generate_text_for_task()
    image = draw_image(lines)
    write_image_to_file("attention_task_" + str(i), image)


def generate_text_for_task():
    full_array = []
    for i in range(4):
        array = []
        for i in range(8):
            marks_above, marks_below = get_random_marks()

            letter = "p" if random.choice([0, 1]) == 0 else 'd'

            array.append({
                "letter": letter,
                "marks_above": marks_above,
                "marks_below": marks_below
            })

        full_array.append(array)

    return full_array


def get_random_marks():
    marks_above = random.choice([0, 1, 2])
    marks_below = random.choice([0, 1, 2])

    if marks_above + marks_below == 0:
        return get_random_marks()
    else:
        return marks_above, marks_below


def draw_image(lines):
    print("-> drawing new attention task image")
    (fullSizeX, fullSizeY) = (1920, 1080)
    image = Image.new("RGBA", (fullSizeX, fullSizeY), (0, 0, 0))
    draw = ImageDraw.Draw(image)

    inconsolata = ImageFont.truetype("resources/Inconsolata-Regular.ttf", 42)

    # draw instructions
    (instruction_width, instruction_height) = ImageDraw.ImageDraw(image).textsize(text=INSTRUCTION_TEXT, font=inconsolata)
    draw.text((fullSizeX/2 - instruction_width/2, (fullSizeY / 20)), INSTRUCTION_TEXT , FONT_COLOR_INSTRUCTION, font=inconsolata)

    x_pos_start = (fullSizeX / 8)
    y_pos = instruction_height

    # draw attention task
    for line in lines:
        xPos = x_pos_start
        y_pos += (fullSizeY / 5)

        for element in line:
            # draw letter
            (letter_width, letter_height) = ImageDraw.ImageDraw(image).textsize(text=element["letter"], font=inconsolata)
            draw.text((xPos, y_pos), element["letter"], FONT_COLOR_TASK, font=inconsolata)

            # draw marks above letter
            if element["marks_above"] == 1:
                draw.line((xPos + (letter_width / 2), y_pos - (letter_height / 2)) + (xPos + (letter_width / 2), y_pos - (letter_height / 2) - MARK_VERTICAL_PADDING), fill=FONT_COLOR_TASK, width=MARK_WIDTH)
            elif element["marks_above"] == 2:
                draw.line((xPos + (1/4 * letter_width), y_pos - (letter_height / 2)) + (xPos + (1/4 * letter_width), y_pos - (letter_height / 2) - MARK_VERTICAL_PADDING), fill=FONT_COLOR_TASK, width=MARK_WIDTH)
                draw.line((xPos + (3/4 * letter_width), y_pos - (letter_height / 2)) + (xPos + (3/4 * letter_width), y_pos - (letter_height / 2) - MARK_VERTICAL_PADDING), fill=FONT_COLOR_TASK, width=MARK_WIDTH)

            # draw marks below letter
            if element["marks_below"] == 1:
                draw.line((xPos + (letter_width / 2), y_pos + (1.5 * letter_height)) + (xPos + (letter_width / 2), y_pos + (1.5 * letter_height) + MARK_VERTICAL_PADDING), fill=FONT_COLOR_TASK, width=MARK_WIDTH)
            elif element["marks_below"] == 2:
                draw.line((xPos + (1/4 * letter_width), y_pos + (1.5 * letter_height)) + (xPos + (1/4 * letter_width), y_pos + (1.5 * letter_height) + MARK_VERTICAL_PADDING), fill=FONT_COLOR_TASK, width=MARK_WIDTH)
                draw.line((xPos + (3/4 * letter_width), y_pos + (1.5 * letter_height)) + (xPos + (3/4 * letter_width), y_pos + (1.5 * letter_height) + MARK_VERTICAL_PADDING), fill=FONT_COLOR_TASK, width=MARK_WIDTH)

            xPos += (fullSizeX / 8)

    return image


def write_image_to_file(file_name, image):
    print("-> saving new attention task image to disk")
    subdirectory = 'output_images'
    try:
        os.mkdir(subdirectory)
    except Exception:
        pass
    image.save(join(subdirectory, file_name + '.png'), "PNG")


main()
