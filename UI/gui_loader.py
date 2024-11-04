import tkinter as tk



class GUILoader:
    def __init__(self, image_path):
        self.root = tk.Tk()
        self.root.title("Buttertoast 0.1")
        
        # Lade das Hintergrundbild direkt mit Tkinter
        self.background_photo = tk.PhotoImage(file=image_path)

        # Erstelle ein Label mit dem Bild und zentriere es
        self.background_label = tk.Label(self.root, image=self.background_photo)
        self.background_label.image = self.background_photo  # Referenz halten, um Garbage Collection zu verhindern
        self.background_label.pack(expand=True)  # Zentriere das Bild im Fenster

    def start_gui(self):
        label = tk.Label(self.root, text="Willkommen in der GUI!", bg="white")  # Setze den Hintergrund auf weiß
        label.pack(pady=20)
        
        button = tk.Button(self.root, text="Schließen", command=self.root.quit)
        button.pack(pady=20)
        
        self.root.mainloop()

        #gsg