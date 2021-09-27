"""@author: Maxime."""


from PIL import Image  # pip install Pillow
import glob
import os


class ASCII_art:
    """
    ASCII Art class: convert image to ASCII art.

    Inspired from: @RameshAditya: https://github.com/RameshAditya/asciify
    """

    def __init__(self, image, width: int,
                 buckets: int, multiplicator: int = 2) -> None:
        self.ascii_characters = ['.', '*', '#', '@'][::-1]
        self.image = Image.open(image)
        self.size = self.image.size  # Image size.
        self.new_width = width  # New width after resizing.
        self.buckets = buckets  # Details indicator.
        self.multiplator = multiplicator  # width multiplicator.

    def resize(self) -> None:
        """Resize the image while maintaining aspect ratio."""
        old_width, old_height = self.size  # Old dimensions of the image.
        # Create new ratio.
        aspect_ratio = float(old_height) / float(old_width * self.multiplator)
        new_height = int(aspect_ratio * self.new_width)  # Set new height.
        # Apply dimensions to size attribute.
        self.size = self.new_width, new_height
        # Apply new image to image attribute.
        self.image = self.image.resize(self.size)

    def grayscale(self) -> None:
        """Grayscaled the image."""
        self.image = self.image.convert('L')

    def modify(self) -> str:
        """Replace every pixel with a character whose intensity is similar."""
        pixels = list(self.image.getdata())  # Get data of image in a list.
        new_pixels = [self.ascii_characters[pixel // self.buckets]
                      for pixel in pixels]
        return ''.join(new_pixels)

    def construct(self) -> None:
        """Construct the image from the character list."""
        self.resize()
        self.grayscale()
        pixels = self.modify()
        # Create an ASCII art from grayscaled image.
        ascii = [pixels[index:index + self.new_width]
                 for index in range(0, len(pixels), self.new_width)]
        return '\n'.join(ascii)


class Converter:
    """Converter class: Images to ASCII text."""

    def __init__(self, path: str) -> None:
        self.colors = {'T': '♣', 'P': '♠', 'K': '♦', 'C': '♥'}
        self.values = {'14': 'A', '2': '2', '3': '3', '4': '4', '5': '5',
                       '6': '6', '7': '7', '8': '8', '9': '9', '10': '10',
                       '11': 'J', '12': 'Q', '13': 'K'}
        self.path = path

    def image_to_ascii(self) -> None:
        """Convert image to ASCII."""
        for image in glob.glob(f'{self.path}/*'):
            ascii_art = ASCII_art(image, 40, 100)
            self.save_text_file(ascii_art.construct(), image)
            os.remove(image)  # Remove image.

    def save_text_file(self, ascii_text: str, image) -> None:
        """Save text file with card name."""
        image_name = image.split(".")[0].split("\\")[1]
        file_name = self.values[image_name[:-1]] + self.colors[image_name[-1]]

        with open(f'{self.path}/{file_name}.txt', 'w+') as file:
            file.write(ascii_text)
            file.close()


if __name__ == '__main__':

    print('Inspired from: @RameshAditya: '
          'https://github.com/RameshAditya/asciify')
    converter = Converter(input('Images path: '))
    converter.image_to_ascii()
