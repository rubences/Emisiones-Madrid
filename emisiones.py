"""Módulo que contiene funciones para analizar la base de datos de emisiones de gases contaminantes del Ayuntamiento de Madrid.
https://datos.madrid.es/portal/site/egob/menuitem.c05c1f754a33a9fbe4b2e4b284f1a5a0/?vgnextoid=aecb88a7e2b73410VgnVCM2000000c205a0aRCRD&vgnextchannel=374512b9ace9f310VgnVCM100000171f5a0aRCRD&vgnextfmt=default
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt

# Códigos de las magnitudes contaminantes medidas
magnitudes = {
    '01':'Dióxido de Azufre',
    '06':'Monóxido de Carbono',
    '07':'Monóxido de Nitrógeno',
    '08':'Dióxido de Nitrógeno',
    '09':'Partículas < 2.5 μm',
    '10':'Partículas < 10 μm',
    '12':'Óxidos de Nitrógeno',
    '14':'Ozono',
    '20':'Tolueno',
    '30':'Benceno',
    '35':'Etilbenceno',
    '37':'Metaxileno',
    '38':'Paraxileno',
    '39':'Ortoxileno',
    '42':'Hidrocarburos totales(hexano)',
    '43':'Metano',
    '44':'Hidrocarburosno metánicos (hexano)'
}

# Códigos de las estaciones de medición.
estaciones = {
    '001':'Pº. Recoletos',
    '002':'Glta. de Carlos V',
    '035':'Pza. del Carmen',
    '004':'Pza. de España',
    '039':'Barrio del Pilar',
    '006':'Pza. Dr. Marañón',
    '007':'Pza. M. de Salamanca',
    '008':'Escuelas Aguirre',
    '009':'Pza. Luca de Tena',
    '038':'Cuatro Caminos',
    '011':'Av. Ramón y Cajal',
    '012':'Pza. Manuel Becerra',
    '040':'Vallecas',
    '014':'Pza. Fdez. Ladreda',
    '015':'Pza. Castilla',
    '016':'Arturo Soria', 
    '017':'Villaverde Alto',
    '018':'Calle Farolillo',
    '019':'Huerta Castañeda',
    '036':'Moratalaz',
    '021':'Pza. Cristo Rey',
    '022':'Pº. Pontones',
    '023':'Final C/ Alcalá',
    '024':'Casa de Campo',
    '025':'Santa Eugenia',
    '026':'Urb. Embajada (Barajas)',
    '027':'Barajas',
    '047':'Méndez Álvaro',
    '048':'Pº. Castellana',
    '049':'Retiro',
    '050':'Pza. Castilla',
    '054':'Ensanche Vallecas',
    '055':'Urb. Embajada (Barajas)',
    '056':'Plaza Elíptica',
    '057':'Sanchinarro',
    '058':'El Pardo',
    '059':'Parque Juan Carlos I',
    '060':'Tres Olivos'
}

def estacion_magnitud(df, estacion, magnitud):
    """
    Función que devuelve la lista de valores de una estación y magnitud.
    Parámetros: 
        - df: Es un DataFrame con la información de la base de datos de emisiones.
        - estacion: Es una cadena con el código de la estación de medición.
        - magnitud: Es una cadena el código de la magnitud medida.
    Devuelve:
        Una lista con los valores de la magnitud medidos en la estación indicada.
    """
    # Filtro de la estación y la magnitud
    df1 = df[(df['ESTACION'] == estacion) & (df['MAGNITUD'] == magnitud)]
    return list(df1['VALOR'])

def medias_mes_estacion(df, mes, estacion):
    """
    Función que devuelve la media de las magnitudes medidas en una estación en un mes concreto.
    Parámetros:
        - df: Es un DataFrame con la información de la base de datos de emisiones.
        - mes: Es una cadena de dos caractares con el número de mes en formato mm.
        - estacion: Es una cadena con el código de la estación de medición.
    Devuelve:
        Un diccionario cuyos pares tienen como clave las magnitudes y como valores las medias del mes en la estación indicada.
    """ 
    # Filtro de la estación y el mes
    df1 = df[(df['ESTACION'] == estacion) & (df['MES'] == mes)]
    # Agrupación por magnitud y cálculo de la media
    return {magnitudes[k]:np.mean(v) for k, v in df1.groupby('MAGNITUD')['VALOR']}

def medias_mes_magnitud(df, mes, magnitud):
    """
    Función que devuelve la media de una magnitud en mes concreto en cada estación de medición.
    Parámetros:
        - df: Es un DataFrame con la información de la base de datos de emisiones.
        - mes: Es una cadena de dos caractares con el número de mes en formato mm.
        - magnitud: Es una cadena con el código de la magnitud medida.
    Devuelve:
        Un diccionario cuyos pares tienen como clave las estaciones y como valores las medias del mes de la magnitud indicada.
    """ 
    # Filtro de la magnitud y el mes
    df1 = df[(df['MAGNITUD'] == magnitud) & (df['MES'] == mes)]
    # Agrupación por estación y cálculo de la media
    return {estaciones[k]:np.mean(v) for k, v in df1.groupby('ESTACION')['VALOR']}

def evolucion_estacion(df, estacion, inicio, fin):
    """
    Función que crea un gráfico con la evolución de las magnitudes de una estación de medición en un rango de fechas.
    Parámetros:
        - df: Es un DataFrame con la información de la base de datos de emisiones.
        - estacion: Es una cadena con el código de la estacion de medición.
        - inicio: Es una cadena con la fecha inicial en formato dd-mm-aaaa.
        - fin: Es una cadena con la fecha final en formato dd-mm-aaaa.
    """
    # Añadir columna con el nombre de las magnitudes
    df['NOMBRE MAGNITUD'] = df['MAGNITUD'].apply(lambda x: magnitudes[x])
    # Filtro de la estación y rango de fechas
    df1 = df[(df['ESTACION'] == estacion) & (df['FECHA'] >= inicio) & (df['FECHA'] <= fin)]
    # Establecemos la columna fecha como índice del DataFrame
    df1.set_index('FECHA', inplace = True)
    # Inicializamos el gráfico
    fig, ax = plt.subplots()
    # Agrupamos los datos por magnitud y generamos el gráfico de líneas
    df1.groupby('NOMBRE MAGNITUD')['VALOR'].plot(legend = True)
    # Reducimos el eje x un 30% para que quepa la leyenda
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.7, box.height])
    # Dibujar la leyenda fuera del área del gráfico
    plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
    # Guardamos el gráfico.
    plt.savefig('img/' + estacion + '-' + inicio + ':' + fin + '.png')
    return

def evolucion_magnitud(df, magnitud, inicio, fin):
    """
    Función que crea un gráfico con la evolución de las mediciones de una magnitud en cada estación en un rango de fechas.
    Parámetros:
        - df: Es un DataFrame con la información de la base de datos de emisiones.
        - magnitud: Es una cadena con el código de la magnitud medida.
        - inicio: Es una cadena con la fecha inicial en formato dd-mm-aaaa.
        - fin: Es una cadena con la fecha final en formato dd-mm-aaaa.
    """
    # Añadir columna con el nombre de las estaciones
    df['NOMBRE ESTACION'] = df['ESTACION'].apply(lambda x: estaciones[x])
    # Filtro de la magnitud y el rango de fechas
    df1 = df[(df['MAGNITUD'] == magnitud) & (df['FECHA'] >= inicio) & (df['FECHA'] <= fin)]
    # Establecemos la columna fecha como índice del DataFrame
    df1.set_index('FECHA', inplace = True)
    # Inicializamos el gráfico
    fig, ax = plt.subplots()
    # Agrupamos los datos por estación y generamos el gráfico de líneas.
    df1.groupby('NOMBRE ESTACION')['VALOR'].plot(legend = True)
    # Reducimos el eje x un 30% para que quepa la leyenda
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.7, box.height])
    # Dibujar la leyenda fuera del área del gráfico
    plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
    # Guardamos el gráfico
    plt.savefig('img/' + magnitud + '-' + inicio + ':' + fin + '.png')
    return

def evolucion_medias_magnitud(df, magnitud):
    """
    Función que crea un gráfico con la evolución de las medias de una magnitud en cada estación.
    Parámetros:
        - df: Es un DataFrame con la información de la base de datos de emisiones.
        - magnitud: Es una cadena con el código de la magnitud medida.
    """
    # Añadir columna con el nombre de las estaciones
    df['NOMBRE ESTACION'] = df['ESTACION'].apply(lambda x: estaciones[x])
    # Filtro de la magnitud
    df1 = df[df['MAGNITUD'] == magnitud]
    # Establecemos la columna fecha como índice del DataFrame
    df1.set_index('FECHA', inplace = True)
    # Inicializamos el gráfico
    fig, ax = plt.subplots()
    # Agrupamos los datos por estación y generamos el gráfico de líneas.
    df1.groupby(['ANO','MES','NOMBRE ESTACION']).mean().unstack()['VALOR'].plot(ax = ax, legend = True)
    # Reducimos el eje x un 30% para que quepa la leyenda
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.7, box.height])
    # Dibujar la leyenda fuera del área del gráfico
    plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
    # Guardamos el gráfico
    plt.savefig('img/' + magnitudes[magnitud] + '.png')
    return
