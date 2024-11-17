import importlib
import os
import sys


class PluginLoader:
    def __init__(self, directory="plugins"):
        # Verzeichnis, in dem sich die Plugins befinden
        self.directory = directory  
    
    def get_extension(self, filename):
        # Extrahiert die Dateiendung
        _, extension = os.path.splitext(filename)
        return extension[1:]  # Entfernt den Punkt
    
    def get_plugin_name(self, extension):
        # Erstellt den Plugin-Namen basierend auf der Dateiendung
        return f"btp_{extension}"
    
    def load_and_run_plugin(self, filename, volume, host):
        """Lädt und führt das Plugin aus."""
        print(f"[DEBUG] Versuche, das Plugin für die Datei '{filename}' zu laden.")
        
        # Hole die Dateiendung und den Plugin-Namen
        extension = self.get_extension(filename)
        plugin_name = self.get_plugin_name(extension)
        print(f"[DEBUG] Gefundene Dateiendung: '{extension}', Plugin-Name: '{plugin_name}'")
        
        # Füge das Plugin-Verzeichnis zu sys.path hinzu
        sys.path.insert(0, self.directory)
        
        try:
            # Versuche, das Plugin-Modul zu importieren
            print(f"[DEBUG] Versuche, das Plugin '{plugin_name}' zu importieren und die Klasse zu laden...")
            plugin_module = importlib.import_module(plugin_name)
            class_name = extension.capitalize()
            plugin_class = getattr(plugin_module, class_name)
            
            # Erstelle eine Instanz der Plugin-Klasse und führe die 'run'-Methode aus
            print(f"[DEBUG] Erstelle eine Instanz von '{plugin_class.__name__}'...")
            plugin_instance = plugin_class()
            print(f"[DEBUG] Führe die run-Methode von '{plugin_class.__name__}' aus...")
            plugin_instance.run(host, volume)  # host und volume als binäre Daten weitergeben
            print(f"[DEBUG] '{plugin_class.__name__}' erfolgreich ausgeführt.")
            
        except (ModuleNotFoundError, AttributeError) as e:
            print(f"[ERROR] Fehler beim Laden des Plugins '{plugin_name}': {e}")
        except Exception as e:
            print(f"[ERROR] Fehler beim Ausführen des Plugins: {e}")
        finally:
            # Entferne das Plugin-Verzeichnis aus sys.path
            sys.path.pop(0)
    
    def list_plugins(self):
        loaded_plugins = []
        
        if not os.path.exists(self.directory):
            print(f"[ERROR] Plugin-Verzeichnis '{self.directory}' nicht gefunden.")
            return loaded_plugins

        print(f"Verfügbare Plugins im Verzeichnis '{self.directory}':")
        for filename in os.listdir(self.directory):
            # Direkt prüfen, ob die Datei mit "btp_" beginnt und mit ".py" endet
            if filename.startswith("btp_") and filename.endswith(".py") and filename != "__init__.py":
                plugin_name = filename[:-3]  # Entfernt die Dateiendung ".py"
                try:
                    print(f"{plugin_name}")
                except Exception as e:
                    print(f"[ERROR] Fehler beim Laden des Plugins '{plugin_name}': {e}")
        
        return loaded_plugins
    
    def test_plugin(self, filename):
        # Hauptmethode zum Laden und Testen eines Plugins basierend auf dem Dateityp
        print(f"[DEBUG] Teste das Plugin für die Datei '{filename}'.")

        # Hole die Dateiendung und Plugin-Name
        extension = self.get_extension(filename)
        plugin_name = self.get_plugin_name(extension)
        print(f"[DEBUG] Gefundene Dateiendung: '{extension}', Plugin-Name: '{plugin_name}'")

        # Füge das Plugin-Verzeichnis zu sys.path hinzu
        sys.path.insert(0, self.directory)

        try:
            # Versuche, das Plugin-Modul zu importieren
            print(f"[DEBUG] Versuche, das Plugin '{plugin_name}' zu importieren und die Klasse zu laden...")
            plugin_module = importlib.import_module(plugin_name)
            class_name = extension.capitalize()
            plugin_class = getattr(plugin_module, class_name)
            
            # Erstelle eine Instanz der Plugin-Klasse und führe die 'run'-Methode aus
            print(f"[DEBUG] Erstelle eine Instanz von '{plugin_class.__name__}' für den Test...")
            plugin_instance = plugin_class()
            
            print(f"[DEBUG] Führe die run-Methode von '{plugin_class.__name__}' im Testmodus aus...")
            plugin_instance.run()  # Da es ein Test ist, wird keine Datei übergeben
            print(f"[DEBUG] '{plugin_class.__name__}' erfolgreich im Testmodus ausgeführt.")

        except (ModuleNotFoundError, AttributeError) as e:
            print(f"[ERROR] Fehler beim Laden des Plugins '{plugin_name}': {e}")
        except Exception as e:
            print(f"[ERROR] Fehler beim Ausführen des Plugins im Testmodus: {e}")
        finally:
            # Entferne das Plugin-Verzeichnis aus sys.path
            sys.path.pop(0)
