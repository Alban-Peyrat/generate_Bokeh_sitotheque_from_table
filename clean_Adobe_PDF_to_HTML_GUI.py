# -*- coding: utf-8 -*-

# External import
import os
import PySimpleGUI as sg
import json
from bs4 import BeautifulSoup

# Internal import
from theme.theme import *

# Load existing settings
with open('settings.json', "r+", encoding="utf-8") as f:
    settings = json.load(f)
    DEFAULT_OUTPUT_FOLDER = settings["DEFAULT_OUTPUT_FOLDER"]

# Get GUI parameters
sg.set_options(font=font, icon="theme/logo.ico", window_location=window_location)
sg.theme_add_new(theme_name, theme)
sg.theme(theme_name)

# # --------------- The Layout ---------------
layout = [
    [sg.Text("Le document que vous voulez nettoyez doit avoir été généré par Adobe Acrobat.")],

    # Original file path
    [sg.Text("Fichier à transformer :")],
    [sg.Input(key="FILE_PATH", size=(80, None)), sg.FileBrowse()],

    # Output folder
    [sg.Text("Dossier contenant l'article et autres fichiers :")],
    [sg.Input(key="OUTPUT_PATH", default_text=DEFAULT_OUTPUT_FOLDER,size=(80, None)), sg.FolderBrowse()],

    # Submit
    [sg.Button("Créer l'article", key="submit")]
]

# # --------------- Window Definition ---------------
# # Create the window
window = sg.Window("Transformer un document en article Bokeh", layout)

# # --------------- Event loop or Window.read call ---------------
# # Display and interact with the Window
# event, values = window.read()
event, val = window.read()
FILE_PATH = val["FILE_PATH"]
FILE_NAME = os.path.basename(FILE_PATH)
OUTPUT_PATH = val["OUTPUT_PATH"]

if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
    print("Application quittée par l'usager")
    exit()

# --------------- Cleaning part ---------------

# Leaves if the file format isn't supported
SUPPORTED_FILE_FORMATS = ["html"]
if FILE_PATH[FILE_PATH.rfind(".")+1:] not in SUPPORTED_FILE_FORMATS:
    print("Erreur : ce format n'est pas pris en charge")
    exit()

# Leaves if the file doesn't exists
if not os.path.exists(FILE_PATH):
    print("Erreur : le fichier n'existe pas")
    exit()

# Read the HTML file
with open(FILE_PATH, mode='r', encoding="utf-8") as f:
    # Create a BeautifulSoup object
    soup = BeautifulSoup(f, "html.parser")

# Find and remove the <head> element
head = soup.find('head')
head.decompose()

# Find all <p><br></p> elements and remove them
for elem in soup.find_all('p'):
    if elem.find_all('br'):
        elem.decompose()

# Find all elements and remove the 'style' and 'class' attributes
for element in soup.find_all():
    element.attrs = {}
    if element.name == 'style':
        element.decompose()

# Write the modified HTML to a new file
with open(OUTPUT_PATH+"/"+FILE_NAME, mode='w', encoding="utf-8") as f:
    f.write(str(soup))

print("Article nettoyé avec succès")

# # --------------- Closing the window ---------------
window.close()