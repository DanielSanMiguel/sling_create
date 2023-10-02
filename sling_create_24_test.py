import streamlit as st
import pandas as pd
from airtable import Airtable
import requests
import json
import datetime
import time


token_github = st.secrets['github_token']
headers_1 = {"Authorization": f"token {token_github}"}
url_archivo_github = "https://raw.githubusercontent.com/DanielSanMiguel/fly-fut_app/main/style.css"
response = requests.get(url_archivo_github, headers=headers_1)
contenido_css = response.text
with open('style.css', 'w') as stl:
    st.markdown(f'<style>{contenido_css}<style>', unsafe_allow_html=True)
    st.markdown( """<style>
                .stButton>button {
                    background-color: #38F538;
                    color: black;}
                .stDataFrame {background-color: #FAFCB3;
                              border: 2px solid #FFA200;
                              padding: 1% 1% 1% 1%;
                              border-radius: 10px;
                              }
                </style>""",unsafe_allow_html=True,)
    pag = st.empty()
    contrasena_correcta = st.secrets['contrasena_correcta']
    pag.title("Aplicación Protegida con Contraseña")
    contrasena = pag.text_input("Ingrese la contraseña:", type="password")
    if contrasena == contrasena_correcta:
        pag.success("¡Contraseña correcta! Bienvenido a la aplicación.")
        pag.empty()
        with pag.container():
            # Aquí puedes agregar el contenido de tu aplicación
            inicio = time.time()
        
            api_key = st.secrets['at_token']
            base_id = 'appFezarrh9fv6WrS'
            table_name = 'M_I_Dani_23'
            table_name_DataCenter = 'DataCenter'
        
            def convert_to_dataframe(airtable_records):
                """Converts dictionary output from airtable_download() into a Pandas dataframe."""
                airtable_rows = []
                airtable_index = []
                for record in airtable_records['records']:
                    airtable_rows.append(record['fields'])
                    airtable_index.append(record['id'])
                airtable_dataframe = pd.DataFrame(airtable_rows, index=airtable_index)
                return airtable_dataframe
            today = datetime.datetime.today()
            hoy = today.date()
            t_1 = datetime.timedelta(days=56)
            t_2 = today + t_1
            t_fin = t_2.date()
            # creamos conexion con una tabla de airtable
            at_Table1 = Airtable(base_id, api_key)
            at_dc = Airtable(base_id,  api_key)
            # recuperamos datos de la tabla
            result_at_Table1 = at_Table1.get(table_name, fields=['ID-partido',
                                                                 'Piloto',
                                                                 'Fecha_UTC',
                                                                 'Sede',
                                                                 'Telf_Coord',
                                                                 'Status partido',
                                                                 'ARCID'])
            result_at_Table2 = at_dc.get(table_name_DataCenter,view = 'Grid view')
            # convertimos a DataFrame de Pandas
            airtable_dataframe = convert_to_dataframe(result_at_Table1)
            atdf = airtable_dataframe.reset_index(drop= True)
            dc_drame = convert_to_dataframe(result_at_Table2)
            dc = dc_drame.reset_index(drop=True)
        
            sling_token_list = [tok for n_t,tok in enumerate(dc['ids']) if dc.loc[n_t,'Name'] == 'sling_token']
            sling_token = sling_token_list[0]
            ids_sling = {si:dc.loc[ne,'ids']  for ne, si in enumerate(dc['Name']) if (dc.loc[ne,'type'] == 'piloto id')}
            equipos = {eq:dc.loc[ne,'ids']  for ne, eq in enumerate(dc['Name']) if (dc.loc[ne,'type'] == 'position id')}
            ids_location = {l:dc.loc[ne,'ids']  for ne, l in enumerate(dc['Name']) if (dc.loc[ne,'type'] == 'location id')}
            try:
                atdf['publi_sling'] = [x if x == True else (False) for x in atdf['publi_sling']]    
            except:
                atdf['publi_sling']=False
        
            headers_AT = {"Authorization" : f"Bearer {api_key}",  "Content-Type" : 'application/json' }
            headers_2 = {"Authorization" : sling_token,  "content-type" : 'application/json'}
            endpoint = 'https://api.getsling.com/v1/shifts'
            endpoint2 = 'https://api.getsling.com/v1/shifts/'
            endpoint3 = f'https://api.getsling.com/v1/calendar/167205/users/3835659?dates={hoy}%2F{t_fin}'
            endpoint_AT = f'https://api.airtable.com/v0/{base_id}/{table_name}'
        
            def fin_part(hora_inicio, hours, minutes):
                '''Define la hora de fin segun la hora de inicio y horas y minutos desde sling_data'''
                fecha = datetime.datetime.strptime(hora_inicio, "%Y-%m-%dT%H:%M:%S.%fZ")
                hora_fin = fecha + datetime.timedelta(hours=int(hours), minutes=int(minutes))
                hora_fin_total = hora_fin.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                return hora_fin_total
            st.subheader('Sling Shift Creator')
            st.write('Base de datos de Airtable')
            st.dataframe(atdf.style.set_properties(**{'background-color': '#EFFCD8'}))
            st.write('Crear partidos y modificar partidos existentes')
    
            b_1 = st.button('Ejecutar')
            if b_1:
                for i in range(len(atdf)):
                    if atdf.loc[i,'publi_sling'] == False:
                        if equipos[atdf.loc[i,'ID-partido'][12:-2]] == '15139774':
                            hours, minutes = [w for x,w in enumerate(dc['hora']) if dc.loc[x,'Name']== '15139774'], [w for x,w in enumerate(dc['minuto']) if dc.loc[x,'Name']== '15139774']
                        elif equipos[atdf.loc[i,'ID-partido'][12:-2]] == '15349440':
                            hours, minutes = [w for x,w in enumerate(dc['hora']) if dc.loc[x,'Name']== '15349440'], [w for x,w in enumerate(dc['minuto']) if dc.loc[x,'Name']== '15349440']
                        elif equipos[atdf.loc[i,'ID-partido'][12:-2]] == '6451139':
                            hours, minutes = [w for x,w in enumerate(dc['hora']) if dc.loc[x,'Name']== '6451139'], [w for x,w in enumerate(dc['minuto']) if dc.loc[x,'Name']== '6451139']
                            
                        data = {"user": {"id": ids_sling[atdf.loc[i,'Piloto']]},
                            "summary": atdf.loc[i,'ID-partido'],
                            "location": {"id": ids_location[atdf.loc[i,'Sede']]},
                            "position": {"id": equipos[atdf.loc[i,'ID-partido'][12:-2]]},
                            "dtend": fin_part(atdf.loc[i,'Fecha_partido'],hours[0], minutes[0]),
                            "dtstart": atdf.loc[i,'Fecha_partido'],
                            "status": "planning"}
                        req = requests.post(endpoint, json.dumps(data), headers = headers_2)
                        summary = data['summary']
                        print(f'creado {summary}')
                        data_AT = {'records' : [{"id": atdf.loc[i,'Rec2'],'fields':{'publi_sling': True }}]}
                        req_AT = requests.patch(endpoint_AT, json.dumps(data_AT), headers = headers_AT)
                
                
                calendar = requests.get(endpoint3, headers = headers_2).json()
                calend_pd_rows = []
                try:
                    for y,z in enumerate(calendar):
                        for u in range(len(atdf)):
                            if equipos[atdf.loc[u,'ID-partido'][12:-2]] == '15139774':
                                hours, minutes = [w for x,w in enumerate(dc['hora']) if dc.loc[x,'Name']== '15139774'], [w for x,w in enumerate(dc['minuto']) if dc.loc[x,'Name']== '15139774']
                            elif equipos[atdf.loc[u,'ID-partido'][12:-2]] == '15349440':
                                hours, minutes = [w for x,w in enumerate(dc['hora']) if dc.loc[x,'Name']== '15349440'], [w for x,w in enumerate(dc['minuto']) if dc.loc[x,'Name']== '15349440']
                            elif equipos[atdf.loc[u,'ID-partido'][12:-2]] == '6451139':
                                hours, minutes = [w for x,w in enumerate(dc['hora']) if dc.loc[x,'Name']== '6451139'], [w for x,w in enumerate(dc['minuto']) if dc.loc[x,'Name']== '6451139']
                            if datetime.datetime.strptime(z["dtstart"],'%Y-%m-%dT%H:%M:%S%z') != datetime.datetime.strptime(atdf.loc[u,'Fecha_partido'],'%Y-%m-%dT%H:%M:%S.%f%z') and z["summary"]==atdf.loc[u,'ID-partido']:
                                print(y,z["dtstart"],z["id"])
                                id_new = z["id"]
                                endpoint2 = f'https://api.getsling.com/v1/shifts/{id_new}'
                                data = {"user": {"id": z["user"]['id']}, "summary": z['summary'], "position": z["position"], "location": z["location"], "dtend": fin_part(atdf.loc[u,'Fecha_partido'],hours[0], minutes[0]), "dtstart": atdf.loc[u,'Fecha_partido'], "status": "planning"}
                                req = requests.put(endpoint2, json.dumps(data), headers = headers_2)
                                req.json()
                except:
                    print('SIN SHIFTS')
                
                fin = time.time()
                total=int(fin-inicio)
                print(f'Procesado en {total} segundos')
    else:
        st.error("Contraseña incorrecta. Por favor, intente de nuevo.")
