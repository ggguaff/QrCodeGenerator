import customtkinter as c_tkinter
import qrcode
from PIL import Image, ImageDraw
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import SolidFillColorMask
from qrcode.image.styles.moduledrawers import (
    CircleModuleDrawer, SquareModuleDrawer
)

from colormap import hex2rgb


def create_round_qr(image):

    width, height = image.size
    left = 0
    top = height // 3
    right = width
    bottom = 2 * height // 3

    cropped_section = image.crop((left, top, right, bottom))
    rotated_crop = cropped_section.copy()
    rotated_crop = rotated_crop.rotate(90, expand=True)

    # fill top
    image.paste(cropped_section, (0, -cropped_section.size[1] // 2 + 20))
    # fill bottom
    image.paste(cropped_section, (0, image.size[1] - cropped_section.size[1] // 2 - 20))
    # fill left
    image.paste(rotated_crop, (-rotated_crop.size[0] // 2 + 20, 0))
    # fill right
    image.paste(rotated_crop, (image.size[0] - rotated_crop.size[0] // 2 - 20, 0))

    # draw round border for qr code
    draw = ImageDraw.Draw(image)
    draw.ellipse(
        (30, 30, image.size[1]-30, image.size[1]-30),
        fill=None,
        outline='black'
    )

    # draw outside mask ring
    draw.ellipse(
        (-rotated_crop.size[0],
         -cropped_section.size[1],
         image.size[1] + rotated_crop.size[0],
         image.size[1] + cropped_section.size[1]
         ),
        fill=None,
        outline='white',
        width=340
    )
    return image

def generate_code(logo_link, url, qr_color):
    # open image from path
    logo = Image.open(logo_link)

    # basewidth of the image
    base_width = 300

    # image size
    w_percent = (base_width / float(logo.size[0]))
    hsize = int(float(logo.size[1]) * float(w_percent))
    logo = logo.resize((base_width, hsize), Image.LANCZOS)
    qr_code = qrcode.QRCode(
        version=10,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=18,
        mask_pattern=4
    )

    # adding URL to QR-code
    qr_code.add_data(url)

    # generating the QR code
    qr_code.make()
    # adding color to QR code
    qr_img = qr_code.make_image(
        image_factory=StyledPilImage,
        module_drawer=CircleModuleDrawer(resample_Method=None),
        color_mask=SolidFillColorMask(back_color=hex2rgb("#ffffff"), front_color=hex2rgb(qr_color))
        ).convert('RGBA')

    qr_img_round = create_round_qr(qr_img)

    # set size of QR-Code
    pos = ((qr_img_round.size[0] - logo.size[0]) // 2,
           (qr_img_round.size[1] - logo.size[1]) // 2)
    qr_img_round.alpha_composite(logo.convert('RGBA'), pos)

    return qr_img_round
