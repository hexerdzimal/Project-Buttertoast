import tkinter as tk

class GUILoader:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Buttertoast 0.1")

    def start_gui(self):
        label = tk.Label(self.root, text="Willkommen in der GUI!")
        label.pack(pady=20)
        
        button = tk.Button(self.root, text="Schließen", command=self.root.quit)
        button.pack(pady=20)
        
        self.root.mainloop()