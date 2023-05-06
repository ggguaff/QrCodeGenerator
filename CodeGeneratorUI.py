import tkinter

import customtkinter as c_tkinter
from customtkinter import filedialog

from tkinter.colorchooser import askcolor

from CodeGenerator import QrCodeGenerator


global mode_var
global qr_code
filename = None
qr_code_color = None


# Function for opening the
# file explorer window
def ask_color():
    colors = askcolor(title="Pick a color")  # open the color picker
    color = colors[1]  # get the color string
    global qr_code_color
    qr_code_color = color


def browse_files():
    # open file-explorer
    global filename
    filename = filedialog.askopenfilename(initialdir="/Users/*/Images",
                                          title="Select a File",
                                          filetypes=(("Image Files", "*.png*"), ("all files", "*.*")))


def create_qr_code():
    # display image
    img_width = 200
    img_height = 200

    global qr_code
    global qr_code_color
    global filename

    if url_entry.get() != '':
        code_generator = QrCodeGenerator(url=url_entry.get(),
                                         image_path=filename if filename is not None else None,
                                         qr_color=qr_code_color if qr_code_color is not None else None)

        qr_code = code_generator.generate_code()

        img = c_tkinter.CTkImage(light_image=qr_code,
                                 size=(img_width, img_height))

        c_tkinter.CTkButton(master=frame,
                            text="Download Image",
                            image=img,
                            compound="top",
                            command=download_image
                            ).pack(pady=20, padx=60)
    else:
        url_warning = c_tkinter.CTkEntry(master=frame,
                                         placeholder_text="Enter URL for QR-Code",
                                         placeholder_text_color="red",
                                         state=tkinter.NORMAL)
        url_warning.pack(pady=20, padx=60)


def download_image():
    route = filedialog.asksaveasfilename(initialdir="/Users/*/Images",
                                         defaultextension=".png",
                                         filetypes=(("Image File", ".png", ".jpg"), ("all files", ".")))
    qr_code.save(route)


c_tkinter.set_appearance_mode("System")
c_tkinter.set_default_color_theme("dark-blue")

root = c_tkinter.CTk()
root.geometry("1024x720")
root.title("QR-Code Generator")

frame = c_tkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = c_tkinter.CTkLabel(master=frame, text="QR-Code Generator",
                           font=("Roboto", 24))
label.pack(pady=12, padx=10)

url_entry = c_tkinter.CTkEntry(master=frame, placeholder_text="Enter URL for QR-Code")
url_entry.pack(pady=12, padx=10)

button = c_tkinter.CTkButton(master=frame, text="Select Image..", command=browse_files)
button.pack(pady=12, padx=10)

color_select = c_tkinter.CTkButton(master=frame, text="Choose Color for QR-Code", command=ask_color)
color_select.pack(pady=12, padx=10)

create_button = c_tkinter.CTkButton(master=frame, text="Create QR-Code", command=create_qr_code)
create_button.pack(pady=12, padx=10)

root.mainloop()
