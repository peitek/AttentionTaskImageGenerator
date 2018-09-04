from PIL import Image, ImageDraw, ImageFont

import random
import os
from os.path import join

from config import OUTPUT_DIRECTORY, INSTRUCTION_TEXT, FONT_COLOR_INSTRUCTION, FONT_COLOR_TASK, FONT_SIZE_TASK, FONT_SIZE_INSTRUCTION, MARK_VERTICAL_PADDING, MARK_WIDTH, IMAGE_SIZE


def generate_attention_task_image(i):
    print("generating attention task image ", i)
    lines = generate_text_for_task()
    image = draw_attention_task_image(lines)
    write_image_to_file("attention_task_" + str(i), image)


def generate_text_for_task():
    full_array = []
    for i in range(3):
        array = []
        for i in range(4):
            marks_above, marks_below = get_random_marks()

            letter = 'd' if random.choice([0, 2]) == 0 else 'p'

            array.append({
                'letter': letter,
                'marks_above': marks_above,
                'marks_below': marks_below
            })

        full_array.append(array)

    return full_array


def get_random_marks():
    marks_above = random.choice([0, 1, 2])
    marks_below = random.choice([0, 1, 2])

    # it's not fully random, we don't want no marks at all
    if marks_above + marks_below == 0:
        return get_random_marks()
    else:
        return marks_above, marks_below


def draw_attention_task_image(lines):
    print("-> drawing new attention task image")
    (fullSizeX, fullSizeY) = IMAGE_SIZE
    image = Image.new("RGBA", (fullSizeX, fullSizeY), (0, 0, 0))
    draw = ImageDraw.Draw(image)

    inconsolata_instruction = ImageFont.truetype('font/Inconsolata-Regular.ttf', FONT_SIZE_INSTRUCTION)
    inconsolata = ImageFont.truetype('font/Inconsolata-Regular.ttf', FONT_SIZE_TASK)

    # draw instructions
    (instruction_width, instruction_height) = ImageDraw.ImageDraw(image).textsize(text=INSTRUCTION_TEXT, font=inconsolata_instruction)
    draw.text((fullSizeX/2 - instruction_width/2, (fullSizeY / 30)), INSTRUCTION_TEXT, FONT_COLOR_INSTRUCTION, font=inconsolata_instruction)

    x_pos_start = (fullSizeX / 12)
    y_pos = instruction_height + (fullSizeY / 6)

    # draw attention task
    for line in lines:
        xPos = x_pos_start

        for element in line:
            print("drawing a {letter} with {marks_above} marks above and {marks_below} marks below".format(**element))

            # draw letter
            (letter_width, letter_height) = ImageDraw.ImageDraw(image).textsize(text=element['letter'], font=inconsolata)
            draw.text((xPos, y_pos), element['letter'], FONT_COLOR_TASK, font=inconsolata)

            # draw marks above letter
            if element['marks_above'] == 1:
                draw.line((xPos + (letter_width / 2), y_pos - (letter_height / 2)) + (xPos + (letter_width / 2), y_pos - (letter_height / 2) - MARK_VERTICAL_PADDING), fill=FONT_COLOR_TASK, width=MARK_WIDTH)
            elif element['marks_above'] == 2:
                draw.line((xPos + (1/4 * letter_width), y_pos - (letter_height / 2)) + (xPos + (1/4 * letter_width), y_pos - (letter_height / 2) - MARK_VERTICAL_PADDING), fill=FONT_COLOR_TASK, width=MARK_WIDTH)
                draw.line((xPos + (3/4 * letter_width), y_pos - (letter_height / 2)) + (xPos + (3/4 * letter_width), y_pos - (letter_height / 2) - MARK_VERTICAL_PADDING), fill=FONT_COLOR_TASK, width=MARK_WIDTH)

            # draw marks below letter
            if element['marks_below'] == 1:
                draw.line((xPos + (letter_width / 2), y_pos + (1.5 * letter_height)) + (xPos + (letter_width / 2), y_pos + (1.5 * letter_height) + MARK_VERTICAL_PADDING), fill=FONT_COLOR_TASK, width=MARK_WIDTH)
            elif element['marks_below'] == 2:
                draw.line((xPos + (1/4 * letter_width), y_pos + (1.5 * letter_height)) + (xPos + (1/4 * letter_width), y_pos + (1.5 * letter_height) + MARK_VERTICAL_PADDING), fill=FONT_COLOR_TASK, width=MARK_WIDTH)
                draw.line((xPos + (3/4 * letter_width), y_pos + (1.5 * letter_height)) + (xPos + (3/4 * letter_width), y_pos + (1.5 * letter_height) + MARK_VERTICAL_PADDING), fill=FONT_COLOR_TASK, width=MARK_WIDTH)

            xPos += 1.05 * (fullSizeX / 4)

        y_pos += 1.1 * (fullSizeY / 4)

    return image


def write_image_to_file(file_name, image):
    print("-> saving new attention task image to disk")
    if not os.path.isdir(OUTPUT_DIRECTORY):
        try:
            os.mkdir(OUTPUT_DIRECTORY)
        except Exception:
            print("Error creating the output repository")

    image.save(join(OUTPUT_DIRECTORY, file_name + '.png'), 'PNG')
    print("-> saved attention task image: ", file_name)