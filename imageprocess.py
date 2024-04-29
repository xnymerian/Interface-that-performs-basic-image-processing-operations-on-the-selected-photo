# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 11:47:44 2024

@author: Lenovo
"""
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

img_label = None
original_image = None
filename = None
button2_pressed = False  

new_width = 800
new_height = 800



def browse_image():
    global filename, original_image, img_label  
    filename = filedialog.askopenfilename(initialdir="/", title="Select Image", filetypes=(("Image files", "*.jpg *.png"), ("all files", "*.*")))
    print("Selected File:", filename)
    if filename:
        original_image = Image.open(filename)
        original_image = original_image.resize((600, 600), Image.BILINEAR)
        original_photo = ImageTk.PhotoImage(original_image)
        if img_label:
            img_label.config(image=original_photo)  
            img_label.image = original_photo
        else:
            img_label = Label(framey, image=original_photo)
            img_label.pack(pady=20)
            
 

def update_image(filename):
    global photo, img_label, button2_pressed
    if not filename:
        if original_image:
            image = original_image
        else:
            return
    else:
        image = Image.open(filename)
    
    image = image.resize((600, 600), Image.BILINEAR)
    if button2_pressed:
        
        bw_factor = bw_scale.get()
        image = image.convert("L")
        threshold = int((255 * bw_factor) / 100)
        image = image.point(lambda p: p > threshold and 255)
    
    photo = ImageTk.PhotoImage(image)
    img_label.config(image=photo)
    img_label.image = photo
    
def update_image1(filename,w,h):
    global photo, img_label, button2_pressed
    if not filename:
        if original_image:
            image = original_image
        else:
            return
    else:
        image = Image.open(filename)
    
    image = image.resize((w, h), Image.LANCZOS)
    if button2_pressed:
        
        bw_factor = bw_scale.get()
        image = image.convert("L")
        threshold = int((255 * bw_factor) / 100)
        image = image.point(lambda p: p > threshold and 255)
    
    photo = ImageTk.PhotoImage(image)
    img_label.config(image=photo)
    img_label.image = photo   
    
def update_image2(filename,w,h,degree):
     global photo, img_label, button2_pressed
     if not filename:
         if original_image:
             image = original_image
         else:
             return
     else:
         image = Image.open(filename)
     
     image = image.resize((w, h), Image.BILINEAR)
     image = image.rotate(degree,expand=True)
     if button2_pressed:
         
         bw_factor = bw_scale.get()
         image = image.convert("L")
         threshold = int((255 * bw_factor) / 100)
         image = image.point(lambda p: p > threshold and 255)
     
     photo = ImageTk.PhotoImage(image)
     img_label.config(image=photo)
     img_label.image = photo       
    

               

def show_histogram():
    if not filename:
        return
    
    image = Image.open(filename)
    image = image.resize((800, 800), Image.BILINEAR)
    image = image.convert("L")
    
    plt.hist(image.histogram(), bins=256, color='gray', alpha=0.7)
    plt.xlabel('Pixel Değeri')
    plt.ylabel('Frekans')
    plt.title('Histogram Grafiği')
    plt.grid(True)
    
    hist_window = Toplevel(master)
    hist_window.title("Histogram")
    hist_window.geometry("800x600")
    
    canvas = FigureCanvasTkAgg(plt.gcf(), master=hist_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=True)

def rotate_image(filename,degrees):
    
    if not filename:
        if original_image:
            rotated_image = original_image.rotate(degrees, expand=True)
            update_image(rotated_image)
    else:
        image = Image.open(filename)
        rotated_image = image.rotate(degrees, expand=True)
        update_image(rotated_image)


master=Tk()
master.title("mehmet's gui")
master.geometry("1680x1680")

canvas=Canvas(master,height=450,width=900)
framex=Frame(master,bg="#590318")
framex.place(relx=0.1,rely=0.1,relwidth=0.1,relheight=0.80)
framey=Frame(master,bg="#add8e6")
framey.place(relx=0.21,rely=0.1,relwidth=0.60,relheight=0.80)

etiket=Label(framey,text="Görüntü Çıktısı",)
etiket.pack(pady=10)

img_label = None
select_image_btn = Button(framex, text="Resim Aç", command=browse_image)
select_image_btn.pack(pady=5,padx=10)

button2 = Button(framex, text=" resim düzelt", command=lambda: update_image(filename if filename else original_image))
button2.pack(pady=10,padx=10)

bw_scale = Scale(framex, from_=0, to=100, orient=HORIZONTAL, label="Eşik değeri", command=lambda value: update_image(filename if filename else original_image))
bw_scale.pack(pady=10, padx=10)

button3 = Button(framex, text=" Histogramı Göster", command=show_histogram)
button3.pack(pady=10,padx=10)

width_scale = Scale(framex, from_=100, to=1600, orient=HORIZONTAL, label="Genişlik", command=lambda value: update_image1(filename if filename else original_image, int(value), new_height))
width_scale.set(new_width)  
width_scale.pack(pady=10, padx=10)

height_scale = Scale(framex, from_=100, to=1600, orient=HORIZONTAL, label="Yükseklik", command=lambda value: update_image1(filename if filename else original_image, new_width, int(value)))
height_scale.set(new_height)  
height_scale.pack(pady=10, padx=10)


button6 = Button(framex, text=" zoom in",command=lambda: update_image1(filename if filename else original_image,1500,1500))
button6.pack(pady=10,padx=10)

button7 = Button(framex, text=" zoom out",command=lambda: update_image1(filename if filename else original_image,200,200))
button7.pack(pady=10,padx=10)

degree_scale = Scale(framex, from_=0, to=360, orient=HORIZONTAL, label="Döndür", command=lambda value: update_image2(filename if filename else original_image, new_width, new_height, int(value)))
degree_scale.pack(pady=10, padx=10)



def on_button2_pressed(event):
    global button2_pressed
    button2_pressed = True
    update_image(filename if filename else original_image)

def on_button2_released(event):
    global button2_pressed
    button2_pressed = False
    update_image(filename if filename else original_image)

button2.bind("<ButtonPress>", on_button2_pressed)
button2.bind("<ButtonRelease>", on_button2_released)

master.mainloop()

















