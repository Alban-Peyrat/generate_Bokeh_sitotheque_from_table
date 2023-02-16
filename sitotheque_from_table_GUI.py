# -*- coding: utf-8 -*-

# External import
import os
import PySimpleGUI as sg
import json

# Internal import
from theme.theme import *
import sitotheque_from_table as sft

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
    # Original file path
    [sg.Text("Fichier à transformer :")],
    [sg.Input(key="FILE_PATH", size=(80, None)), sg.FileBrowse()],

    # Output folder
    [sg.Text("Dossier contenant le fichier de sortie :")],
    [sg.Input(key="OUTPUT_PATH", default_text=DEFAULT_OUTPUT_FOLDER,size=(80, None)), sg.FolderBrowse()],

    # Submit
    [sg.Button("Créer l'article", key="submit")]
]

# # --------------- Window Definition ---------------
# # Create the window
window = sg.Window("Générer une sitothèque pour Bokeh à partir d'un tableur", layout)

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

# Leaves if the file format isn't supported
SUPPORTED_FILE_FORMATS = ["xls", "xlsx", "ods", "csv", "tsv", "txt"]
FILE_FORMAT = FILE_PATH[FILE_PATH.rfind(".")+1:]
if FILE_FORMAT not in SUPPORTED_FILE_FORMATS:
    print("Erreur : ce format n'est pas pris en charge")
    exit()

# Leaves if the file doesn't exists
if not os.path.exists(FILE_PATH):
    print("Erreur : le fichier n'existe pas")
    exit()

# Creates the file
sft.main(FILE_PATH, FILE_NAME, FILE_FORMAT, OUTPUT_PATH)

print("Article créé avec succès")

# # --------------- Closing the window ---------------
window.close()