from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog 
import numpy
import convertor

class Window(Frame):
    def __init__(self, master=None):
# create screen widgets
        self.box = Text(root)
        self.box.config(state='disabled')
        self.info = Label(root, text='Original Image :')
        self.info2 = Label(root, text='Decryption Image : ')
        self.info3 = Label(root, text='Encryption (part of) : ')
        self.info4 = Label(root, text='Mode is "ECB" or "CBC"')
        self.info5 = Label(root, text='Rounds in ( 1 to 255 )')
        self.info6 = Label(root, text='"All variables have a defalt values"')
        self.lbl = Label(root, text='Key')
        self.lbl2 = Label(root, text='Mode')
        self.lbl3 = Label(root, text='Rounds')
        self.btn = Button(root, text ='open image', command = self.open_img)
        self.btn.place(x=450, y=500, width = 100, height = 25)
        self.info.place(x=10, y=5)
        self.info2.place(x=310, y=5)
        self.info3.place(x=10, y=305)
        self.box.place(x=25, y=335,width = 250, height = 250) 
# place variables form
        self.info6.place(x=380, y=305)
        self.lbl.place(x=350, y=345)
        self.lbl2.place(x=350, y=395)
        self.lbl3.place(x=350, y=435)
        self.t = Entry(bd=3)
        self.t.place(x=430, y=345 ,width=150)
        self.info4.place(x=430, y=375)
        self.info5.place(x=430, y=415)
        self.t2 = Entry(bd=3)
        self.t2.place(x=430, y=395 ,width=150)
        self.t3 = Entry(bd=3)
        self.t3.place(x=430, y=435 ,width=150)

# get key variable and display defalt value if it is empty
    def getKey(self):
        key = self.t.get().lower()
        if key == '' :
            key = 'pig'
        return key
# get mode variable and display defalt value if it is empty
    def getMode(self):
        mode = self.t2.get().upper()
        return mode
# get rounds variable and display defalt value if it is empty
    def getRounds(self):
        rounds = self.t3.get().upper()
        if rounds != '' :
            rounds = int(rounds)
        else:
            rounds = 16
        return rounds
    def open_img(self): 
        # Select the Imagename from a folder 
        x = self.openfilename()
        # opens the image 
        img = Image.open(x) 
        img_Width , img_Height = img.size
        # convert image to numoy array
        pix = numpy.array(img)
        # get main variables for encrepthions
        window , windowsize_r , windowsize_c = convertor.original(pix,img_Width,img_Height)
        new_pix = numpy.block(window)
        # get variables from user
        key = self.getKey()
        mode = self.getMode()
        rounds = self.getRounds()
        # get encryting result
        enc = convertor.encrypt(window,windowsize_r,windowsize_c,key,rounds,mode)
        # diplay part of the encryption string array on screen
        self.box.config(state='normal')
        self.box.delete('1.0','end')
        self.box.insert('end', str([enc[c] for c in range(1,20)]))
        self.box.config(state='disabled')
        # get decryption result
        res = convertor.decrypt(enc,windowsize_r,windowsize_c,key,rounds,mode)
        # concert decrept arrar to numby image block
        de_pix = numpy.block(res)
        # PhotoImage class is used to add image to widgets, icons etc 
        new_pix = ImageTk.PhotoImage(image=Image.fromarray(new_pix))
        de_pix = ImageTk.PhotoImage(image=Image.fromarray(de_pix))
        # create a label 
        panel1 = Label(root, image = new_pix) 
        panel2 = Label(root, image = de_pix) 
        # set the image 
        panel1.image = new_pix 
        panel2.image = de_pix 
        panel2.place(x=325, y=25, width = 250, height = 250)
        panel1.place(x=25, y=25, width = 250, height = 250)
    # get the image from user
    def openfilename(self): 
        # open file dialog box to select image 
        # The dialogue box has a title "Open" 
        filename = filedialog.askopenfilename(title ='Open')
        return filename 

        
root = Tk()
app = Window(root)
root.wm_title("Image Encryption")
root.geometry("600x600")
root.resizable(width = False , height = False) 
root.mainloop()