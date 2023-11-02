import pandas as pd
import numpy as np
import datetime as dt


emisiones_2016 = pd.read_csv('emisiones-2016.csv', sep = ';')
emisiones_2017 = pd.read_csv('emisiones-2017.csv', sep = ';')
emisiones_2018 = pd.read_csv('emisiones-2018.csv', sep = ';')
emisiones_2019 = pd.read_csv('emisiones-2019.csv', sep = ';')
df_emisiones = pd.concat([emisiones_2016, emisiones_2017, emisiones_2018, emisiones_2019])
print(df_emisiones)

columnas = ['ESTACION', 'MAGNITUD', 'ANO', 'MES']
columnas.extend([col for col in df_emisiones if col.startswith('D')])
df_emisiones = df_emisiones[columnas]
print(df_emisiones)

# Reestructurar el DataFrame para que los valores de los contaminantes de las columnas de los días aparezcan en una única columna.
df_emisiones = df_emisiones.melt(id_vars=['ESTACION', 'MAGNITUD', 'ANO', 'MES'], var_name='DIA', value_name='VALOR')
print(df_emisiones)
# Primero eliminamos el caracter D del comienzo de la columna de los días
df_emisiones['DIA'] = df_emisiones.DIA.str.strip('D')
# Concatenamos las columnas del año, mes y día
df_emisiones['FECHA'] = df_emisiones.ANO.apply(str) + '/' + df_emisiones.MES.apply(str) + '/' + df_emisiones.DIA.apply(str)
# Convertimos la nueva columna al tipo fecha
df_emisiones['FECHA'] = pd.to_datetime(df_emisiones.FECHA, format='%Y/%m/%d', infer_datetime_format=True, errors='coerce')
print(df_emisiones)
# Eliminar las filas con fechas no válidas
df_emisiones = df_emisiones.drop(df_emisiones[np.isnat(df_emisiones.FECHA)].index)
# Ordenar el el dataframe por estación, magnitud y fecha
df_emisiones.sort_values(['ESTACION', 'MAGNITUD', 'FECHA'])
# Mostrar las estaciones disponibles
print('Estaciones:', df_emisiones.ESTACION.unique())
# Mostrar los contaminantes disponibles
print('Contaminantes:', df_emisiones.MAGNITUD.unique())
# Resumen descriptivo por contaminantes
df_emisiones.groupby('MAGNITUD').VALOR.describe()
# Resumen descriptivo por contaminantes y distritos
df_emisiones.groupby(['ESTACION', 'MAGNITUD']).VALOR.describe()
# Función que devuelve un resumen descriptivo de la emisiones en un contaminante dado en un estación dada
def resumen(estacion, contaminante):
    return df_emisiones[(df_emisiones.ESTACION == estacion) & (df_emisiones.MAGNITUD == contaminante)].VALOR.describe()

# Resumen de Dióxido de Nitrógeno en Plaza Elíptica
print('Resumen Dióxido de Nitrógeno en Plaza Elíptica:\n', resumen(56, 8),'\n', sep='')
# Resumen de Dióxido de Nitrógeno en Plaza del Carmen
print('Resumen Dióxido de Nitrógeno en Plaza del Carmen:\n', resumen(35, 8), sep='')
# Función que devuelve una serie con las emisiones medias mensuales de un contaminante y un mes año para todos las estaciones
def evolucion_mensual(contaminante, año):
    return df_emisiones[(df_emisiones.MAGNITUD == contaminante) & (df_emisiones.ANO == año)].groupby(['ESTACION', 'MES']).VALOR.mean().unstack('MES')

# Evolución del dióxido de nitrógeno en 2019
evolucion_mensual(8, 2019)