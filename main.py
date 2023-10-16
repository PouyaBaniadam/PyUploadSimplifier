import os
import sys
import tkinter
from tkinter import *
from tkinter import messagebox

import pygame
import pyperclip
from PIL import ImageTk, ImageSequence
from PIL.Image import open as pil_open


def main_screen():
    global bg
    global button_start
    global button_paste
    global button_delete
    global titles_entry

    def insert_into_tags(titles_entry):
        if len(titles_entry) != 0:
            entry_list = titles_entry.strip().split('\n')

            titles_tag_index = 0
            titles_tag = ""

            for title_to_be_added in entry_list:
                html_tag = f'<li><a href="#{titles_tag_index + 1}"></a></li>'
                insertion_index = html_tag.index("</a>")
                titles_tag += html_tag[:insertion_index] + title_to_be_added + html_tag[insertion_index:] + "\n"
                titles_tag_index += 1

            titles_tag_result_to_copy = """<div class="catalogbox">
    <strong><span style="color:#2f4f4f;">آنچه در این مقاله می خوانید:</span></strong>
    <ul>
""" + titles_tag + """</ul>
</div>"""

            h2_tag_index = 0
            h2_tag = ""

            for h2_to_be_added in entry_list:
                html_tag = f'<h2 dir="RTL" id="{h2_tag_index + 1}" style="text-align: justify;"><strong></strong></h2><p>&nbsp;</p>'
                insertion_index = html_tag.index("</strong>")
                h2_tag += html_tag[:insertion_index] + h2_to_be_added + html_tag[insertion_index:] + "\n"
                h2_tag_index += 1

            h2_tag_result_to_copy = h2_tag

            delete()

            can_copy_titles = messagebox.askyesno(title="Copy?", message="Can I copy titles part to clipboard?")
            if can_copy_titles:
                pyperclip.copy(titles_tag_result_to_copy)

            can_copy_h2s = messagebox.askyesno(title="Copy?", message="Can I copy H2 part to clipboard?")
            if can_copy_h2s:
                pyperclip.copy(h2_tag_result_to_copy)

        else:
            messagebox.showerror(title="Error", message="Give me some text first!")

    bg = PhotoImage(file=resource_path("media//screen.png"))
    bg_label = Label(image=bg)
    bg_label.pack()

    def on_hover(event, button, x_coordinate, y_coordinate, text):
        bind_button.config(text=text)
        bind_button.place(x=x_coordinate, y=y_coordinate)
        button.config(cursor="hand1")

    def leave_hover(event):
        bind_button.place_forget()

    def paste():
        titles_entry.insert(END, pyperclip.paste())

    def delete():
        titles_entry.delete("1.0", "end")

    bind_button = Label(root, text="", bg="#2e2b32", fg="#2e2b32", font=("B Nazanin", 12))
    bind_button.pack()

    titles_entry = Text(root, border=0, background="#1f1f1f", fg="#ffffff", font=("B Nazanin", 13))
    titles_entry.place(x=60, y=110, width=380, height=220)

    button_paste = PhotoImage(file=resource_path("media//paste.png"))
    button_paste_label = Label(image=button_paste, borderwidth=0)
    button_paste_label.place(x=350, y=345)
    real_button_paste = Button(root, image=button_paste, borderwidth=0, activebackground="#1f1f1f", bg="#1f1f1f",
                               command=paste)
    real_button_paste.place(x=350, y=345)
    real_button_paste.bind("<Enter>",
                           lambda event: on_hover(event, event.widget, 0, 100, text=""))
    real_button_paste.bind("<Leave>", leave_hover)

    button_delete = PhotoImage(file=resource_path("media//delete.png"))
    button_delete_label = Label(image=button_delete, borderwidth=0)
    button_delete_label.place(x=100, y=345)
    real_button_delete = Button(root, image=button_delete, borderwidth=0, activebackground="#1f1f1f", bg="#1f1f1f",
                                command=delete)
    real_button_delete.place(x=100, y=345)
    real_button_delete.bind("<Enter>",
                            lambda event: on_hover(event, event.widget, 0, 100, text=""))
    real_button_delete.bind("<Leave>", leave_hover)

    button_start = PhotoImage(file=resource_path("media//start.png"))
    button_start_label = Label(image=button_start, borderwidth=0)
    button_start_label.place(x=215, y=400)
    real_button_start = Button(root, image=button_start, borderwidth=0, activebackground="#2e2b32", bg="#2e2b32",
                               command=lambda: insert_into_tags(titles_entry=titles_entry.get('1.0', 'end-1c')))
    real_button_start.place(x=215, y=400)
    real_button_start.bind("<Enter>",
                           lambda event: on_hover(event, event.widget, 0, 100, text=""))
    real_button_start.bind("<Leave>", leave_hover)


def resource_path(relative_path):
    global base_path
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath("assets")

    return os.path.join(base_path, relative_path)


def update_frame():
    global frame_index
    frame = frames[frame_index]
    frame_index = (frame_index + 1) % len(frames)

    splash_bg_label.configure(image=frame)
    splash_bg_label.image = frame

    splash_root.after(frame_duration, update_frame)


def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


def main_window():
    global root
    splash_root.destroy()
    root = tkinter.Tk()
    root.title("PyUploadSimplifier")
    root.minsize(width=500, height=500)
    root.maxsize(width=500, height=500)
    root.iconbitmap(resource_path("media//icon.ico"))
    center_window(root)

    main_screen()
    root.mainloop()


def splash_screen():
    global frames
    global frame_index
    global frame_duration
    global splash_bg_label
    global splash_root

    splash_root = tkinter.Tk()
    splash_root.geometry("600x600")
    splash_root.overrideredirect(True)
    splash_root.attributes("-topmost", True)

    gif_path = resource_path("media/Loading.gif")
    splash_bg = pil_open(gif_path)
    frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(splash_bg)]
    frame_index = 0
    splash_bg_label = Label(splash_root, image=frames[0])
    splash_bg_label.pack()
    frame_duration = 17
    update_frame()

    pygame.mixer.init()
    pygame.mixer.music.load(resource_path("media/StartSound.mp3"))
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play()

    splash_root.after(4750, main_window)


if __name__ == "__main__":
    splash_screen()
    center_window(splash_root)

    splash_root.mainloop()
