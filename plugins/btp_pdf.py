from Engine.plugin_Interface import plugin_Interface

class Pdf(plugin_Interface):
    def run(self):
        print("""[SUCCESS]If you can read this, it means that you successfully loaded and executed
              the pdf-File-Plugin!
               """)