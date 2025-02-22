from math import ceil
import os

from PIL import (
    Image,
    ImageFont,
    ImageDraw,
)


PIL_GRAYSCALE = 'L'
PIL_WIDTH_INDEX = 0
PIL_HEIGHT_INDEX = 1
COMMON_MONO_FONT_FILENAMES = [
    'DejaVuSansMono.ttf',  # Linux
    'Consolas Mono.ttf',   # MacOS, I think
    'Consolas.ttf',         # Windows, I think
]

image_width = 1000

# import image from file
image_name = "img.png"
img = Image.open(image_name)

def ascii_image(image):
    width, height = image.size
    aspect_ratio = height/width
    new_width = image_width
    new_height = aspect_ratio * new_width * 0.55
    #convert float to int
    new_height = int(new_height)
    #resize image
    img = image.resize((new_width, new_height))

    img = img.convert('L')
    pixels = img.getdata()

    # replace each pixel with a chartacter from array
    chars = ['@', '#', '$', '%', '^', '&', '*', ':', ';', '.', ',']
    new_pixels = [chars[pixel//25] for pixel in pixels]
    new_pixels = ''.join(new_pixels)

    #split string of chars into multiple strings of length=new_width and create a list
    new_pixels_count = len(new_pixels)
    ascii_image = [new_pixels[index:index+new_width] for index in range(0, new_pixels_count, new_width)]
    ascii_image = '\n'.join(ascii_image)

    # save ascii image to a file
    file = "ascii_image.txt"
    with open(file, 'w') as f:
        f.write(ascii_image)
        print("saved image to {}".format(file))


def textfile_to_image(textfile_path):
    """Convert text file to a grayscale image.

    arguments:
    textfile_path - the content of this file will be converted to an image
    font_path - path to a font file (for example impact.ttf)
    """
    # parse the file into lines stripped of whitespace on the right side
    with open(textfile_path) as f:
        lines = tuple(line.rstrip() for line in f.readlines())

    # choose a font (you can see more detail in the linked library on github)
    font = None
    large_font = 20  # get better resolution with larger size
    for font_filename in COMMON_MONO_FONT_FILENAMES:
        try:
            font = ImageFont.truetype(font_filename, size=large_font)
            print(f'Using font "{font_filename}".')
            break
        except IOError:
            print(f'Could not load font "{font_filename}".')
    if font is None:
        font = ImageFont.load_default()
        print('Using default font.')

    # make a sufficiently sized background image based on the combination of font and lines
    font_points_to_pixels = lambda pt: round(pt * 96.0 / 72)
    margin_pixels = 20

    # height of the background image
    tallest_line = max(lines, key=lambda line: font.getsize(line)[PIL_HEIGHT_INDEX])
    max_line_height = font_points_to_pixels(font.getsize(tallest_line)[PIL_HEIGHT_INDEX])
    realistic_line_height = max_line_height * 0.8  # apparently it measures a lot of space above visible content
    image_height = int(ceil(realistic_line_height * len(lines) + 2 * margin_pixels))

    # width of the background image
    widest_line = max(lines, key=lambda s: font.getsize(s)[PIL_WIDTH_INDEX])
    max_line_width = font_points_to_pixels(font.getsize(widest_line)[PIL_WIDTH_INDEX])
    image_width = int(ceil(max_line_width + (2 * margin_pixels)))

    # draw the background
    background_color = 255  # white
    image = Image.new(PIL_GRAYSCALE, (image_width, image_height), color=background_color)
    draw = ImageDraw.Draw(image)

    # draw each line of text
    font_color = 0  # black
    horizontal_position = margin_pixels
    for i, line in enumerate(lines):
        vertical_position = int(round(margin_pixels + (i * realistic_line_height)))
        draw.text((horizontal_position, vertical_position), line, fill=font_color, font=font)
    
    os.remove(textfile_path)

    return image



ascii_image(img)
output = textfile_to_image('ascii_image.txt')

# save the image to a file
filename = 'out ' + image_name
output.save(filename)
print('saved image to {}'.format('out ' + image_name))