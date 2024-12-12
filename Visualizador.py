import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt


# Cargar el archivo de Excel
uploaded_file = st.file_uploader("Sube tu archivo Excel", type=["xlsx"])

if uploaded_file is not None:
    # Leer los datos de la hoja de Excel
    df = pd.read_excel(uploaded_file)

    # Verificamos las primeras filas de los datos cargados
    st.write(df.head())

    # Contamos las ocurrencias de cada "Curso" para cada "Unidad Educativa"
    df_counts = df.groupby(['Unidad Educativa', 'Curso']).size().reset_index(name='Total')

    # Crear un gráfico de barras agrupadas con los totales sobre cada barra
    fig = px.bar(df_counts, 
                 x='Unidad Educativa', 
                 y='Total', 
                 color='Curso', 
                 barmode='group', 
                 title="Gráfico de Barras Agrupadas por Unidad Educativa y Curso",
                 text='Total')

    # Configurar el gráfico para que muestre los totales cuando el cursor se acerque
    fig.update_traces(texttemplate='%{text}', textposition='outside', hoverinfo='x+y+text')

    # Mostrar el gráfico
    st.plotly_chart(fig)

    #######

        # Contamos las ocurrencias de cada combinación "Edad" y "Sexo"
    df_counts = df.groupby(['Edad', 'Sexo']).size().reset_index(name='Total')

    # Crear un gráfico de barras agrupadas con los totales sobre cada barra
    fig = px.bar(df_counts, 
                 x='Edad', 
                 y='Total', 
                 color='Sexo', 
                 barmode='group', 
                 title="Gráfico de Barras Agrupadas por Edad y Sexo",
                 text='Total')

    # Configurar el gráfico para que muestre los totales cuando el cursor se acerque
    fig.update_traces(texttemplate='%{text}', textposition='outside', hoverinfo='x+y+text')

    # Mostrar el gráfico
    st.plotly_chart(fig)
    
    #####
    
    # Dividir las respuestas de la columna si hay varias opciones separadas por ", "
    # Usamos .explode() para crear un registro por cada opción
    df_exploded = df['¿Quién toma las decisiones sobre cómo gastar y ahorrar dinero en tu hogar?'].str.split(', ').explode().reset_index(drop=True)

    # Contamos las ocurrencias de cada opción
    counts = df_exploded.value_counts()

    # Calculamos los porcentajes
    total = counts.sum()
    percentages = (counts / total) * 100

    # Convertimos a DataFrame para facilidad de uso con Plotly
    result_df = pd.DataFrame({'Opción': counts.index, 'Frecuencia': counts.values, 'Porcentaje': percentages.values})

    # Crear un gráfico de torta con los porcentajes
    fig = px.pie(result_df, 
                 names='Opción', 
                 values='Porcentaje', 
                 title="Porcentaje de Respuestas sobre Quién Toma las Decisiones en el Hogar",
                 labels={'Opción': 'Quién toma las decisiones', 'Porcentaje': 'Porcentaje (%)'},
                 hole=0.3,  # Para hacer el gráfico de torta (agrega un agujero en el centro)
                 hover_data={'Porcentaje': True})

    # Mostrar el gráfico
    st.plotly_chart(fig) 
    
    ###
    
    # Contamos las ocurrencias de cada opción para la columna '¿Utilizas alguna aplicación móvil para manejar tu dinero o realizar transacciones financieras?'
    counts = df['¿Utilizas alguna aplicación móvil para manejar tu dinero o realizar transacciones financieras?'].value_counts()

    # Convertimos a DataFrame para facilidad de uso con Plotly
    result_df = pd.DataFrame({'Opción': counts.index, 'Frecuencia': counts.values})

    # Lista de colores personalizados para las barras
    colores = ['#0f00ff', '#00e8ff']  # Puedes agregar más colores si es necesario

    # Crear un gráfico de barras con los totales (frecuencias absolutas)
    fig = px.bar(result_df, 
                 x='Frecuencia', 
                 y='Opción', 
                 orientation='h',  # Barras horizontales
                 title="Frecuencia de Respuestas sobre el Uso de Aplicaciones Móviles para Manejar Dinero",
                 labels={'Opción': 'Respuesta', 'Frecuencia': 'Total'},
                 text='Frecuencia',  # Mostrar el total sobre las barras
                 color='Opción',  # Usamos la opción como criterio para color
                 color_discrete_sequence=colores)  # Asignamos los colores manualmente

    # Configurar el gráfico para que muestre los totales sobre las barras
    fig.update_traces(texttemplate='%{text}', textposition='inside', hoverinfo='x+y+text')

    # Mostrar el gráfico
    st.plotly_chart(fig)
    
    ##
    
    # Contamos las respuestas para "¿Tienes alguna meta financiera para el futuro?"
    counts = df['¿Tienes alguna meta financiera para el futuro?'].value_counts().reset_index()
    counts.columns = ['Respuesta', 'Frecuencia']

    # Crear un gráfico de barras
    fig = px.bar(counts, 
                 x='Respuesta',  # Respuestas en el eje X
                 y='Frecuencia', 
                 title="¿Tienes alguna meta financiera para el futuro?",
                 labels={'Respuesta': 'Respuesta', 
                         'Frecuencia': 'Frecuencia'},
                 text='Frecuencia')  # Mostrar el total sobre las barras

    # Configurar el gráfico para mostrar los totales sobre las barras
    fig.update_traces(texttemplate='%{text}', textposition='inside', hoverinfo='x+y+text')

    # Personalizar los colores
    # Diccionario con colores personalizados para cada respuesta
    color_map = {
        'Si': 'green',           
        'No': 'red'    
    }

    # Asignar los colores manualmente según la respuesta
    fig.update_traces(marker=dict(color=[color_map.get(respuesta, 'gray') for respuesta in counts['Respuesta']]))

    # Mostrar el gráfico
    st.plotly_chart(fig)
    
    #############
    
    # Crear las combinaciones de 'Sexo' y 'Unidad Educativa'
    df['Sexo - Unidad Educativa'] = df['Sexo'] + ' - ' + df['Unidad Educativa']
    
    # Seleccionar las columnas de las que queremos hacer el gráfico
    columnas = ['Estudios',
                'Salud',
                'Jubilación o vejez',
                'Vestimenta',
                'Inversiones',
                'Ocio']
    
    # Para cada área, generar un gráfico separado
    for area in columnas:
        # Agrupar los datos por 'Sexo - Unidad Educativa' y la columna del área de interés
        df_grouped = df[['Sexo - Unidad Educativa', area]].dropna()  # Eliminar valores NaN
        df_grouped = df_grouped.groupby(['Sexo - Unidad Educativa', area]).size().reset_index(name='Frecuencia')

        # Crear el gráfico de barras agrupadas por área
        fig = px.bar(df_grouped, 
                     x='Sexo - Unidad Educativa', 
                     y='Frecuencia', 
                     color=area, 
                     barmode='group', 
                     title=f"Importancia de Ahorrar en {area} según Sexo y Unidad Educativa",
                     labels={'Frecuencia': 'Frecuencia', 
                             'Sexo - Unidad Educativa': 'Combinación Sexo y Unidad Educativa', 
                             area: f'Nivel de Importancia'},
                     color_discrete_sequence=['blue', 'green', 'red', 'orange', 'purple', 'yellow'])  # Colores personalizados
        
        # Mostrar el gráfico
        st.plotly_chart(fig)
        
    #####
    
        # Agrupar los datos por 'Unidad Educativa' y la columna de educación financiera
    df_grouped = df[['Unidad Educativa', '¿Has recibido alguna educación financiera en tu colegio o en otro lugar?']].dropna()  # Eliminar valores NaN
    df_grouped = df_grouped.groupby(['Unidad Educativa', '¿Has recibido alguna educación financiera en tu colegio o en otro lugar?']).size().reset_index(name='Frecuencia')

    # Crear el gráfico de barras agrupadas por 'Unidad Educativa' y la respuesta sobre educación financiera
    fig = px.bar(df_grouped, 
                 x='Unidad Educativa', 
                 y='Frecuencia', 
                 color='¿Has recibido alguna educación financiera en tu colegio o en otro lugar?', 
                 barmode='group', 
                 title="Educación Financiera Recibida según Unidad Educativa",
                 labels={'Frecuencia': 'Frecuencia', 
                         'Unidad Educativa': 'Unidad Educativa', 
                         '¿Has recibido alguna educación financiera en tu colegio o en otro lugar?': 'Respuesta sobre Educación Financiera'},
                 color_discrete_sequence=['blue', 'green'])  # Colores personalizados para las respuestas

    # Mostrar el gráfico
    st.plotly_chart(fig)
    
    #####
    
        # Agrupar los datos por 'Sexo', 'Edad' y la columna de interés
    df_grouped = df[['Sexo', 'Edad', '¿Te gustaría aprender más sobre cómo manejar tu dinero y planificar tus finanzas?']].dropna()  # Eliminar valores NaN
    df_grouped = df_grouped.groupby(['Sexo', 'Edad', '¿Te gustaría aprender más sobre cómo manejar tu dinero y planificar tus finanzas?']).size().reset_index(name='Frecuencia')

    # Crear el gráfico de barras agrupadas por 'Sexo' y 'Edad'
    fig = px.bar(df_grouped, 
                 x='Edad', 
                 y='Frecuencia', 
                 color='Sexo', 
                 facet_col='¿Te gustaría aprender más sobre cómo manejar tu dinero y planificar tus finanzas?', 
                 barmode='group', 
                 title="Interés en Aprender sobre Manejo de Dinero y Planificación Financiera según Sexo y Edad",
                 labels={'Frecuencia': 'Frecuencia', 
                         'Edad': 'Edad', 
                         'Sexo': 'Sexo', 
                         '¿Te gustaría aprender más sobre cómo manejar tu dinero y planificar tus finanzas?': 'Respuesta sobre Educación Financiera'},
                 color_discrete_sequence=['blue', 'orange'])  # Colores personalizados para el sexo

    # Mostrar el gráfico
    st.plotly_chart(fig)
    
    #####
    
        # Separar las respuestas múltiples (si hay más de una opción separada por coma)
    df['¿Has oído hablar de los siguientes productos financieros?'] = df['¿Has oído hablar de los siguientes productos financieros?'].fillna('')

    # Separar las respuestas que están combinadas por coma y espacio
    products_list = df['¿Has oído hablar de los siguientes productos financieros?'].str.split(', ', expand=True)

    # Aplanar el DataFrame de las respuestas separadas en una lista
    all_products = products_list.stack().reset_index(drop=True)

    # Contar la frecuencia de cada opción
    product_counts = all_products.value_counts().reset_index(name='Frecuencia')
    product_counts.columns = ['Producto', 'Frecuencia']

    # Agrupar las respuestas por sexo
    df_sex = df[['Sexo', '¿Has oído hablar de los siguientes productos financieros?']].dropna()

    # Contar la frecuencia por sexo para cada producto financiero
    df_sex['¿Has oído hablar de los siguientes productos financieros?'] = df_sex['¿Has oído hablar de los siguientes productos financieros?'].str.split(', ')
    df_sex = df_sex.explode('¿Has oído hablar de los siguientes productos financieros?')

    # Agrupar por 'Sexo' y contar la frecuencia de productos financieros
    product_sex_counts = df_sex.groupby(['Sexo', '¿Has oído hablar de los siguientes productos financieros?']).size().reset_index(name='Frecuencia')
    
    # Crear el gráfico de barras
    fig = px.bar(product_sex_counts, 
                 x='Frecuencia', 
                 y='¿Has oído hablar de los siguientes productos financieros?', 
                 color='Sexo', 
                 orientation='h',
                 title="Conocimiento de Productos Financieros según Sexo",
                 labels={'Frecuencia': 'Frecuencia', 
                         'Sexo': 'Sexo', 
                         '¿Has oído hablar de los siguientes productos financieros?': 'Producto Financiero'},
                 color_discrete_sequence=['blue', 'orange'])

    # Mostrar el gráfico
    st.plotly_chart(fig)
    
    ####
    
    # Filtrar las columnas específicas
    columns_of_interest = [
        "¿Has utilizado alguna vez un cajero automático?", 
        "¿Has realizado alguna transacción financiera por Internet?", 
        "¿Has utilizado alguna vez códigos QR para realizar pagos o transferencias de dinero?", 
        "¿Te sientes seguro/a realizando transacciones financieras por Internet?"
    ]

    # Verificar si todas las columnas existen en los datos
    for column in columns_of_interest:
        if column not in df.columns:
            st.error(f"La columna '{column}' no se encuentra en el archivo.")
            break
    else:
        # Agrupar por las preguntas de interés
        df_filtered = df[columns_of_interest]

        # Reemplazar valores nulos o vacíos
        df_filtered = df_filtered.fillna('No responde')

        # Convertir las respuestas en categorías
        df_filtered = df_filtered.melt(var_name="Pregunta", value_name="Respuesta")
        
        # Agrupar por Pregunta y Respuesta para contar las frecuencias
        response_counts = df_filtered.groupby(["Pregunta", "Respuesta"]).size().reset_index(name="Frecuencia")

        # Definir una lista de colores personalizados
        color_palette = ['#7100ea', '#c200f7', '#f912c1']

        # Crear gráficos por separado para cada pregunta
        for pregunta in columns_of_interest:
            question_data = response_counts[response_counts["Pregunta"] == pregunta]
            
            # Asignar colores a las respuestas
            color_map = {respuesta: color_palette[i % len(color_palette)] for i, respuesta in enumerate(question_data["Respuesta"].unique())}
            fig = px.bar(question_data, 
                         x="Frecuencia", 
                         y="Respuesta", 
                         orientation="h",
                         title=f"Respuestas sobre {pregunta}",
                         labels={'Frecuencia': 'Frecuencia', 'Respuesta': 'Respuesta'},
                         color="Respuesta",
                         color_discrete_map=color_map)
            
            # Mostrar el gráfico
            st.plotly_chart(fig)
            
    #####
    
    # Filtrar la columna de interés
    columna = "¿Cuál de las siguientes afirmaciones describe mejor tu actitud hacia el dinero?"

    # Verificar si la columna existe en los datos
    if columna not in df.columns:
        st.error(f"La columna '{columna}' no se encuentra en el archivo.")
    else:
        # Reemplazar valores nulos o vacíos
        df[columna] = df[columna].fillna('No responde')

        # Separar las respuestas combinadas por ", " en una lista
        df_separado = df[columna].str.split(', ', expand=True)

        # Convertir las respuestas separadas en una sola columna larga
        df_separado = df_separado.melt(value_name="Respuesta", var_name="Var")

        # Filtrar las filas no vacías
        df_separado = df_separado[df_separado["Respuesta"].notna()]

        # Agrupar por sexo, unidad educativa y respuesta para contar las frecuencias
        df_separado['Sexo'] = df['Sexo']
        df_separado['Unidad Educativa'] = df['Unidad Educativa']

        response_counts = df_separado.groupby(["Sexo", "Unidad Educativa", "Respuesta"]).size().reset_index(name="Frecuencia")

        # Crear un gráfico de barras agrupado por sexo y unidad educativa
        fig = px.bar(response_counts, 
                     x="Respuesta", 
                     y="Frecuencia", 
                     color="Sexo",
                     facet_col="Unidad Educativa", 
                     title="Actitud hacia el dinero según sexo y unidad educativa",
                     labels={'Frecuencia': 'Frecuencia', 'Respuesta': 'Respuesta'},
                     barmode="group")

        # Mostrar el gráfico
        st.plotly_chart(fig)
    
    ####
    
    # Columna de interés
    columna = "¿Sueles llevar un registro de tus gastos?"

    # Verificar si la columna existe en los datos
    if columna not in df.columns:
        st.error(f"La columna '{columna}' no se encuentra en el archivo.")
    else:
        # Reemplazar valores nulos o vacíos
        df[columna] = df[columna].fillna('No responde')

        # Agrupar por sexo, unidad educativa y la respuesta para contar las frecuencias
        response_counts = df.groupby(["Sexo", "Unidad Educativa", columna]).size().reset_index(name="Frecuencia")

        # Crear una nueva columna para combinar Sexo y Unidad Educativa
        response_counts['Combinacion'] = response_counts['Sexo'] + ' - ' + response_counts['Unidad Educativa']

        # Definir los colores personalizados
        color_map = {
            'Femenino - Fe y alegría Compañía de Jesús': '#1aab00',
            'Masculino - Fe y alegría Compañía de Jesús': '#0bfd6a',
            'Femenino - La Salle de Convenio': '#03f8c4',
            'Masculino - La Salle de Convenio': '#f8f803'
        }

        # Crear el gráfico de barras con la combinación de Sexo y Unidad Educativa
        fig = px.bar(response_counts, 
                     x=columna, 
                     y="Frecuencia", 
                     color="Combinacion", 
                     title="¿Sueles llevar un registro de tus gastos?",
                     labels={'Frecuencia': 'Frecuencia', columna: 'Respuesta'},
                     barmode="group",
                     color_discrete_map=color_map)  # Aplicar el mapa de colores personalizado

        # Mostrar el gráfico
        st.plotly_chart(fig)
        
    ####
    
    # Columna de interés
    columna = "Antes de comprar algo, ¿Consideras si realmente lo necesitas y si puedes pagarlo?"

    # Verificar si la columna existe en los datos
    if columna not in df.columns:
        st.error(f"La columna '{columna}' no se encuentra en el archivo.")
    else:
        # Reemplazar valores nulos o vacíos
        df[columna] = df[columna].fillna('No responde')

        # Agrupar por sexo, unidad educativa y la respuesta para contar las frecuencias
        response_counts = df.groupby(["Sexo", "Unidad Educativa", columna]).size().reset_index(name="Frecuencia")

        # Crear una nueva columna para combinar Sexo y Unidad Educativa
        response_counts['Combinacion'] = response_counts['Sexo'] + ' - ' + response_counts['Unidad Educativa']

        color_map = {
            'Femenino - Fe y alegría Compañía de Jesús': '#0826fa', 
            'Masculino - Fe y alegría Compañía de Jesús': '#00e4ff',  
            'Femenino - La Salle de Convenio': '#56baff', 
            'Masculino - La Salle de Convenio': '#00ffd4'
        }

        # Crear el gráfico de barras con la combinación de Sexo y Unidad Educativa
        fig = px.bar(response_counts, 
                     x=columna, 
                     y="Frecuencia", 
                     color="Combinacion", 
                     title="Antes de comprar algo, ¿Consideras si realmente lo necesitas y si puedes pagarlo?",
                     labels={'Frecuencia': 'Frecuencia', columna: 'Respuesta'},
                     barmode="group",
                     color_discrete_map=color_map)  # Aplicar el mapa de colores personalizado

        # Mostrar el gráfico
        st.plotly_chart(fig)
        
    #####
    
        # Columna de interés
    columna = "¿Crees que es importante tener un fondo de emergencia para imprevistos?"

    # Verificar si la columna existe en los datos
    if columna not in df.columns:
        st.error(f"La columna '{columna}' no se encuentra en el archivo.")
    else:
        # Reemplazar valores nulos o vacíos
        df[columna] = df[columna].fillna('No responde')

        # Agrupar por Sexo, Unidad Educativa y la respuesta para contar las frecuencias
        response_counts = df.groupby(["Sexo", "Unidad Educativa", columna]).size().reset_index(name="Frecuencia")

        # Crear una nueva columna para combinar Sexo y Unidad Educativa
        response_counts['Combinacion'] = response_counts['Sexo'] + ' - ' + response_counts['Unidad Educativa']

        color_map = {
            'Femenino - Fe y alegría Compañía de Jesús': '#40069f', 
            'Masculino - Fe y alegría Compañía de Jesús': '#a406ff',  
            'Femenino - La Salle de Convenio': '#712ef7', 
            'Masculino - La Salle de Convenio': '#cd76ff'
        }

        # Crear el gráfico de barras
        fig = px.bar(response_counts,
                     x=columna,
                     y="Frecuencia",
                     color="Combinacion",
                     title="¿Crees que es importante tener un fondo de emergencia para imprevistos?",
                     color_discrete_map=color_map,
                     barmode="group",
                     labels={
                         columna: "Respuesta",
                         "Frecuencia": "Cantidad",
                         "Combinacion": "Sexo y Unidad Educativa"
                     })

        # Mostrar el gráfico
        st.plotly_chart(fig)
        
    #### 
    
        # Columna de interés
    columna = "¿Cómo calificarías tu conocimiento sobre temas financieros?"

    # Verificar si la columna existe en los datos
    if columna not in df.columns:
        st.error(f"La columna '{columna}' no se encuentra en el archivo.")
    else:
        # Reemplazar valores nulos o vacíos
        df[columna] = df[columna].fillna('No responde')

        # Agrupar por Sexo, Unidad Educativa y la respuesta para contar las frecuencias
        response_counts = df.groupby(["Sexo", "Unidad Educativa", columna]).size().reset_index(name="Frecuencia")

        # Crear una nueva columna para combinar Sexo y Unidad Educativa
        response_counts['Combinacion'] = response_counts['Sexo'] + ' - ' + response_counts['Unidad Educativa']

        color_map = {
            'Femenino - Fe y alegría Compañía de Jesús': '#ff9700', 
            'Masculino - Fe y alegría Compañía de Jesús': '#ffff01',  
            'Femenino - La Salle de Convenio': '#ffd101', 
            'Masculino - La Salle de Convenio': '#d9ff01'
        }

        # Crear el gráfico de barras
        fig = px.bar(response_counts,
                     x=columna,
                     y="Frecuencia",
                     color="Combinacion",
                     title="¿Cómo calificarías tu conocimiento sobre temas financieros?",
                     color_discrete_map=color_map,
                     barmode="group",
                     labels={
                         columna: "Respuesta",
                         "Frecuencia": "Cantidad",
                         "Combinacion": "Sexo y Unidad Educativa"
                     })

        # Mostrar el gráfico
        st.plotly_chart(fig)
        
    ###
    
        # Columna de interés
    columna = f"Si la inflación es del 3% anual, ¿qué significa esto?"

    # Verificar si la columna existe en los datos
    if columna not in df.columns:
        st.error(f"La columna '{columna}' no se encuentra en el archivo.")
    else:
        # Reemplazar valores nulos o vacíos
        df[columna] = df[columna].fillna('No responde')

        # Agrupar por Sexo, Unidad Educativa y la respuesta para contar las frecuencias
        response_counts = df.groupby(["Sexo", "Unidad Educativa", columna]).size().reset_index(name="Frecuencia")

        # Crear una nueva columna para combinar Sexo y Unidad Educativa
        response_counts['Combinacion'] = response_counts['Sexo'] + ' - ' + response_counts['Unidad Educativa']

        color_map = {
            'Femenino - Fe y alegría Compañía de Jesús': '#b40000', 
            'Masculino - Fe y alegría Compañía de Jesús': '#d1ae00',  
            'Femenino - La Salle de Convenio': '#b46800', 
            'Masculino - La Salle de Convenio': '#d4dc65'
        }

        # Crear el gráfico de barras
        fig = px.bar(response_counts,
                     x=columna,
                     y="Frecuencia",
                     color="Combinacion",
                     title="Significado de la inflación",
                     color_discrete_map=color_map,
                     barmode="group",
                     labels={
                         columna: "Respuesta",
                         "Frecuencia": "Cantidad",
                         "Combinacion": "Sexo y Unidad Educativa"
                     })

        # Mostrar el gráfico
        st.plotly_chart(fig)
    
    
    ####
    
        # Columna de interés
    columna = "¿Es verdad o Falso que es más seguro guardar tu dinero en diferentes lugares en vez de solo uno?"

    # Verificar si la columna existe en los datos
    if columna not in df.columns:
        st.error(f"La columna '{columna}' no se encuentra en el archivo.")
    else:
        # Reemplazar valores nulos o vacíos
        df[columna] = df[columna].fillna('No responde')

        # Agrupar por Sexo, Unidad Educativa y la respuesta para contar las frecuencias
        response_counts = df.groupby(["Sexo", "Unidad Educativa", columna]).size().reset_index(name="Frecuencia")

        # Crear una nueva columna para combinar Sexo y Unidad Educativa
        response_counts['Combinacion'] = response_counts['Sexo'] + ' - ' + response_counts['Unidad Educativa']

        color_map = {
            'Femenino - Fe y alegría Compañía de Jesús': '#c10064', 
            'Masculino - Fe y alegría Compañía de Jesús': '#0206fa',  
            'Femenino - La Salle de Convenio': '#6300c1', 
            'Masculino - La Salle de Convenio': '#02ebfa'
        }

        # Crear el gráfico de barras
        fig = px.bar(response_counts,
                     x=columna,
                     y="Frecuencia",
                     color="Combinacion",
                     title="Seguridad al guardar dinero",
                     color_discrete_map=color_map,
                     barmode="group",
                     labels={
                         columna: "Respuesta",
                         "Frecuencia": "Cantidad",
                         "Combinacion": "Sexo y Unidad Educativa"
                     })

        # Mostrar el gráfico
        st.plotly_chart(fig)