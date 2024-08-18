# ~ ~ ~ ~ ~ ~ ~ ~ LIBRERIAS ~ ~ ~ ~ ~ ~ ~ ~

import streamlit as st
import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import os
import json
import zipfile
import shutil
from Bio.PDB import MMCIFParser, PDBIO
from Bio.PDB import MMCIFParser, PDBIO, Select
from io import BytesIO

import py3Dmol


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ 

# * * * * * * * * FUNCIONES * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  

# FUNCION- FLOR -----------------------------------------------------------------------------------------------

# def load_af3_pdb(zip_file_path):  # Cambié el argumento para aceptar la ruta del archivo
#     Z = {}

#     # Obtener el nombre del archivo sin extensión para usarlo como nombre de la carpeta
#     name = os.path.basename(zip_file_path).replace('.zip', '')

#     folder = f'AF3_files/{name}'
#     results_folder = f'AF3_files/{name}'
#     os.makedirs(results_folder, exist_ok=True)

#     # Extraer el archivo ZIP
#     with zipfile.ZipFile(zip_file_path, 'r') as fz:
#         fz.extractall(folder)

#     pdb_file_path = None  # Inicializar la ruta del archivo PDB

#     # Procesar los archivos dentro de la carpeta extraída
#     for path in os.listdir(folder):
#         long_path = os.path.join(folder, path)

#         if long_path.endswith("_summary_confidences_0.json"):
#             with open(long_path, 'r') as file:
#                 data = json.load(file)
#                 ptmscore = float(data['ptm'])

#         if long_path.endswith("_model_0.cif"):
#             file_parser = MMCIFParser(QUIET=True)
#             structure = file_parser.get_structure("base", long_path)
#             io = PDBIO()
#             io.set_structure(structure)
#             io.save(f'{results_folder}/{name}_relaxed.pdb', select=Select())  # Asegurar que select esté configurado
#             pdb_file_path = f'{results_folder}/{name}_relaxed.pdb'
#             print(f"Archivo PDB guardado en: {pdb_file_path}")

#         if long_path.endswith("_full_data_0.json"):
#             with open(long_path, 'r') as file:
#                 data = json.load(file)
#                 distance = {"distance": data['pae']}
#             with open(f'{results_folder}/{name}_pae.json', 'w', encoding='utf-8') as f:
#                 json.dump(distance, f, ensure_ascii=False)

#     # Retornar la ruta del archivo PDB
#     return pdb_file_path

#--------------------------------------------------------------------------------------------------------------

def extract_data_from_zip(zip_file):
    
    pdb_content = None  # Para almacenar el contenido PDB
    ptmscore = None

    with zipfile.ZipFile(zip_file, 'r') as fz:
        fz.extractall('temp_folder')

    for path in os.listdir('temp_folder'):
        long_path = os.path.join('temp_folder', path)

        if long_path.endswith("_summary_confidences_0.json"):
            with open(long_path, 'r') as file:
                data = json.load(file)
                ptmscore = float(data['ptm'])

    for path in os.listdir('temp_folder'):
        long_path = os.path.join('temp_folder', path)

        if long_path.endswith("_model_0.cif"):
            file_parser = MMCIFParser(QUIET=True)
            structure = file_parser.get_structure("base", long_path)
            io = PDBIO()
            io.set_structure(structure)

            # Guardar el archivo PDB en un archivo temporal en disco
            pdb_temp_file = "temp_folder/temp.pdb"
            io.save(pdb_temp_file)  # Guardar en archivo temporal

            # Leer el contenido del archivo temporal en memoria
            with open(pdb_temp_file, 'r') as file:
                pdb_content = file.read()
            
    return pdb_content, ptmscore


# Función para visualizar el archivo PDB en 3D
def visualize_pdb_3d(pdb_content):
    view_3d = py3Dmol.view(width=800, height=500)
    view_3d.addModel(pdb_content, 'pdb')
    view_3d.setStyle({'model': 0}, {"cartoon": {'color': '0x51adbe'}})  # Modelo 0 con color azul
    view_3d.zoomTo()
    #view_3d.show()
    return view_3d



# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 


# Set Up de la applicación * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  
st.set_page_config(
    page_title="NOMBRE DE LA APP",
    page_icon="	:mag_right:",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        # #pestañas del menu que se pueden modificar, pero solo acepta estas 3
        # 'Get Help': "COMPLETAR MAIL",
        # 'Report a bug': "COMPLETAR - MAIL",
        # 'About': "COMPLETAR"
    }
)

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

st.write("Buen Día :)")





# Subida del archivo .zip
uploaded_file = st.file_uploader("Sube un archivo .zip de AlphaFold 3", type="zip")

if uploaded_file is not None:
    st.write("Procesando el archivo...")
    
    # Extraer ptmscore
    pdb_content, ptmscore = extract_data_from_zip(uploaded_file)
    st.write(ptmscore)
    # Generar y visualizar el archivo PDB
    
    if pdb_content:
        st.write("Visualizando la estructura 3D del modelo PDB:")
        view_3d = visualize_pdb_3d(pdb_content)
        st.components.v1.html(view_3d._make_html(), height=500, width=800)
    else:
        st.write("No se encontró un archivo _model_0.cif en el zip.")

