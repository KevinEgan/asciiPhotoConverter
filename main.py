from PIL import Image
from colorama import Fore, init

#initialise colorama
init(convert=True)

# resize image to a size of 800 x 175, a size which best suits windows cmd & my laptop screen
original_image = Image.open('ascii-pineapple.jpg')
resized_image = original_image.resize((800, 175))
resized_image.save('resized2.jpg')

# print(resized_image.format, resized_image.size, resized_image.mode)  // prints qualities of image

# gets the rgb of each pixel and returns a matrix containing rgb values
def get_pixel_rgb_values(user_image):
    pixel_matrix = []
    length, height = user_image.size
    # create 2d array containg each pixel's rbg values
    pixel_class = user_image.load()
    for pixel_y_axis in range(height):
        temp_matrix = []
        for pixel_x_axis in range(length):
            temp_matrix.append(pixel_class[pixel_x_axis, pixel_y_axis])
        pixel_matrix.append(temp_matrix)
    return pixel_matrix

# converts rgb to brightness. Also takes user input to decide on which brightness calculation to carry out, and whether
# to invert brightness or not
def convert_rgb_to_brightness(pixel_matrix, user_input, inverted):
    avg_matrix = []
    for line in pixel_matrix:
        temp_matrix = []
        for rgb_tuple in line:
            num1, num2, num3 = rgb_tuple
            if user_input == 1:
                avg_tuple = (num1 + num2 + num3) / 3
            elif user_input == 2:
                # lightness - average of the min & max RGB values
                avg_tuple = (max(num1, num2, num3) + min(num1, num2, num3)) / 2
            else:
                # weighted average of RBG which accounts for human perception
                avg_tuple = (0.21 * num1) + (0.72 * num2) + (0.07 * num3)
            if inverted:
                avg_tuple = (avg_tuple - 255) * -1
            temp_matrix.append(round(avg_tuple))
        avg_matrix.append(temp_matrix)
    return avg_matrix


# converts brightness value to corresponding ascii character
def convert_brightness_to_ascii(avg_matrix):
    # ASCII string from most bright to least bright
    ascii_str = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
    ascii_len = len(ascii_str)
    ascii_matrix = []
    for line in avg_matrix:
        temp_matrix = []
        for value in line:
            brightness_factor = (value / 255)
            ascii_num = round(brightness_factor * ascii_len)
            if ascii_num > 64:
                ascii_num = 64
            ascii_char = ascii_str[ascii_num]
            temp_matrix.append([ascii_char])
        ascii_matrix.append(temp_matrix)
    return ascii_matrix


# prints obtained ascii characters
def print_ascii(ascii_matrix, matrix_mode):
    for i in ascii_matrix:
        ascii_line = ""
        for j in i:
            ascii_line += j[0]
        if matrix_mode:
            print(Fore.GREEN + ascii_line)
        else:
            print(ascii_line)


user_input = -1
while not user_input >= 1 and user_input <= 3:
    print("select an option")
    print("Average: 1")
    print("Brightness: 2")
    print("Luminosity: 3")
    user_input = int(input("Input 1, 2, or 3:"))
    user_matrix_mode = input("Activate The Matrix's green mode? (y/n) ")
    user_inverted = input("Would you like to invert the brightness of the image? (y/n): ")

    pixel_matrix = get_pixel_rgb_values(resized_image)
    avg_matrix = convert_rgb_to_brightness(pixel_matrix, user_input, user_inverted == "y")
    ascii_matrix = convert_brightness_to_ascii(avg_matrix)
    print_ascii(ascii_matrix, user_matrix_mode == "y")

    user_input = -1

