import tkinter
from tkinter.colorchooser import askcolor
import customtkinter as c_tkinter
from customtkinter import filedialog
from code_generator import QrCodeGenerator

"""
setting global varibles for the QR-code Generator GUI
"""
global mode_var
global qr_code
global close_button
global download_button  
filename = None
qr_code_color = None
qr_frame = None  
close_button = None  
download_button = None  
party_frame = None  
party_colors = ['#000000', '#FF0000',
                '#FFFFFF', '#FF7F00',
                '#000000', '#FFFF00',
                '#FFFFFF', '#00FF00', 
                '#000000', '#0000FF',
                '#FFFFFF', '#4B0082', 
                '#000000', '#9400D3']
current_color_index = 0
party_mode_duration = 3000  

def ask_color():
    """
    Opens a color picker dialog for the user to select a color. 
    Sets the global `qr_code_color` variable to the selected color.
    """
    colors = askcolor(title="Pick a color")
    color = colors[1]
    global qr_code_color
    if not color.startswith('#'):
        color = '#' + color
    qr_code_color = color

def browse_files():
    """
    Opens a file dialog for the user to select an image file. 
    Sets the global `filename` variable to the selected file's path.
    """
    global filename
    filename = filedialog.askopenfilename(initialdir=".",
                                          title="Select a File",
                                          filetypes=(("Image Files", "*.png*"), ("all files", "*.*")))

def create_qr_code():
    """
    Generates a QR code based on the input URL, selected image, and color.
    Displays the QR code along with the URL in the application window.
    """
    img_width = 200
    img_height = 200

    global qr_code
    global qr_code_color
    global filename
    global qr_frame
    global close_button
    global download_button

    if url_entry.get() != '':
        if qr_frame:
            qr_frame.destroy()  

        code_generator = QrCodeGenerator(url=url_entry.get(),
                                         image_path=filename or None,
                                         qr_color=qr_code_color if qr_code_color is not None else "#000000")

        qr_code = code_generator.generate_code()

        img = c_tkinter.CTkImage(light_image=qr_code,
                                 size=(img_width, img_height))

        qr_frame = c_tkinter.CTkFrame(master=qr_code_frame)
        qr_frame.grid(row=1, column=0, columnspan=10, rowspan=20)

        url_label = c_tkinter.CTkLabel(master=qr_frame, text=url_entry.get())
        url_label.grid(row=0, column=0)

        label_img = c_tkinter.CTkLabel(master=qr_frame, image=img)
        label_img.grid(row=1, column=0)

        
        if close_button is None:
            close_button = c_tkinter.CTkButton(master=frame,
                                               text="Delete",
                                               command=close_qr_code,
                                               fg_color="red", hover_color="darkred", text_color="black")
            close_button.grid(row=5, column=0, columnspan=2, sticky="ew")
        else:
            close_button.grid(row=5, column=0, columnspan=2, sticky="ew")

        
        if download_button is None:
            download_button = c_tkinter.CTkButton(master=frame,
                                                  text="Download",
                                                  command=lambda: download_image(qr_code),
                                                  fg_color="green", hover_color="darkgreen", text_color="black")
            download_button.grid(row=6, column=0, columnspan=2, sticky="ew")
        else:
            download_button.grid(row=6, column=0, columnspan=2, sticky="ew")

def close_qr_code():
    """
    Closes and removes the displayed QR code and its associated buttons from the application window.
    """
    global qr_frame
    global close_button
    global download_button
    if qr_frame:
        qr_frame.destroy()
    if close_button:
        close_button.grid_forget()
    if download_button:
        download_button.grid_forget()

def download_image(qr_code):
    """
    Opens a file dialog for the user to save the generated QR code as an image file.
    """
    route = filedialog.asksaveasfilename(initialdir=".",
                                         defaultextension=".png",
                                         filetypes=(("Image Files", "*.png"), ("all files", "*.*")))
    qr_code.save(route)


def party_mode():
    """
    Activates party mode by creating a frame that cycles through different background colors.
    The mode runs for a duration specified by `party_mode_duration`.
    """
    global party_frame
    global current_color_index

    if party_frame:
        party_frame.destroy()

    party_frame = c_tkinter.CTkFrame(master=root, width=420, height=240)
    party_frame.place(x=0, y=0)
    current_color_index = 0
    change_color()
    root.after(party_mode_duration, end_party_mode)

def change_color():
    """
    Changes the color of the `party_frame` to create a party effect.
    This function is called repeatedly to cycle through colors.
    """
    global current_color_index

    if party_frame is not None:
        party_frame.configure(fg_color=party_colors[current_color_index])
        current_color_index = (current_color_index + 1) % len(party_colors)
        root.after(100, change_color)
def end_party_mode():
    """
    Ends party mode by destroying the `party_frame`.
    """
    global party_frame
    if party_frame:
        party_frame.destroy()
        party_frame = None

if __name__ == '__main__':
    c_tkinter.set_appearance_mode("System")

    root = c_tkinter.CTk()
    root.geometry("420x240")  
    root.title("QR-Code Generator -> momosversion")


    
    frame = c_tkinter.CTkFrame(master=root)
    frame.pack(side="left", fill="y", expand=False)

    
    qr_code_frame = c_tkinter.CTkFrame(master=root)
    qr_code_frame.pack(side="left", fill="both", expand=True)

    label = c_tkinter.CTkLabel(master=frame, text="QR-Code Generator",
                               font=("Calibri", 24), text_color="lightgray")
    label.grid(row=0, column=0, columnspan=2, sticky="ew")

    url_entry = c_tkinter.CTkEntry(master=frame, placeholder_text="Enter URL for QR-Code", )
    url_entry.grid(row=1, column=0, columnspan=2, sticky="ew")

    button = c_tkinter.CTkButton(master=frame, text="Select Image", command=browse_files,
                                 fg_color="green", hover_color="darkgreen", text_color="black")
    button.grid(row=2, column=0, columnspan=2, sticky="ew")

    color_select = c_tkinter.CTkButton(master=frame, text="Select Color", command=ask_color, 
                                       fg_color="green", hover_color="darkgreen", text_color="black")
    color_select.grid(row=3, column=0, columnspan=2, sticky="ew")

    create_button = c_tkinter.CTkButton(master=frame, text="Create QR-Code", command=create_qr_code,
                                        fg_color="green", hover_color="darkgreen", text_color="black")
    create_button.grid(row=4, column=0, columnspan=2, sticky="ew")

    party_button = c_tkinter.CTkButton(master=frame, text="Party Mode!", command=party_mode,
                                       fg_color="green", hover_color="darkgreen", text_color="black")
    party_button.grid(row=5, column=0, columnspan=2, sticky="ew")

    root.mainloop()
