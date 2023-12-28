import csv
from behave import *
from scripts.Class_Kpi_mod_baja import Kpi_baja

@given('Abriendo el csv "{filename}" con los kpis correctos')
def abrir_csv(context, filename):
    # Cargar los datos de entrada desde tu archivo CSV de referencia
    try:
        with open(filename, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            context.datos_correctos = list(reader)
            print("Archivo leído correctamente")
    except FileNotFoundError:
        print(f"Error: No se pudo abrir el archivo {filename}")
        context.datos_correctos = None


@when('Se obtengan los kpis de la clase para el periodo entre "{fecha_inicio}" y "{fecha_fin}"')
def obtener_kpis_comparacion(context, fecha_inicio, fecha_fin):
    # Realizar los cálculos con tu clase y guardar los resultados
    kpi = Kpi_baja("Custom", start_period=fecha_inicio, end_period=fecha_fin)
    kpi.get_period()
    kpi.get_data()
    kpi.group_data()
    context.resultados_obtenidos = kpi.kpis_result


@then("Se comparan el otp 15 de la clase con los del csv")
def comparar_otp15_csv(context):
    respuestas= []
    for estacion_correcto, estacion_obtenido in zip(context.datos_correctos, context.resultados_obtenidos):
        if estacion_correcto['Carrier'] == estacion_obtenido['Carrier'] and estacion_correcto['station'] == estacion_obtenido['Estacion']:
            if float(estacion_correcto['OTP_15']) == float(estacion_obtenido['OTP_15']):
                respuestas.append(True)
            else:
                print("OTP15 no coiciden para {}_{}. \n Respuesta obtenida: {}. Respuesta correcta: {}".format(
                    estacion_obtenido['Carrier'], estacion_obtenido['Estacion'],
                    estacion_obtenido['OTP_15'], estacion_correcto['OTP_15']
                ))
                respuestas.append(False)
    assert all(respuestas), "Los valores de OTP_15 no coinciden"

@then("Se comparan el otp 15 wx & cta de la clase con los del csv")
def comparar_otp15_wxcta_csv(context):
    respuestas= []
    for estacion_correcto, estacion_obtenido in zip(context.datos_correctos, context.resultados_obtenidos):
        if estacion_correcto['Carrier'] == estacion_obtenido['Carrier'] and estacion_correcto['station'] == estacion_obtenido['Estacion']:
            if float(estacion_correcto['OTP_WX&CTA']) == float(estacion_obtenido['OTP_WX&CTA']):
                respuestas.append(True)
            else:
                print("OTP15 WX & CTA no coiciden para {}_{}. \n Respuesta obtenida: {}. Respuesta correcta: {}".format(
                    estacion_obtenido['Carrier'], estacion_obtenido['Estacion'],
                    estacion_obtenido['OTP_WX&CTA'], estacion_correcto['OTP_WX&CTA']
                ))
                respuestas.append(False)
    assert all(respuestas), "Los valores de OTP_15 WX & CTA no coinciden"

@then("Se comparan el btp 0 de la clase con los del csv")
def comparar_btp0_csv(context):
    respuestas= []
    for estacion_correcto, estacion_obtenido in zip(context.datos_correctos, context.resultados_obtenidos):
        if estacion_correcto['Carrier'] == estacion_obtenido['Carrier'] and estacion_correcto['station'] == estacion_obtenido['Estacion']:
            if float(estacion_correcto['BTP_0']) == float(estacion_obtenido['BTP_0']):
                respuestas.append(True)
            else:
                print("BTP 0 no coiciden para {}_{}. \n Respuesta obtenida: {}. Respuesta correcta: {}".format(
                    estacion_obtenido['Carrier'], estacion_obtenido['Estacion'],
                    estacion_obtenido['BTP_0'], estacion_correcto['BTP_0']
                ))
                respuestas.append(False)
    assert all(respuestas), "Los valores de BTP_0 no coinciden"

@then("Se comparan el btp 5 de la clase con los del csv")
def comparar_btp0_csv(context):
    respuestas = []
    for estacion_correcto, estacion_obtenido in zip(context.datos_correctos, context.resultados_obtenidos):
        if estacion_correcto['Carrier'] == estacion_obtenido['Carrier'] and estacion_correcto['station'] == \
                estacion_obtenido['Estacion']:
            if float(estacion_correcto['BTP_5']) == float(estacion_obtenido['BTP_5']):
                respuestas.append(True)
            else:
                print("BTP 5 no coiciden para {}_{}. \n Respuesta obtenida: {}. Respuesta correcta: {}".format(
                    estacion_obtenido['Carrier'], estacion_obtenido['Estacion'],
                    estacion_obtenido['BTP_5'], estacion_correcto['BTP_5']
                ))
                respuestas.append(False)
    assert all(respuestas), "Los valores de BTP_5 no coinciden"

@then("Se comparan el atd 0 de la clase con los del csv")
def comparar_atd0_csv(context):
    respuestas = []
    for estacion_correcto, estacion_obtenido in zip(context.datos_correctos, context.resultados_obtenidos):
        if estacion_correcto['Carrier'] == estacion_obtenido['Carrier'] and estacion_correcto['station'] == \
                estacion_obtenido['Estacion']:
            if float(estacion_correcto['ATD_0']) == float(estacion_obtenido['ATD_0']):
                respuestas.append(True)
            else:
                print("ATD 0 no coiciden para {}_{}. \n Respuesta obtenida: {}. Respuesta correcta: {}".format(
                    estacion_obtenido['Carrier'], estacion_obtenido['Estacion'],
                    estacion_obtenido['ATD_0'], estacion_correcto['ATD_0']
                ))
                respuestas.append(False)
    assert all(respuestas), "Los valores de ATD_0 no coinciden"

@then("Se comparan el atd 5 de la clase con los del csv")
def comparar_atd5_csv(context):
    respuestas = []
    for estacion_correcto, estacion_obtenido in zip(context.datos_correctos, context.resultados_obtenidos):
        if estacion_correcto['Carrier'] == estacion_obtenido['Carrier'] and estacion_correcto['Estacion'] == \
                estacion_obtenido['Estacion']:
            if (float(estacion_correcto['Num_atd5']) == float(estacion_obtenido['Num_atd5']) and
                    float(estacion_correcto['Den_atd5']) == float(estacion_obtenido['Den_atd5'])):
                respuestas.append(True)
            else:
                print("""ATD 5 no coiciden para {}_{}. \n Respuesta obtenida: {}. Respuesta correcta: {} \n
                        Calculado: {}/{}. Correcto: {}/{}""".format(
                    estacion_obtenido['Carrier'], estacion_obtenido['Estacion'],
                    estacion_obtenido['ATD_5'], estacion_correcto['ATD_5'],
                    estacion_obtenido['Num_atd5'], estacion_obtenido['Den_atd5'],
                    estacion_correcto['Num_atd5'], estacion_correcto['Den_atd5']
                ))
                respuestas.append(False)
    assert all(respuestas), "Los valores de ATD_5 no coinciden"

@then("Se comparan el gtp 0 de la clase con los del csv")
def comparar_gtp0_csv(context):
    respuestas = []
    for estacion_correcto, estacion_obtenido in zip(context.datos_correctos, context.resultados_obtenidos):
        if estacion_correcto['Carrier'] == estacion_obtenido['Carrier'] and estacion_correcto['Estacion'] == \
                estacion_obtenido['Estacion']:
            if (float(estacion_correcto['Num_gtp0']) == float(estacion_obtenido['Num_gtp0']) and
                    float(estacion_correcto['Den_gtp0']) == float(estacion_obtenido['Den_gtp0'])):
                respuestas.append(True)
            else:
                print("""GTP 0 no coiciden para {}_{}. \n Respuesta obtenida: {}. Respuesta correcta: {} \n
                        Calculado: {}/{}. Correcto: {}/{}""".format(
                    estacion_obtenido['Carrier'], estacion_obtenido['Estacion'],
                    estacion_obtenido['GTP_0'], estacion_correcto['GTP_0'],
                    estacion_obtenido['Num_gtp0'], estacion_obtenido['Den_gtp0'],
                    estacion_correcto['Num_gtp0'], estacion_correcto['Den_gtp0']
                ))
                respuestas.append(False)
    assert all(respuestas), "Los valores de GTP_0 no coinciden"


@then("Se comparan el gtp 5 de la clase con los del csv")
def comparar_gtp5_csv(context):
    respuestas = []
    for estacion_correcto, estacion_obtenido in zip(context.datos_correctos, context.resultados_obtenidos):
        if estacion_correcto['Carrier'] == estacion_obtenido['Carrier'] and estacion_correcto['Estacion'] == \
                estacion_obtenido['Estacion']:
            if (float(estacion_correcto['Num_gtp5']) == float(estacion_obtenido['Num_gtp5']) and
                    float(estacion_correcto['Den_gtp5']) == float(estacion_obtenido['Den_gtp5'])):
                respuestas.append(True)
            else:
                print("""GTP 5 no coiciden para {}_{}. \n Respuesta obtenida: {}. Respuesta correcta: {} \n
                        Calculado: {}/{}. Correcto: {}/{}""".format(
                    estacion_obtenido['Carrier'], estacion_obtenido['Estacion'],
                    estacion_obtenido['GTP_5'], estacion_correcto['GTP_5'],
                    estacion_obtenido['Num_gtp5'], estacion_obtenido['Den_gtp5'],
                    estacion_correcto['Num_gtp5'], estacion_correcto['Den_gtp5']
                ))
                respuestas.append(False)
    assert all(respuestas), "Los valores de GTP_5 no coinciden"

@then("Se comparan el pax de la clase con los del csv")
def comparar_pax_csv(context):
    respuestas = []
    for estacion_correcto, estacion_obtenido in zip(context.datos_correctos, context.resultados_obtenidos):
        if estacion_correcto['Carrier'] == estacion_obtenido['Carrier'] and estacion_correcto['Estacion'] == \
                estacion_obtenido['Estacion']:
            if (float(estacion_correcto['Num_pax']) == float(estacion_obtenido['Num_pax']) and
                    float(estacion_correcto['Den_gtp5']) == float(estacion_obtenido['Den_gtp5'])):
                respuestas.append(True)
            else:
                print("""PAX no coiciden para {}_{}. \n Respuesta obtenida: {}. Respuesta correcta: {} \n
                        Calculado: {}/{}. Correcto: {}/{}""".format(
                    estacion_obtenido['Carrier'], estacion_obtenido['Estacion'],
                    estacion_obtenido['PAX'], estacion_correcto['PAX'],
                    estacion_obtenido['Num_pax'], estacion_obtenido['Den_pax'],
                    estacion_correcto['Num_pax'], estacion_correcto['Den_pax']
                ))
                respuestas.append(False)
    assert all(respuestas), "Los valores de PAX no coinciden"