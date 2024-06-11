import tkinter
from tkinter.colorchooser import askcolor
import customtkinter as c_tkinter
from customtkinter import filedialog
from code_generator import QrCodeGenerator
import threading
import time

# Global variables
filename = None
qr_code_color = None
qr_frame = None  
close_button = None  
download_button = None
cancel_button = None
party_frame = None  
party_colors = ['#000000', '#FF0000', '#FFFFFF', '#FF7F00',
                '#000000', '#FFFF00', '#FFFFFF', '#00FF00', 
                '#000000', '#0000FF', '#FFFFFF', '#4B0082', 
                '#000000', '#9400D3']
current_color_index = 0
party_mode_duration = 2000  

loading_label = None
generation_thread = None
stop_event = threading.Event()

def ask_color():
    colors = askcolor(title="Pick a color")
    color = colors[1]
    global qr_code_color
    if not color.startswith('#'):
        color = '#' + color
    qr_code_color = color

def browse_files():
    global filename
    filename = filedialog.askopenfilename(initialdir=".", title="Select a File",
                                          filetypes=(("Image Files", "*.png*"), ("all files", "*.*")))

def create_qr_code_thread():
    global qr_code, qr_code_color, filename, qr_frame, close_button, download_button, loading_label
    try:
        stop_event.clear()
        img_width = 200
        img_height = 200

        if url_entry.get() != '':
            for _ in range(3):
                if stop_event.is_set():
                    return
                time.sleep(1)

            if stop_event.is_set():
                return

            code_generator = QrCodeGenerator(url=url_entry.get(),
                                             image_path=filename or None,
                                             qr_color=qr_code_color if qr_code_color is not None else "#000000")

            qr_code = code_generator.generate_code()

            if stop_event.is_set():
                return

            img = c_tkinter.CTkImage(light_image=qr_code, size=(img_width, img_height))

            root.after(0, lambda: display_qr_code(img, url_entry.get()))
    finally:
        root.after(0, cleanup_after_generation)

def display_qr_code(img, url):
    global qr_frame, close_button, download_button
    if qr_frame:
        qr_frame.destroy()

    qr_frame = c_tkinter.CTkFrame(master=qr_code_frame)
    qr_frame.grid(row=1, column=0, columnspan=10, rowspan=20)

    url_label = c_tkinter.CTkLabel(master=qr_frame, text=url)
    url_label.grid(row=0, column=0)

    label_img = c_tkinter.CTkLabel(master=qr_frame, image=img)
    label_img.grid(row=1, column=0)

    if close_button is None:
        close_button = c_tkinter.CTkButton(master=frame, text="Delete", command=close_qr_code,
                                           fg_color="red", hover_color="darkred", text_color="black")
        close_button.grid(row=5, column=0, columnspan=2, sticky="ew")
    else:
        close_button.grid(row=5, column=0, columnspan=2, sticky="ew")

    if download_button is None:
        download_button = c_tkinter.CTkButton(master=frame, text="Download",
                                              command=lambda: download_image(qr_code),
                                              fg_color="green", hover_color="darkgreen", text_color="black")
        download_button.grid(row=6, column=0, columnspan=2, sticky="ew")
    else:
        download_button.grid(row=6, column=0, columnspan=2, sticky="ew")

def start_qr_code_generation():
    global generation_thread, loading_label, cancel_button
    if loading_label:
        loading_label.destroy()
    
    loading_label = c_tkinter.CTkLabel(master=frame, text="Generating, please wait...")
    loading_label.grid(row=7, column=0, columnspan=2, sticky="ew")

    if cancel_button is None:
        cancel_button = c_tkinter.CTkButton(master=frame, text="Cancel", command=cancel_qr_code_generation,
                                            fg_color="red", hover_color="darkred", text_color="black")
        cancel_button.grid(row=8, column=0, columnspan=2, sticky="ew")
    else:
        cancel_button.grid(row=8, column=0, columnspan=2, sticky="ew")

    generation_thread = threading.Thread(target=create_qr_code_thread)
    generation_thread.start()

def cancel_qr_code_generation():
    global generation_thread, stop_event, loading_label, cancel_button
    stop_event.set()
    if generation_thread and generation_thread.is_alive():
        generation_thread.join(1)  # join with a timeout to avoid blocking the main thread
    cleanup_after_generation()

def cleanup_after_generation():
    global loading_label, cancel_button
    if loading_label:
        loading_label.destroy()
    if cancel_button:
        cancel_button.grid_forget()

def close_qr_code():
    global qr_frame, close_button, download_button
    if qr_frame:
        qr_frame.destroy()
    if close_button:
        close_button.grid_forget()
    if download_button:
        download_button.grid_forget()

def download_image(qr_code):
    route = filedialog.asksaveasfilename(initialdir=".", defaultextension=".png",
                                         filetypes=(("Image Files", "*.png"), ("all files", "*.*")))
    qr_code.save(route)

def party_mode():
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
    global current_color_index

    if party_frame is not None:
        party_frame.configure(fg_color=party_colors[current_color_index])
        current_color_index = (current_color_index + 1) % len(party_colors)
        root.after(88, change_color)

def end_party_mode():
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

    label = c_tkinter.CTkLabel(master=frame, text="QR-Code Generator", font=("Calibri", 24), text_color="lightgray")
    label.grid(row=0, column=0, columnspan=2, sticky="ew")

    url_entry = c_tkinter.CTkEntry(master=frame, placeholder_text="Enter URL for QR-Code")
    url_entry.grid(row=1, column=0, columnspan=2, sticky="ew")

    button = c_tkinter.CTkButton(master=frame, text="Select Image", command=browse_files,
                                 fg_color="green", hover_color="darkgreen", text_color="black")
    button.grid(row=2, column=0, columnspan=2, sticky="ew")

    color_select = c_tkinter.CTkButton(master=frame, text="Select Color", command=ask_color,
                                       fg_color="green", hover_color="darkgreen", text_color="black")
    color_select.grid(row=3, column=0, columnspan=2, sticky="ew")

    create_button = c_tkinter.CTkButton(master=frame, text="Create QR-Code", command=start_qr_code_generation,
                                        fg_color="green", hover_color="darkgreen", text_color="black")
    create_button.grid(row=4, column=0, columnspan=2, sticky="ew")

    party_button = c_tkinter.CTkButton(master=frame, text="Party Mode!", command=party_mode,
                                       fg_color="green", hover_color="darkgreen", text_color="black")
    party_button.grid(row=6, column=0, columnspan=2, sticky="ew")

    root.mainloop()
