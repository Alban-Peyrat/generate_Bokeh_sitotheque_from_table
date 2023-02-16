# -*- coding: utf-8 -*-

# External import
import pandas as pd
from bs4 import BeautifulSoup
import re

# Internal import

def main(INPUT_FILE, FILE_NAME, FILE_FORMAT, OUTPUT_PATH):
    """Generates the HTML file.
    
    Takes as argument :
        - INPUT_FILE : absolute path to the file to transform
        - FILE_NAME : only the name of the file (with file format)
        - FILE_FORMAT : the efile format
        - OUTPUT_PATH : the directory for the created HTML file"""
    
    # Open the file
    df = None
    if FILE_FORMAT in ["xlsx", "xls", "ods"]:
        df = pd.read_excel(INPUT_FILE)
    elif FILE_FORMAT == "csv":
        df = pd.read_csv(INPUT_FILE, sep=";")
    elif FILE_FORMAT in ["tsv", "txt"]:
        df = pd.read_csv(INPUT_FILE, sep="\t")
    else:
        print("Incorrect file format")
        exit()

    # Create BS object
    html = BeautifulSoup(features="html.parser")

    # Creates the containers
    div_toc = html.new_tag("div", id="div_toc")
    div_toc.append(new_header(html, "Sommaire", lvl=1))
    ul_toc = html.new_tag("ul")
    div_links = html.new_tag("div", id="div_links")

    # For each category
    categories = df["Category"].fillna("").unique()
    categories.sort()
    for ii, cat in enumerate(categories):
        cat_str = str(cat).strip()

        # Defines the sub-dataset
        df_cat =  df[df["Category"].fillna("") == cat]
                        
        # Generates the header in the link div
        cat_id = generate_header_id(generate_id_key(ii), cat_str)
        div_links.append(new_header(html, cat_str, lvl=1, id=cat_id))

        # Generates the entry in the table of contents
        cat_li = new_toc_entry(html, cat_str, cat_id)
        cat_ul = html.new_tag("ul")
        
        # pour les subcat, il faut générer un ul dans le li de la catégorie

        # For each sub-category
        sub_categories = df_cat["Sub-category"].fillna("").unique()
        sub_categories.sort()
        for jj, subcat in enumerate(sub_categories):
            subcat_str = str(subcat).strip()

            # Defines the sub-dataset
            df_subcat = df[(df["Category"].fillna("") == cat) & (df["Sub-category"].fillna("") == subcat)]

            # If the subcat isn't an empty string, generate a header & TOC entry
            if subcat_str != "":
                # Generates the header in the link div
                subcat_id = generate_header_id(generate_id_key(ii, jj), subcat_str)
                div_links.append(new_header(html, subcat_str, lvl=2, id=subcat_id))

                # Generates the entry in the table of contents
                cat_ul.append(new_toc_entry(html, subcat_str, subcat_id))

            # Generates the list
            link_ul = html.new_tag("ul")

            # For each row with this cat & subcat
            for index, row in df_subcat.iterrows():
                link_ul.append(new_link_entry(html, str(row["Name"]).strip(), str(row["URL"]).strip(), str(row["Description"]).strip()))

            # Appends the ul to the link container
            div_links.append(link_ul)

        # After each sub-category, append cat ul and li to TOC
        cat_li.append(cat_ul)
        ul_toc.append(cat_li)
    
    # Append the containers to the HTML
    div_toc.append(ul_toc)
    html.append(div_toc)
    html.append(div_links)

    # Creates the output file
    with open(OUTPUT_PATH+"/"+FILE_NAME[:FILE_NAME.rfind(".")]+".html", "w", encoding="utf-8") as f:
        f.write(str(html))

def new_header(html, txt, lvl=1, id=""):
    """Generates a header.
    
    Returns the created tag

    Takes as argument :
        - html : BS object
        - txt {str} : text content of the header
        - lvl {int} : which level of title"""
    head = html.new_tag("h" + str(lvl))
    head.string = txt
    if id != "":
        head["id"] = id
    return head

def new_link(html, txt, link, external=True, title_generic_text="Accéder à", title_destination_name=""):
    """Generates an external link
    
    Takes as argument :
        - html : BS object
        - txt {str} : text content of the link
        - link {str} : destination of the link
        - external {bool} : is the link external ?
        - title_generic_text {str} : the start of the link title
        - title_destination_name {str} : the name of the ressource to be displayed in the title"""

    # If title_destination_name is blank, takes txt as its value
    if title_destination_name == "":
        title_destination_name = txt
    
    a = html.new_tag("a", href=link)
    a["title"] = " ".join([str(title_generic_text), str(title_destination_name)])
    a.string = txt
    if external:
        a["target"] = "_blank"
    else:
        a["href"] = "#" + str(a["href"])
    return a

def new_link_entry(html, name, link, desc):
    """Generates a new entry in the links : returns the li element.
    
    Takes as argument :
        - html : BS object
        - name {str} : name of the ressource
        - link {str} : destination of the link
        - desc {str} : the discription of the ressource"""

    li = html.new_tag("li")
    a = new_link(html, name, link, external=True, title_generic_text="Accéder à", title_destination_name=name)
    li.append(a)
    li.append(" : " + str(desc))
    return li

def new_toc_entry(html, name, id):
    """Generates a link for the table of contents : returns the li element
    
    Takes as argument :
        - html : BS object
        - name {str} : name of the element
        - id {str} : id of the element"""
    
    li = html.new_tag("li")
    a = new_link(html, name, id, external=False, title_generic_text="Accéder à la catégorie", title_destination_name=name)
    li.append(a)
    return li

def generate_header_id(id_key, name):
    """Returns the key to use as an ID

    Takes as argument :
        - id_key {str} : index of the header in the list
        - name {str} : name of the ressource"""
    
    name = str(name).strip().lower() # Remove leading and endign spaces + set to lower case
    name = re.sub(r'[^\x00-\x7F]+', '', name) # Remove non-ASCII char
    name = re.sub(r'\s', "-", name) # Replace spaces by dashes
    return "{}-{}".format(str(id_key), str(name))

def generate_id_key(cat_idx, subcat_idx=-1):
    """Returns the ID Key to use in ids : the category index as a string if no sub-category is provided.
    Else, : "{index of category}--{index of sub-catagory}"
    
    Takes as argument :
        - cat_idx {int} : the index of the category
        - subcat_idx {int} [optional] : the index of the sub-category"""
    if subcat_idx == -1:
        return str(cat_idx)
    else:
        return "{}--{}".format(str(cat_idx), str(subcat_idx))