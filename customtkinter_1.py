import customtkinter as ctk

# def button_callback():
#     app.counter +=1
#     print("Button clicked!, 버튼을 클릭하다")
#     if app.counter >=10:
#         print("누른 횟수가", app.counter, "번이다", "그만 눌러")
   

# app = ctk.CTk()
# app.counter=0
# app.geometry("400x150")
# app.grid_columnconfigure(0, weight=1)

# button=ctk.CTkButton(app, text="마이 바똔", command=button_callback)
# #button.pack(padx=20, pady=20)
# button.grid(row=0, column=0,padx=20, pady=20, sticky="ew", columnspan=2)
# checkbox_1= ctk.CTkCheckBox(app, text="체크박스 1")
# checkbox_1.grid(row=1, column=0, padx=20, pady=(0,20), sticky="w")
# checkbox_2 = ctk.CTkCheckBox(app, text="체크박스 2")
# checkbox_2.grid(row=1, column=1, padx=20, pady=(0,20), sticky="w")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("my app")
        self.geometry("400x150")
        self.grid_columnconfigure(0, weight=1)

        self.button = ctk.CTkButton(self, text="my button", command=self.button_callback)
        self.button.grid(row=0, column=0, padx=20, pady=20, sticky="ew", columnspan=2)
        self.checkbox_1= ctk.CTkCheckBox(self, text="체크박스 1")
        self.checkbox_1.grid(row=1, column=0, padx=20, pady=(0,20), sticky="w")
        self.checkbox_2 = ctk.CTkCheckBox(self, text="체크박스 2")
        self.checkbox_2.grid(row=1, column=1, padx=20, pady=(0,20), sticky="w")

    def button_callback(self):
        print("button clicked!")

app=App()
app.mainloop()