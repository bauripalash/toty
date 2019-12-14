from tkinter import *
from tkinter import font
from tkinter import ttk
import pyotp
import pickledb


class Window(Frame):
    def __init__(self , master=None):
        Frame.__init__(self,master)
        self.master = master
        self.DB = pickledb.load("./toty.db" , True)
        self.DB.set("GIthub (bauripalash)" , "base32secret2332")
        self.init_window()

    def init_window(self):
        self.master.title("TOTY Authenticator")
        self.pack(fill=BOTH , expand=1)
        self.listfont = font.Font(size=20)
        self.addbtn_font = font.Font(size=16)
        self.outputbox_font = font.Font(size=35)
        # print(font.families())

        self.init_widgets()
    
    def init_widgets(self):

        self.add_icon = PhotoImage(file = "./res/add-icon.png")
        self.del_icon = PhotoImage(file = "./res/del-icon.png")

        # self. = PhotoImage(file = "res/add-icon.png") 
        # small_logo = photo.subsample(5,5)
        self.authlist = Listbox(self , font=self.listfont, bg="lightblue")
        self.authlist.pack(fill=BOTH , expand=1 , side=TOP)

        self.outputbox_text = StringVar()
        self.outputbox = Entry(self,textvariable=self.outputbox_text , font=self.outputbox_font)
        self.outputbox.pack(fill=BOTH , expand=0 , side=TOP)


        self.addbtn = Button(self , text="Add +" , font=self.addbtn_font)
        self.addbtn.config(image = self.add_icon, compound = "left" , command = self.AddNew)
        self.addbtn.pack(fill=BOTH , expand=1 ,side=LEFT)
        
        
        self.delbtn = Button(self , text="", height=2, width=50, font=self.addbtn_font)
        self.delbtn.config(image = self.del_icon , compound="left" , command = self.DelSelected)
        self.delbtn.pack(fill=BOTH , expand=0 ,side=LEFT)

        for item in self.GetAllAuths():
            self.authlist.insert(END, item)

        self.authlist.bind('<<ListboxSelect>>', self.authlist_select)

    def authlist_select(self,event):
        # print(type(self.GetAllAuths()) , self.GetAllAuths())
        self.outputbox_text.set(pyotp.TOTP(self.DB.get(self.GetAllAuths()[self.authlist.curselection()[0]])).now())
    
    def GetAllAuths(self):
        return list(self.DB.getall())

    def AddNew(self):
        print("Adding New")
        

    def DelSelected(self):
        print("Deleting : " , self.GetAllAuths()[self.authlist.curselection()[0]])

def main():
    
    # all_auths = GetAllAuths(DB)
    root = Tk()
    root.geometry("640x580")
    app = Window(root)
    app.mainloop()

main()    