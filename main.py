import tkinter
from tkinter import *
from tkinter import font
from tkinter import ttk
import pyotp
import pickledb

class NewAuthtBox(object):

    root = None

    def __init__(self , dict_key):
        self.top = Toplevel(NewAuthtBox.root)
        self.top.geometry("500x200")
        main_frame = Frame(self.top, borderwidth=4, relief='ridge' )
        main_frame.pack(fill=BOTH, expand=1)

        self.new_font = font.Font(size=21)

        account_label = Label(main_frame, text="Account Name :" , font=self.new_font)
        account_label.pack(fill = BOTH , expand = 0 , padx=4, pady=4)

        # caller_wants_an_entry = dict_key is not None

        # if caller_wants_an_entry:
        self.account_entry = Entry(main_frame , font=self.new_font)
        self.account_entry.pack(fill = X , expand = 0 ,pady=4)

        key_label = Label(main_frame, text="Your Key :", font=self.new_font)
        key_label.pack(fill = BOTH , expand = 0 ,padx=4, pady=4)

        # caller_wants_an_entry = dict_key is not None

        # if caller_wants_an_entry:
        self.key_entry = Entry(main_frame, font=self.new_font)
        self.key_entry.pack(fill = BOTH , expand = 0 ,pady=4)

        b_submit = Button(main_frame, text='Save', font=self.new_font)
        b_submit['command'] = lambda: self.entry_to_dict(dict_key)
        b_submit.pack(fill = X , expand = 1 , side = LEFT)

        b_cancel = Button(main_frame, text='Cancel', font=self.new_font)
        b_cancel['command'] = self.top.destroy
        b_cancel.pack(fill=X, side=LEFT)

    def entry_to_dict(self, dict_key):
        account_data = self.account_entry.get()
        key_data = self.key_entry.get()
        if account_data and key_data:
            # d, key = dict_key
            # d[key] = data
            # d = {"account" : account_data , "key" : key_data}
            # d,key = dict_key
            dict_key["account"] = account_data
            dict_key['key'] = key_data
            print(dict_key)
            self.top.destroy()


class Window(Frame):
    def __init__(self , master=None):
        Frame.__init__(self,master)
        self.master = master
        self.DB = pickledb.load("./toty.db" , True)
        self.DB.set("GIthub (bauripalash)" , "base32secret2332")
        self.Mbox = NewAuthtBox
        self.Mbox.root = self.master
        self.D = {"account" : "" , "key" : ""}
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
        self.addbtn.config(image = self.add_icon, compound = "left" , command = lambda: self.AddNew())
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
        self.NEWx = self.Mbox(self.D)
        self.master.wait_window(self.NEWx.top)
        # print("X" , self.D)
        self.DB.set(self.D["account"] , self.D["key"])
        self.authlist.insert(END , self.D["account"])
        

    def DelSelected(self):
        print("Deleting : " , self.GetAllAuths()[self.authlist.curselection()[0]])

def main():
    
    # all_auths = GetAllAuths(DB)
    root = Tk()
    root.geometry("640x580")
    app = Window(root)
    app.mainloop()

main()    