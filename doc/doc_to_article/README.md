# Générer des articles pour Bokeh à partir de documents `.docx`

Utiliser [pandoc](https://pandoc.org/) via [pypandoc](https://pypi.org/project/pypandoc/) pour convertir les documenst words en html
Pour exporter les images, voir https://gist.github.com/jesperronn/ff5764274b3642bc7f2f#file-docx2md-sh

Avoir plusieurs paramétrages :
* avec/sans images ?
* dans le fichier, quel chemin pour les images ? (commence forcément par `usefiles/image/adm_doc_pro/` si c'est doc pro, sinon c'est le chemin vers la commission si c'est une commision, sinon vers l'école)
* pour ce point ↑↑↑↑↑, faire un choix avant : destination : documentation_professionnelle, commission (+ nom commission), ENSA (+ nom ensa) → faire une équivalence dans .json
Avoir une gui pour input le ficheir et pour choisir la destination finale ?
Créer un exe

Faut-il delete les informations de style des images par défaut ?


ex (docs sans les images): 
```Python
pypandoc.convert_file("C:\\Users\\alban.peyrat\\Downloads\\KohaArchires_Gestion des adherentsV3.docx", "html", outputfile="C:\\Users\\alban.peyrat\\Downloads\\el_test.html")
```