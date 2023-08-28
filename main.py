from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps, ImageGrab
import ctypes

CANVAS_WIDTH = 1920
CANVAS_HEIGHT = 1080
BUTTON_BORDER = 7


class MainWindow:
    def __init__(self, main):
        # setup canvas
        self.canvas = Canvas(width=CANVAS_WIDTH, height=CANVAS_HEIGHT, highlightthickness=0)
        # setup image base
        self.file_target = "landing_image.png"
        image_base_raw = Image.open(self.file_target)
        self.original_size_x = image_base_raw.width
        self.original_size_y = image_base_raw.height
        image_base_raw = ImageOps.contain(image_base_raw, (CANVAS_WIDTH, CANVAS_HEIGHT))
        self.image_base = ImageTk.PhotoImage(image_base_raw)
        self.image_base_canvas = self.canvas.create_image(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2,
                                                          anchor="center", image=self.image_base)
        # setup image watermark
        self.image_watermark_raw = None
        self.image_watermark = None       
        self.watermark_image_canvas = self.canvas.create_image(CANVAS_WIDTH/2, CANVAS_HEIGHT/2,
                                                               anchor="center", image=self.image_watermark)
        self.image_watermark_scale = 1.0
        # setup text watermark
        self.text_watermark_size = 25
        self.watermark_text_canvas = self.canvas.create_text(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2,
                                                             text="", anchor="center", fill="white",
                                                             font=f"Arial {self.text_watermark_size} bold")
        self.canvas.grid(column=0, row=0, columnspan=24, pady=20)

        # control panel
        # row 1: base image controls
        browse_base_btn = Button(main, text="Browse Base Image", bd=BUTTON_BORDER,
                                 command=self.update_base_image)
        browse_base_btn.grid(column=1, row=1, columnspan=3)
        # row 2: image watermark controls
        browse_watermark_btn = Button(main, text="Browse Watermark Image", bd=BUTTON_BORDER,
                                      command=self.update_watermark_image)
        browse_watermark_btn.grid(column=1, row=2, columnspan=3, pady=10)
        loc1_label = Label(text="Position:")
        loc1_label.grid(column=5, row=2)
        left1_btn = Button(main, text="🡰", bd=BUTTON_BORDER,
                           command=lambda: self.update_watermark_pos("image", "left"))
        left1_btn.grid(column=6, row=2)
        right1_btn = Button(main, text="🡲", bd=BUTTON_BORDER,
                            command=lambda: self.update_watermark_pos("image", "right"))
        right1_btn.grid(column=7, row=2)
        up1_btn = Button(main, text="🡱", bd=BUTTON_BORDER,
                         command=lambda: self.update_watermark_pos("image", "up"))
        up1_btn.grid(column=8, row=2)
        down1_btn = Button(main, text="🡳", bd=BUTTON_BORDER,
                           command=lambda: self.update_watermark_pos("image", "down"))
        down1_btn.grid(column=9, row=2)
        size1_label = Label(text="Size:")
        size1_label.grid(column=11, row=2)
        plus1_btn = Button(main, text="➕", bd=BUTTON_BORDER,
                           command=lambda: self.update_watermark_size("image", "increase"))
        plus1_btn.grid(column=12, row=2)
        minus1_btn = Button(main, text="➖", bd=BUTTON_BORDER,
                            command=lambda: self.update_watermark_size("image", "decrease"))
        minus1_btn.grid(column=13, row=2)
        # row 3: text watermark controls
        text_label = Label(text="Text:")
        text_label.grid(column=1, row=3)
        self.text_entry = Entry(width=5)
        self.text_entry.grid(column=2, row=3, sticky="EW")
        text_btn = Button(main, text="Apply Text", bd=BUTTON_BORDER, command=self.update_text)
        text_btn.grid(column=3, row=3)
        loc2_label = Label(text="Position:")
        loc2_label.grid(column=5, row=3)
        left2_btn = Button(main, text="🡰", bd=BUTTON_BORDER,
                           command=lambda: self.update_watermark_pos("text", "left"))
        left2_btn.grid(column=6, row=3)
        right2_btn = Button(main, text="🡲", bd=BUTTON_BORDER,
                            command=lambda: self.update_watermark_pos("text", "right"))
        right2_btn.grid(column=7, row=3)
        up2_btn = Button(main, text="🡱", bd=BUTTON_BORDER,
                         command=lambda: self.update_watermark_pos("text", "up"))
        up2_btn.grid(column=8, row=3)
        down2_btn = Button(main, text="🡳", bd=BUTTON_BORDER,
                           command=lambda: self.update_watermark_pos("text", "down"))
        down2_btn.grid(column=9, row=3)
        size2_label = Label(text="Size:")
        size2_label.grid(column=11, row=3)
        plus2_btn = Button(main, text="➕", bd=BUTTON_BORDER,
                           command=lambda: self.update_watermark_size("text", "increase"))
        plus2_btn.grid(column=12, row=3)
        minus2_btn = Button(main, text="➖", bd=BUTTON_BORDER,
                            command=lambda: self.update_watermark_size("text", "decrease"))
        minus2_btn.grid(column=13, row=3)
        # save control
        save_btn = Button(main, text="Save\nImage", bd=BUTTON_BORDER,
                          command=self.save_image, height=5, width=10)
        save_btn.grid(column=15, row=1, columnspan=8, rowspan=3)

    def update_base_image(self):
        self.file_target = filedialog.askopenfilename(initialdir="/",
                                                      title="Select an Image",
                                                      filetypes=(('PNG', '*.png'),
                                                                 ('JPEG', ('*.jpg', '*.jpeg', '*.jpe')),
                                                                 ('BMP', '*.bmp'),
                                                                 ('GIF', '*.gif')))
        image_base_raw = Image.open(self.file_target)
        image_base_raw = ImageOps.contain(image_base_raw, (CANVAS_WIDTH, CANVAS_HEIGHT))
        self.original_size_x = image_base_raw.width
        self.original_size_y = image_base_raw.height
        self.image_base = ImageTk.PhotoImage(image_base_raw)
        self.canvas.itemconfig(self.image_base_canvas, image=self.image_base)

    def update_watermark_image(self):
        self.file_target = filedialog.askopenfilename(initialdir="/",
                                                      title="Select an Image",
                                                      filetypes=(('PNG', '*.png'),
                                                                 ('JPEG', ('*.jpg', '*.jpeg', '*.jpe')),
                                                                 ('BMP', '*.bmp'),
                                                                 ('GIF', '*.gif')))
        if self.file_target:
            self.image_watermark_raw = Image.open(self.file_target)
            self.image_watermark = ImageTk.PhotoImage(self.image_watermark_raw)
            self.canvas.itemconfig(self.watermark_image_canvas, image=self.image_watermark)

    def update_text(self):
        self.canvas.itemconfig(self.watermark_text_canvas, text=self.text_entry.get())

    def save_image(self):
        image_file = filedialog.asksaveasfilename(initialdir="/", title="Save Image", defaultextension="*.*",
                                                  filetypes=(('PNG', '*.png'),
                                                             ('JPEG', ('*.jpg', '*.jpeg', '*.jpe')),
                                                             ('BMP', '*.bmp'),
                                                             ('GIF', '*.gif')))
        if image_file:
            diff_canvas_image_x = (CANVAS_WIDTH - self.image_base.width()) / 2
            diff_canvas_image_y = (CANVAS_HEIGHT - self.image_base.height()) / 2
            x = self.canvas.winfo_rootx() + diff_canvas_image_x
            y = self.canvas.winfo_rooty() + diff_canvas_image_y
            x1 = x + self.image_base.width()
            y1 = y + self.image_base.height()
            final_image = ImageGrab.grab().crop((x, y, x1, y1)).resize((self.original_size_x, self.original_size_y))
            final_image.save(image_file)

    def update_watermark_pos(self, watermark_type, pos):
        if watermark_type == "image":
            target = self.watermark_image_canvas
        else:
            target = self.watermark_text_canvas

        if pos == "left":
            self.canvas.move(target, -20, 0)
        elif pos == "right":
            self.canvas.move(target, 20, 0)
        elif pos == "up":
            self.canvas.move(target, 0, -20)
        else:
            self.canvas.move(target, 0, 20)

    def update_watermark_size(self, watermark_type, size):
        if watermark_type == "image":
            if self.image_watermark_raw:
                if size == "increase":
                    self.image_watermark_scale = round(self.image_watermark_scale + 0.2, 1)
                else:
                    if self.image_watermark_scale > 0.2:
                        self.image_watermark_scale = round(self.image_watermark_scale - 0.2, 1)
                    else:
                        self.image_watermark_scale = 0.2

                original_width, original_height = self.image_watermark_raw.size
                new_width = int(original_width * self.image_watermark_scale)
                new_height = int(original_height * self.image_watermark_scale)
                self.image_watermark_raw = Image.open(self.file_target)
                resized_image = self.image_watermark_raw.resize((new_width, new_height))
                self.image_watermark = ImageTk.PhotoImage(resized_image)
                self.canvas.itemconfig(self.watermark_image_canvas, image=self.image_watermark)
        elif watermark_type == "text":
            if self.text_entry.get():
                if size == "increase":
                    self.text_watermark_size += 2
                else:
                    if self.text_watermark_size > 2:
                        self.text_watermark_size -= 2

            self.canvas.itemconfig(self.watermark_text_canvas, font=f"Arial {self.text_watermark_size} bold")


root = Tk()
root.title("Quick Watermark")
root.config(padx=10, pady=10)
ctypes.windll.shcore.SetProcessDpiAwareness(1)
root.tk.call('tk', 'scaling', 4)
MainWindow(root)
root.mainloop()
