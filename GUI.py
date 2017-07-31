import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
import time
#from AnimatedGif import *
import AvgPosGen as avg
from _thread import start_new_thread
import threading

def startDrone():
    class myThread (threading.Thread):
        def __init__(self, threadID, name, counter):
            threading.Thread.__init__(self)
            self.threadID = threadID
            self.name = name
            self.counter = counter
        def run(self):
            print ("Starting " + self.name)
            animate ()
            print ("Exiting " + self.name)



    def animate ():
        imagelist=[]
        for i in range (1,76):
            imagelist.append('Images/drone ('+str(i)+').gif')
           
               # extract width and height info
        photo = ImageTk.PhotoImage(file=imagelist[0])
        width = photo.width()
        height = photo.height()
        canvas = tk.Canvas(width=width, height=height,highlightthickness=0,)
        canvas.place(x=200, y=160)
        canvas.configure(background='white')
           # create a list of image objects
        giflist = []
        for imagefile in imagelist:
            photo = ImageTk.PhotoImage(file=imagefile)
            giflist.append(photo)
           # loop through the gif image objects for a while
        x=0    
        def recgif (list,i):
            if i==75:
                return None
            canvas.delete(ALL)
            canvas.create_image(width/2.0, height/2.0, image=list[i])
            canvas.update()
            time.sleep(0.04)
            i+=1
            recgif(list,i)
               
        while x<100:
            recgif(giflist,0)        
             

    thread1 = myThread(1,"Thread-1", 1)
    thread1.start()

def background_init(frame):
    load = Image.open("Images/background.png")
    render = ImageTk.PhotoImage(load)

    # labels can be text or images
    img = tk.Label(frame, image=render)
    img.image = render
    img.place(x=0, y=0)

def set_btn_bg(btn,path):
    load = Image.open(path)
    render = ImageTk.PhotoImage(load)
    btn.config(image=render)
    btn.image = render
    return btn

class AvgPos(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        #Chief icon:
        self.iconbitmap('Images/chief.ico')

        #Window label:
        self.title("Average Position Generator")

        self.frames = {}

        for F in (StartPage, inProgress, Stopped):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):

        def onClick_start ():
            opt=getV()
            print(opt)
            print(txtBox.get())
            try:
                value = int(txtBox.get())
                controller.show_frame(inProgress)
                startDrone()
##                if value>0:
##                    
##                    try:
##                        avg.start_pos(opt,value)
##                    except Exception:
##                        print("Connection Problem!")
##                else:
##                    print("only positive numbers")
            except Exception:
                print("unaccepted value")

        tk.Frame.__init__(self, parent)

        background_init(self)

        #instruction label:
        label = tk.Label(self, text="*Make sure that you have a static IP\n"
                                "*Make sure the mast DEBUG cable is connected\n",
                         justify="left")
        label.config(bg="white")
        label.place(x=180 , y=70)

        # radio buttons label
        radioLabel=tk.Label(self, text="Choose one option:\n")
        radioLabel.config(bg="white",font = "Arial 12 bold underline")
        radioLabel.place(x=220 , y=120)

        # radio buttons setup:
        timeChoises = [
            ("Seconds\n(40-400)", 3),
            ("Minutes\n(1-60)", 2),
            ("Hours\n(0.1-48)", 1),
        ]
        v = tk.IntVar()
        v.set(1)
        def getV():
           return v.get()

        for txt, val in timeChoises:
            radio=tk.Radiobutton(self,
                        text=txt,
                        padx=20,
                        variable=v,
                        value=val,
                        command=getV)
            x = int(val * 100)+50
            radio.config(bg="white")
            radio.place(x=x, y=150)

        # text box
        value=tk.StringVar()
        value.set("")

        txtLable=tk.Label(self, text="Time:")
        txtLable.config(font="Arial 9 bold underline", bg="white")
        txtLable.place(x=220, y=255)
        txtBox=tk.Entry(self)
        txtBox.place(x=270, y=255)

        txtLable2=tk.Label(self, text="COM Number:")
        txtLable2.config(font="Arial 9 bold underline", bg="white")
        txtLable2.place(x=178, y=230)
        txtBox=tk.Entry(self)
        txtBox.place(x=270, y=230)


        # start button
        button = ttk.Button(self, text="",
                            command=onClick_start)
        button = set_btn_bg(button, "Images/start_btn.png")
        button.place(x=200,y=320)

        # quit button
        button2 = ttk.Button(self, text="",
                            command=quit)
        button2=set_btn_bg(button2,"Images/quit_btn.png")
        button2.place(x=310 , y=320)


class inProgress(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        background_init(self)

        # in progress label:
        label = tk.Label(self, text="IN PROGRESS ...\n")
        label.config(bg="white", fg = "red",font = "Times 12 bold")
        label.place(x=225, y=95)

        label = tk.Label(self, text="*DO NOT disconnect the DEBUG cable\n"
                                    "*DO NOT turn of the computer\n",
                         justify="left")
        label.config(bg="white")
        label.place(x=200, y=120)

        # back button
        button = ttk.Button(self, text="back",
                            command=lambda: controller.show_frame(Stopped))
        button = set_btn_bg(button, "Images/back_btn.png")
        button.place(x=200,y=320)

        # quit button
        button2 = ttk.Button(self, text="Quit",
                             command=quit)
        button2 = set_btn_bg(button2, "Images/quit_btn.png")
        button2.place(x=310 , y=320)
    


    


class Stopped(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        background_init(self)

        # "you hav stoped" label:
        label = tk.Label(self, text="You have stoped the process ...\n")
        label.config(bg="white", fg="red", font="Times 12 bold")
        label.place(x=225, y=95)

        # start again button
        button1 = ttk.Button(self,
                            command=lambda: controller.show_frame(StartPage))
        button1 = set_btn_bg(button1, "Images/start_again_btn.png")
        button1.place(x=220,y=320)

        # quit button
        button2 = ttk.Button(self,
                             command=quit)
        button2 = set_btn_bg(button2, "Images/quit_btn.png")
        button2.place(x=320 , y=320)



app = AvgPos()


#Window size settings
app.minsize(600,450)
app.maxsize(600,450)

app.mainloop()
