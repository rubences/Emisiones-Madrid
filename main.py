# Programa de análisis de las emisiones en Madrid
from emisiones import *

# Preprocesado de datos
# Carga de datos
ruta = 'datos/datos-emisiones.csv'
df = pd.read_csv(ruta)
# Preprocesamiento de datos
# Pasar los días de columnas a una nueva variable DIA
df = df.melt(
    id_vars=['ESTACION', 'MAGNITUD', 'ANO', 'MES'],
    var_name='DIA',
    value_name='VALOR')
# Eliminar la D del valor de los días
df['DIA'] = df['DIA'].apply(lambda x: x[1:])
# Convertir las columnas DIA, MES, ANO, ESTACION y MAGNITUD en cadenas
df['ESTACION'] = df['ESTACION'].astype(str)
df['MAGNITUD'] = df['MAGNITUD'].astype(str)
df['MES'] = df['MES'].astype(str)
df['ANO'] = df['ANO'].astype(str)
# Añadir 00 a la estación cuando la estación solo tiene un dígito y 0 cuando tiene dos
df['ESTACION'] = df['ESTACION'].apply(
    lambda x: '00' + x if len(x) < 2 else '0' + x)
# Añadir 0 a la magnitud cuando solo tiene un dígito
df['MAGNITUD'] = df['MAGNITUD'].apply(lambda x: '0' + x if len(x) < 2 else x)
# Añadir 0 al mes cuando el mes solo tiene un dígito
df['MES'] = df['MES'].apply(lambda x: '0' + x if len(x) < 2 else x)
# Crear una nueva columna concatenando las columnas DIA, MES y AÑO en formato dd/mm/aaaa
df['FECHA'] = df['DIA'] + '/' + df['MES'] + '/' + df['ANO']
# Convertir la columna fecha al tipo datetime
df['FECHA'] = pd.to_datetime(df['FECHA'], format='%d/%m/%Y', errors='coerce')
# Eliminar las filas con fechas no válidas
df = df.drop(df[np.isnat(df['FECHA'])].index)
# Ordenar el dataframe por fechas, magnitudes y estaciones
df = df.sort_values(['FECHA', 'MAGNITUD', 'ESTACION'])

print(df)

print(estacion_magnitud(df, '050', '12'))
print(medias_mes_estacion(df, '03', '050'))
print(medias_mes_magnitud(df, '12', '12'))
evolucion_estacion(df, '017', '2018-03-01', '2018-06-30')
evolucion_magnitud(df, '12', '2018-03-01', '2018-06-30')
evolucion_medias_magnitud(df, '12')
