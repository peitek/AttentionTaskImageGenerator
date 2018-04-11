from PIL import Image, ImageDraw, ImageFont

import os
from os.path import join

from config import OUTPUT_DIRECTORY, FONT_COLOR_TASK

FONT_SIZE = 18


def generate_calibration_image():
    print("draw eye-tracking calibration image")
    image = draw_calibration_image()
    write_image_to_file("calibration", image)


def generate_rest_condition_image(i):
    print("draw rest condition calibration image", i)
    image = draw_rest_condition_image()
    write_image_to_file("rest_" + str(i), image)


def generate_decision_time_image(i):
    print("draw decision time calibration image", i)
    image = draw_decision_time_image()
    write_image_to_file("dec_time_" + str(i), image)


def draw_calibration_image():
    # TODO this has a hard-coded image size. change to a more dynamic approach, possibly including more options than just 9-dot calibration?
    print("-> drawing new calibration image")
    (fullSizeX, fullSizeY) = (1920, 1080)
    image = Image.new('RGBA', (fullSizeX, fullSizeY), (0, 0, 0))
    draw = ImageDraw.Draw(image)

    if False:
        array_coords = [(512, 384), (512, 65), (512, 702), (61, 384), (962, 384), (61, 65), (962, 65), (61, 702), (962, 702)]

        for point in array_coords:
            draw.ellipse((point[0] - 10, point[1] - 10, point[0] + 10, point[1] + 10), fill='white', outline='white')
    else:
        print("" + str(1 / 4 * fullSizeX) + ", " + str(1 / 4 * fullSizeY))
        draw.ellipse(((1 / 4 * fullSizeX) - 10, (1 / 4 * fullSizeY) - 10, (1 / 4 * fullSizeX) + 10, (1 / 4 * fullSizeY) + 10), fill='white', outline='white')
        print("" + str(2 / 4 * fullSizeX) + ", " + str(1 / 4 * fullSizeY))
        draw.ellipse(((2 / 4 * fullSizeX) - 10, (1 / 4 * fullSizeY) - 10, (2 / 4 * fullSizeX) + 10, (1 / 4 * fullSizeY) + 10), fill='white', outline='white')
        print("" + str(3 / 4 * fullSizeX) + ", " + str(1 / 4 * fullSizeY))
        draw.ellipse(((3 / 4 * fullSizeX) - 10, (1 / 4 * fullSizeY) - 10, (3 / 4 * fullSizeX) + 10, (1 / 4 * fullSizeY) + 10), fill='white', outline='white')

        print("" + str(1 / 4 * fullSizeX) + ", " + str(2 / 4 * fullSizeY))
        draw.ellipse(((1 / 4 * fullSizeX) - 10, (2 / 4 * fullSizeY) - 10, (1 / 4 * fullSizeX) + 10, (2 / 4 * fullSizeY) + 10), fill='white', outline='white')
        print("" + str(2 / 4 * fullSizeX) + ", " + str(2 / 4 * fullSizeY))
        draw.ellipse(((2 / 4 * fullSizeX) - 10, (2 / 4 * fullSizeY) - 10, (2 / 4 * fullSizeX) + 10, (2 / 4 * fullSizeY) + 10), fill='white', outline='white')
        print("" + str(3 / 4 * fullSizeX) + ", " + str(2 / 4 * fullSizeY))
        draw.ellipse(((3 / 4 * fullSizeX) - 10, (2 / 4 * fullSizeY) - 10, (3 / 4 * fullSizeX) + 10, (2 / 4 * fullSizeY) + 10), fill='white', outline='white')

        print("" + str(1 / 4 * fullSizeX) + ", " + str(3 / 4 * fullSizeY))
        draw.ellipse(((1 / 4 * fullSizeX) - 10, (3 / 4 * fullSizeY) - 10, (1 / 4 * fullSizeX) + 10, (3 / 4 * fullSizeY) + 10), fill='white', outline='white')
        print("" + str(2 / 4 * fullSizeX) + ", " + str(3 / 4 * fullSizeY))
        draw.ellipse(((2 / 4 * fullSizeX) - 10, (3 / 4 * fullSizeY) - 10, (2 / 4 * fullSizeX) + 10, (3 / 4 * fullSizeY) + 10), fill='white', outline='white')
        print("" + str(3 / 4 * fullSizeX) + ", " + str(3 / 4 * fullSizeY))
        draw.ellipse(((3 / 4 * fullSizeX) - 10, (3 / 4 * fullSizeY) - 10, (3 / 4 * fullSizeX) + 10, (3 / 4 * fullSizeY) + 10), fill='white', outline='white')

    return image


def draw_rest_condition_image():
    print("-> drawing rest condition image")
    (fullSizeX, fullSizeY) = (1280, 1024)
    image = Image.new("RGBA", (fullSizeX, fullSizeY), (0, 0, 0))
    draw = ImageDraw.Draw(image)

    inconsolata = ImageFont.truetype('font/Inconsolata-Regular.ttf', FONT_SIZE)

    (letter_width, letter_height) = ImageDraw.ImageDraw(image).textsize(text='+', font=inconsolata)
    draw.text((fullSizeX/2 - letter_width/2, fullSizeY/2 - letter_height/2), '+', FONT_COLOR_TASK, font=inconsolata)

    return image


def draw_decision_time_image():
    print("-> drawing decision time image")
    (fullSizeX, fullSizeY) = (1280, 1024)
    image = Image.new('RGBA', (fullSizeX, fullSizeY), (0, 0, 0))
    draw = ImageDraw.Draw(image)

    inconsolata = ImageFont.truetype('font/Inconsolata-Regular.ttf', FONT_SIZE)

    (letter_width, letter_height) = ImageDraw.ImageDraw(image).textsize(text="Falls noch nicht geschehen: letzte Chance zum Klicken...", font=inconsolata)
    draw.text((fullSizeX / 2 - letter_width / 2, fullSizeY / 2 - letter_height / 2), "Falls noch nicht geschehen: letzte Chance zum Klicken...", FONT_COLOR_TASK, font=inconsolata)

    return image


def write_image_to_file(file_name, image):
    print("-> saving new image to disk")

    if not os.path.isdir(OUTPUT_DIRECTORY):
        try:
            os.mkdir(OUTPUT_DIRECTORY)
        except Exception:
            print("Error creating the output repository")

    image.save(join(OUTPUT_DIRECTORY, file_name + '.png'), 'PNG')
    print("-> saved image: ", file_name)
