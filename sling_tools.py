# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 15:09:57 2023

@author: dsanm
"""

import streamlit as st
import requests
import json
import pandas as pd

at_token = st.secrets["at_token"]
base_id = st.secrets["at_base_id"]
table_name = 'DataCenter'
headers_AT = {"Authorization" : f"Bearer {at_token}",  "Content-Type" : 'application/json' }
endpoint_AT = f'https://api.airtable.com/v0/{base_id}/{table_name}'

url = "https://api.getsling.com/account/login"
data = {"email" : st.secrets["sl_email"], "password" : st.secrets["sl_psswrd"]}
headers = {"Content-Type" : "application/json", "accept" : "*/*"}

st.markdown( """<style>
    .block-container :nth-child(1) :nth-child(1) :nth-child(5) :nth-child(1) :nth-child(1) {
    background-color: #FA0E0E;
    }
    .stButton>button {
        background-color: #38F538;
        color: black;
        width: 133px;}
    .st-be.st-b3.st-bf.st-b8.st-bg.st-bh.st-bi.st-bj.st-bk.st-bl.st-bm.st-bn.st-bo.st-b1.st-bp.st-au.st-ax.st-av.st-aw.st-ae.st-af.st-ag.st-ah.st-ai.st-aj.st-bq.st-br.st-bs.st-bt.st-bu.st-bv.st-cy {
        border: 1px solid #FFA200;
        width: 133px;}
    .stDataFrame {background-color: #FAFCB3;
        border: 2px solid #FFA200;
        padding: 1% 1% 1% 1%;
        border-radius: 10px;}
    </style>""",unsafe_allow_html=True,)
pag = st.empty()
contrasena_correcta = st.secrets['contrasena_correcta']
pag.title("Aplicación Protegida con Contraseña")
contrasena = pag.text_input("Ingrese la contraseña:", type="password")
if contrasena == contrasena_correcta:
    pag.success("¡Contraseña correcta! Bienvenido a la aplicación.")
    pag.empty()
    
    st.title("SLING TOOLS :hammer_and_wrench:")
    st.divider()
    bot_1 = st.button("Generar Token ", key="button1")
    
    if bot_1:
        
        response = requests.post(url, json = data, headers = headers)
        authorization_header = response.headers.get("authorization", "")
        sl_token = authorization_header
        at_data ={'records' : [{"id": "recAIgXVtDBCO64rb",'fields':{'ids': sl_token }}]}
        req = requests.patch(endpoint_AT, json.dumps(at_data), headers = headers_AT)

    bot_2 = st.button('Pilotos')
    if bot_2:

        req = requests.get('https://api.airtable.com/v0/appFezarrh9fv6WrS/DataCenter/recAIgXVtDBCO64rb',  headers = headers_AT)
        tk_at = req.json()
        sl_token = tk_at['fields']['ids']
        lista = requests.get("https://api.getsling.com/v1/users",headers = {"Authorization" : sl_token,  "accept" : 'application/json' } )
        l_1 = lista.json()
        l_2 = json.loads(lista.text)
        lista_pilotos = []
        for j in l_1:
            if j['active'] == True:
                lista_pilotos.append([j['name'],j['lastname'],str(j['id'])])
                print(j['name'],j['lastname'],j['id'])
        pilots= pd.DataFrame(lista_pilotos)
        st.write(pilots)
        
    bot_3 = st.button('Positions')
    if bot_3:

        req = requests.get('https://api.airtable.com/v0/appFezarrh9fv6WrS/DataCenter/recAIgXVtDBCO64rb',  headers = headers_AT)
        tk_at = req.json()
        sl_token = tk_at['fields']['ids']
        lista = requests.get("https://api.getsling.com/v1/personas",headers = {"Authorization" : sl_token,  "accept" : 'application/json' } )
        l_1 = lista.json()
        l_2 = json.loads(lista.text)
        lista_position = []
        for j in l_1:
            if j['type'] == 'position':
                lista_position.append([j['name'],str(j['id'])])
        positions= pd.DataFrame(lista_position)
        st.write(positions)

    bot_4 = st.button('Locations')
    if bot_4:

        req = requests.get('https://api.airtable.com/v0/appFezarrh9fv6WrS/DataCenter/recAIgXVtDBCO64rb',  headers = headers_AT)
        tk_at = req.json()
        sl_token = tk_at['fields']['ids']
        lista = requests.get("https://api.getsling.com/v1/personas",headers = {"Authorization" : sl_token,  "accept" : 'application/json' } )
        l_1 = lista.json()
        l_2 = json.loads(lista.text)
        lista_location = []
        for j in l_1:
            if j['type'] == 'location':
                lista_location.append([j['name'],str(j['id'])]) 
        location= pd.DataFrame(lista_location)
        st.write(location)