from Engine.plugin_loader import PluginLoader

class SILoader:
    def __init__(self):
        self.plugin_loader = PluginLoader()

    def start_txt(self):

        print (r"""

             Version: Burnt (0.1)                             by Fabian Kozlowski, Stefan Leippe, Matthias Ferstl
             +===================================================================================================+
            |   ██████╗ ██╗   ██╗████████╗████████╗███████╗██████╗ ████████╗ ██████╗  █████╗ ███████╗████████╗  |
            |   ██╔══██╗██║   ██║╚══██╔══╝╚══██╔══╝██╔════╝██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗██╔════╝╚══██╔══╝  |
            |   ██████╔╝██║   ██║   ██║      ██║   █████╗  ██████╔╝   ██║   ██║   ██║███████║███████╗   ██║     |
            |   ██╔══██╗██║   ██║   ██║      ██║   ██╔══╝  ██╔══██╗   ██║   ██║   ██║██╔══██║╚════██║   ██║     |
            |   ██████╔╝╚██████╔╝   ██║      ██║   ███████╗██║  ██║   ██║   ╚██████╔╝██║  ██║███████║   ██║     |
            |   ╚═════╝  ╚═════╝    ╚═╝      ╚═╝   ╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝   ╚═╝     |
            +===================================================================================================+

                Hiding things in files since 2024, just like butter that "integrates" in a warm toast.

            """)


        print("Open Hub, this is the police! Please state your name:")
        
        name = input("Your name: ")
        print("Thanks for being here with us, " + name + "!")
        print("What is your favourite toast?")
        
        magicKey = input("We know you want it too: ")
        if magicKey == "Buttertoast":
            print("Great! So now, lets do some work!")
        else:  
            print("Disappointing!")
        
        while True:
            flow = input('Enter "1" to load plugins and execute their code, enter "2" to quit: ')
            if flow == "1":
                print("Plugins loaded. Executing code.")
                plugins = self.plugin_loader.load_plugins()
                for plugin in plugins:
                    plugin.run()
                break
            elif flow == "2":
                print("Quitting program.")
                break
            else:
                print("Invalid input. Please enter '1' or '2'.")
        
        input('Press ENTER to exit')