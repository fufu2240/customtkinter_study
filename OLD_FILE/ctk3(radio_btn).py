import customtkinter as ctk

class MyCheckBoxFrame(ctk.CTkFrame):
    def __init__(self, master,title, values):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.title=title
        self.checkboxes = []

        self.title=ctk.CTkLabel(self, text=self.title, fg_color="gray", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")
        

        for i, value in enumerate(self.values):
            checkbox = ctk.CTkCheckBox(self, text=value)
            checkbox.grid(row=i+1, column=0, padx=10, pady=(10, 0), sticky="w")
            self.checkboxes.append(checkbox)

    def get(self):
        checked_checkboxes = []
        for checkbox in self.checkboxes:
            if checkbox.get() == 1:
                checked_checkboxes.append(checkbox.cget("text"))
        return checked_checkboxes

class MyRadiobuttonFrame(ctk.CTkFrame):
    def __init__(self, master,title, values):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.title=title
        self.checkboxes = []
        self.variale= ctk.StringVar(value="")

        self.title=ctk.CTkLabel(self, text=self.title, fg_color="gray", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

        for i, value in enumerate(self.values):
            radiobutton = ctk.CTkRadioButton(self, text=value, value=value, variable=self.variale)
            radiobutton.grid(row=0 , column=0, padx=10, pady=(10, 0), sticky="w")
            self.radiobuttons.append(radiobutton)
    
    def get(self):
        return self.variale.get()
    
    def set(self, value):
        self.variale



class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("my app")
        self.geometry("400x220")
        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.checkbox_frame=MyCheckBoxFrame(self, "Values", values=["value 1", "value 2", "value 3"])
        self.checkbox_frame.grid(row=0, column=0, padx=10, pady=(10,0), sticky="nsw")
        self.radiobutton=MyCheckBoxFrame(self, "Options", values=["option 1", "option 2"])
        self.radiobutton.grid(row=0, column=1, padx=(0,10), pady=(10,0), sticky="nsw")
        

        self.button = ctk.CTkButton(self, text="my button", command=self.button_callback)
        self.button.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

    def button_callback(self):
        print("checked_frame:", self.checkbox_frame.get())
        print("radiobutton:", self.radiobutton.get())

app=App()
app.mainloop()