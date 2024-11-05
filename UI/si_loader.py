from Engine.plugin_Loader import PluginLoader

class SILoader:
    def __init__(self):
        self.plugin_loader = PluginLoader()
        

    def start_txt(self):

        print (r"""

               
                 
             +===================================================================================================+
            |                                                                         Version: 0.1 (burnt) 2024 |
            |   ██████╗ ██╗   ██╗████████╗████████╗███████╗██████╗ ████████╗ ██████╗  █████╗ ███████╗████████╗  |
            |   ██╔══██╗██║   ██║╚══██╔══╝╚══██╔══╝██╔════╝██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗██╔════╝╚══██╔══╝  |
            |   ██████╔╝██║   ██║   ██║      ██║   █████╗  ██████╔╝   ██║   ██║   ██║███████║███████╗   ██║     |
            |   ██╔══██╗██║   ██║   ██║      ██║   ██╔══╝  ██╔══██╗   ██║   ██║   ██║██╔══██║╚════██║   ██║     |
            |   ██████╔╝╚██████╔╝   ██║      ██║   ███████╗██║  ██║   ██║   ╚██████╔╝██║  ██║███████║   ██║     |
            |   ╚═════╝  ╚═════╝    ╚═╝      ╚═╝   ╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝   ╚═╝     |
            |                                    The melting pot of polyglot.                                   |
            +===================================================================================================+
                                            by Fabian Kozlowski, Stefan Leippe, Malte Muthesius, Matthias Ferstl
               

                            

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
            flow = input('Enter "1" to list plugins, enter "2" to quit: ')
            if flow == "1":
                print("Listing plugins.")
                self.plugin_loader.list_plugins()  # Plugins abrufen
                
                break
            elif flow == "2":
                print("Quitting program.")
                break
            else:
                print("Invalid input. Please enter '1' or '2'.")
        
        input('Press ENTER to exit')