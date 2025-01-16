import os
from PIL import Image

def rename_resize_generate_html(directory, output_html_file):
    # Überprüfen, ob das Verzeichnis existiert
    if not os.path.isdir(directory):
        print(f"Das Verzeichnis {directory} existiert nicht.")
        return
    
    count = 1
    image_entries = []  # Für die HTML-Bildabschnitte

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif')):
            try:
                with Image.open(file_path) as img:
                    # Sicherstellen, dass das Bild RGB-Modus verwendet
                    img = img.convert("RGB")
                    
                    # Neue Auflösung berechnen (75% der Originalgröße)
                    scale_factor = 0.12
                    new_width = max(1, int(img.width * scale_factor))
                    new_height = max(1, int(img.height * scale_factor))
                    
                    # Bild skalieren
                    img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    
                    # Neuen Dateinamen generieren
                    new_name = f"praline{count}.png"
                    new_path = os.path.join(directory, new_name)
                    
                    # Bild speichern
                    img_resized.save(new_path, "PNG")
                    
                    # Originaldatei löschen (optional)
                    # os.remove(file_path)
                    
                    # HTML für das Bild erstellen
                    image_entries.append(
                        f'    <div class="slides">\n'
                        f'        <img src="img/{new_name}" alt="Praline {count}">\n'
                        f'    </div>'
                    )
                    
                    print(f"{filename} wurde zu {new_name} umbenannt und skaliert.")
                    count += 1
            except Exception as e:
                print(f"Fehler beim Verarbeiten der Datei {filename}: {e}")
    
    # HTML-Datei schreiben
    try:
        with open(output_html_file, "w", encoding="utf-8") as html_file:
            html_content = (
                '<div class="slideshow-container">\n'
                '    <!-- Slides -->\n'
                + "\n".join(image_entries) +
                '\n</div>'
            )
            html_file.write(html_content)
            print(f"HTML-Datei wurde erfolgreich erstellt: {output_html_file}")
    except Exception as e:
        print(f"Fehler beim Erstellen der HTML-Datei: {e}")

# Beispielverwendung
directory_path = os.path.join(os.getcwd(),"img/verbessert")  # Verzeichnis anpassen
output_html = os.path.join(os.getcwd(),"slideshow.html")  # Speicherort für die HTML-Datei
rename_resize_generate_html(directory_path, output_html)