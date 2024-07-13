import qrcode
import sys
import requests
from PIL import Image
from io import BytesIO



MODES = [1, 2]
HELP_MODES = {'help', 'Help', 'HELP', 'h', 'H'}
URL_MODES = {'U', 'u', 'url', 'Url', 'URL'}
DIR_MODES = {'D', 'd', 'dir', 'Dir', 'DIR'}
DEFAULT_IMAGE_URL = 'https://svgtopng.com/files/6lldgu0p4szac8y5/o_1er05v6kt1ksorj9mhu1vfpe51b/thumb.png'

def display_help_message():
    return (
        'Usage: python qrmaker.py <MODE> <FILENAME> <"QR DATA"> <"IMAGE URL/DIR" (Mode 2 only!)> <URL/DIR (Mode 2 only!)>\n'
        'Modes:\n'
        '[1] Text2QR\n'
        '[2] Text2QR with an image in the center'
    )

def main():
    mode = parse_mode()
    
    if mode in HELP_MODES:
        print(display_help_message())
        sys.exit()

    filename = parse_filename()
    text = parse_text()

    if mode == 1:
        generate_qr_code(text, filename)
    elif mode == 2:
        image_location, url_or_dir = parse_image_info()
        generate_qr_code_with_image(text, filename, image_location, url_or_dir)
    else:
        print('Unknown mode!')

def parse_mode():
    try:
        return int(sys.argv[1])
    except (IndexError, ValueError):
        print('Invalid or missing mode, defaulting to mode 1.')
        return 1

def parse_filename():
    try:
        return f'{sys.argv[2]}.png'
    except IndexError:
        print('Filename not specified, defaulting to "MyQR.png".')
        return 'MyQR.png'

def parse_text():
    try:
        return sys.argv[3]
    except IndexError:
        print('Text not specified, defaulting to "Hello World!".')
        return 'Hello World!'

def parse_image_info():
    try:
        image_location = sys.argv[4]
    except IndexError:
        print('Image URL/DIR not provided, using default image.')
        image_location = DEFAULT_IMAGE_URL

    try:
        url_or_dir = sys.argv[5]
    except IndexError:
        print('URL/Dir mode not specified, defaulting to URL.')
        url_or_dir = 'url'

    return image_location, url_or_dir

def generate_qr_code(text, filename):
    img = qrcode.make(text)
    img.save(filename)
    print(f'QR code saved as {filename}')

def generate_qr_code_with_image(text, filename, image_location, url_or_dir):
    image_data = fetch_image(image_location, url_or_dir)
    if not image_data:
        print(f'Failed to retrieve image from {image_location}.')
        sys.exit()

    img = qrcode.make(text)
    logo = Image.open(image_data)
    logo.thumbnail((60, 60))

    logo_pos = ((img.size[0] - logo.size[0]) // 2, (img.size[1] - logo.size[1]) // 2)
    img.paste(logo, logo_pos, mask=logo if logo.mode == 'RGBA' else None)

    img.save(filename)
    print(f'QR code with image saved as {filename}')

def fetch_image(image_location, url_or_dir):
    if url_or_dir in URL_MODES:
        try:
            response = requests.get(image_location)
            response.raise_for_status()
            return BytesIO(response.content)
        except requests.RequestException as e:
            print(f'Error fetching image from URL: {e}')
            return None
    elif url_or_dir in DIR_MODES:
        return image_location
    else:
        print(f'Invalid option for URL/Dir: {url_or_dir}')
        return None

if __name__ == '__main__':
    main()