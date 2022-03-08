from tkinter import *
from pytube import*
from tkinter import ttk
from PIL import Image,ImageTk
import requests
import io
import os

class Youtube_app:
    def __init__(self, root):

        self.root = root
        self.root.title("Youtube Dowanloader.Developed By Fahad")
        self.root.geometry("500x420+300+50")
        self.root.resizable(False,False)
        self.root.config(bg='white')

        title=Label(self.root,text='  Youtube Dowanloader.Developed By Fahad',font=("times new roman",15),bg="#262626",fg="white",anchor="w").pack(side=TOP,fill=X)
        self.var_url=StringVar()
        lbl_url=Label(self.root,text='Video url',font=("times new roman",15,'bold'),bg="white").place(x=10,y=50)
        entry = Entry(self.root,font=("times new roman", 13),textvariable=self.var_url, bg="lightyellow").place(x=120, y=50,width=350)
        file_type = Label(self.root, text='File Type', font=("times new roman", 15, 'bold'), bg="white").place(x=10, y=90)

        self.var_fillType=StringVar()
        self.var_fillType.set('Video')
        video_radio=Radiobutton(self.root, text='Video',variable=self.var_fillType,value='Video', font=("times new roman", 13), bg="white",activebackground="white").place(x=120, y=90)

        audio_radio = Radiobutton(self.root, text='Audio',variable=self.var_fillType,value='Audio', font=("times new roman", 13), bg="white",activebackground="white").place(x=220, y=90)

        btn_search=Button(self.root,text="Search",command=self.search,font=('times new roman',15),bg='blue',fg='white').place(x=300,y=90,height=30,width=120)

        frame1=Frame(self.root,bd=2,relief=RIDGE,bg='lightyellow')
        frame1.place(x=10,y=130,width=480,height=180)

        self.video_title = Label(frame1,text='Video Title Here', font=("times new roman", 12),bg="lightgray", fg="white", anchor="w")
        self.video_title.place(x=0,y=0,relwidth=1)

        self.video_image = Label(frame1, text='Video \nImage', font=("times new roman", 15), bg="lightgray",bd=2,relief=RIDGE)
        self.video_image.place(x=5,y=30, width=180,height=140)

        lbl_desc = Label(frame1, text='Description', font=("times new roman", 15), bg="lightyellow").place(x=190,y=30)

        self.video_desc =Text(frame1,font=("times new roman", 12), bg="lightyellow")
        self.video_desc.place(x=190,y=60, width=280,height=110)

        self.lbl_size = Label(self.root, text='Total Size:', font=("times new roman", 15), bg="white")
        self.lbl_size.place(x=10, y=320)

        self.lbl_percentage = Label(self.root, text='Dowanloading:', font=("times new roman", 15), bg="white")
        self.lbl_percentage.place(x=160, y=320)

        btn_clear= Button(self.root, text="Clear",command=self.clear,font=('times new roman', 13), bg='blue', fg='white').place(x=350,y=320,height=25,width=70)
        self.btn_dowanload = Button(self.root, text="Download",state=DISABLED,command=self.dowanload,font=('times new roman', 13), bg='green', fg='white')
        self.btn_dowanload.place(x=410, y=320, height=25,width=90)

        self.prog=ttk.Progressbar(self.root,orient=HORIZONTAL,length=590,mode='determinate')
        self.prog.place(x=10,y=360,width=485,height=20)

        self.lbl_message = Label(self.root, text='', font=("times new roman", 13), bg="white")
        self.lbl_message.place(x=0, y=385,relwidth=1)

        if os.path.exists('Audios')==FALSE:
            os.mkdir('Audios')
        if os.path.exists('Videos')==FALSE:
            os.mkdir('Videos')

#====================================================================================================================================================================================
    def search(self):
        if self.var_url.get()=='':
            self.lbl_message.config(text="Video URL is Required",fg='red')
        else:
            yt = YouTube(self.var_url.get())
    #======convert image url to image======

            response=requests.get(yt.thumbnail_url)
            img_byte=io.BytesIO(response.content)
            self.img=Image.open(img_byte)
            self.img=self.img.resize((180,140),Image.ANTIALIAS)
            self.img=ImageTk.PhotoImage(self.img)
            self.video_image.config(image=self.img)

        #=======fatch as the size as  per type=====
            if self.var_fillType.get()=='Video':
                select_file=yt.streams.filter(progressive=TRUE).first()
            if self.var_fillType.get()=='Audio':
                select_file=yt.streams.filter(only_audio=TRUE).first()

            self.size_inBytes=select_file.filesize
            max_size=self.size_inBytes/1024000
            self.mb=str(round(max_size,2))+"MB"

            #====updating the frame elements=======
            self.lbl_size.config(text='Total Size: '+self.mb)
            self.video_title.config(text=yt.title)
            self.video_desc.delete("1.0",END)
            self.video_desc.insert(END,yt.description[:200])
            self.btn_dowanload.config(state=NORMAL)

    def progress_(self,streams,chunk,bytes_remanining):
        percentage=(float(abs(bytes_remanining-self.size_inBytes)/self.size_inBytes))*float(100)
        self.prog['value']=percentage
        self.prog.update()
        self.lbl_percentage.config(text=f'Dowanloading: {str(round(percentage,2))}%')
        if round(percentage,2)==100:
            self.lbl_message.config(text="Dowanload Complete",fg="green")
            self.btn_dowanload.config(state=DISABLED)
    def clear(self):
        self.var_fillType.set("Video")
        self.var_url.set('')
        self.prog['value']=0
        self.btn_dowanload.config(state=DISABLED)
        self.lbl_message.config(text='')
        self.video_title.config(text='Video Title Here')
        self.video_image.config(image='')
        self.video_desc.delete('1.0',END)
        self.lbl_size.config(text="Total Size: MB")
        self.lbl_percentage.config(text="Dowanloading:0%")

    def dowanload(self):
        yt = YouTube(self.var_url.get(),on_progress_callback=self.progress_)
        # =======fatch as the size as  per type=====
        if self.var_fillType.get() == 'Video':
            select_file = yt.streams.filter(progressive=TRUE).first()
            select_file.download("Videos/")
        if self.var_fillType.get() == 'Audio':
            select_file = yt.streams.filter(only_audio=TRUE).first()
            select_file.download("Audios/")





root = Tk()
obj = Youtube_app(root)
root.mainloop()
