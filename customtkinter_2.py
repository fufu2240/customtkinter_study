import customtkinter as ctk

class MyCheckBoxFrame(ctk.CTkFrame):
    def __init__(self, master,values):
        super().__init__(master)
        # self.checkbox_1= ctk.CTkCheckBox(self, text="checkbox 1")
        # self.checkbox_1.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        # self.checkbox_2 = ctk.CTkCheckBox(self, text="checkbox 2")
        # self.checkbox_2.grid(row=1, column=0, padx=10, pady=(10,0), sticky="w")
        # self.checkbox_3=ctk.CTkCheckBox(self, text="checkbox 3")
        # self.checkbox_3.grid(row=2, column=0, padx=10, pady=(10,0), sticky="w")
        self.values=values
        self.checkboxes=[]

        for i, value in enumerate(self.values):
            checkbox=ctk.CTkCheckBox(self, text=value)
            checkbox.grid(row=i, column=0, padx=10, pady=(10,0), sticky="w")
            self.checkboxes.append(checkbox)



    def get(self):
        checked_checkboxes = []
        # if self.checkbox_1.get() ==1:
        #     checked_checkboxes.append(self.checkbox_1.cget("text"))
        # if self.checkbox_2.get() ==1:
        #     checked_checkboxes.append(self.checkbox_2.cget("text"))  
        # if self.checkbox_3.get() ==1:
        #     checked_checkboxes.append(self.checkbox_3.cget("text"))  
        # return checked_checkboxes   


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("my app")
        self.geometry("400x180")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        self.checkbox_frame=MyCheckBoxFrame(self)
        self.checkbox_frame.grid(row=0, column=0, padx=10, pady=(10,0), sticky="nsw")

        self.button = ctk.CTkButton(self, text="my button", command=self.button_callback)
        self.button.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

    def button_callback(self):
        print("checked checkboxes:", self.checkbox_frame.get())

app=App()
app.mainloop()