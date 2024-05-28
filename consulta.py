from django.db import connection
import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE","corredora.settings")
django.setup()

def inmueblesComuna():

    sql_comunas = """
    SELECT DISTINCT web_comuna.id, web_comuna.nombre 
    FROM web_comuna
    ORDER BY web_comuna.id ASC;
    """
    with connection.cursor() as cursor1:
        cursor1.execute(sql_comunas)
        comunas = cursor1.fetchall()
        for comuna in comunas:
            criterio = comuna[0]
            with open("inmuebles-comuna.txt", "a", encoding="utf-8") as archivo:
                archivo.write(comuna[1] + ":"+"\n")
                archivo.close()
                with connection.cursor() as cursor:
                    sql = f"""
                    SELECT web_inmueble.nombre AS nombre_inmueble, web_inmueble.descripcion AS descripcion_inmueble, web_region.nombre AS nombre_region
                    FROM web_inmueble
                    INNER JOIN web_region ON web_inmueble.region_id = web_region.id
                    GROUP BY web_inmueble.region_id, web_inmueble.nombre, web_inmueble.descripcion, web_region.nombre
                    HAVING web_inmueble.region_id = {criterio} 
                    ORDER BY web_inmueble.region_id ASC;
                    """
                    cursor.execute(sql)
                    inmuebles = cursor.fetchall()

                    print(criterio, comuna[1] +" ->", len(inmuebles))

                    if not inmuebles:
                        with open("inmuebles-comuna.txt", "a", encoding="utf-8") as archivo:
                            archivo.write("\tSin inmuebles registrados en la Comuna\n")
                    else:
                        for inmueble in inmuebles:
                            with open("inmuebles-comuna.txt", "a", encoding="utf-8") as archivo:
                                archivo.write("\t" + inmueble[0] + ", " + inmueble[1] +"\n")
                        archivo.close()


def inmueblesRegion():

    sql_region = """
    SELECT DISTINCT web_region.id, web_region.nombre 
    FROM web_region
    ORDER BY web_region.id ASC;
    """
    with connection.cursor() as cursor1:
        cursor1.execute(sql_region)
        regiones = cursor1.fetchall()
        for region in regiones:
            criterio = region[0]
            with open("inmuebles-region.txt", "a", encoding="utf-8") as archivo:
                archivo.write(region[1] + ":"+"\n")
                archivo.close()
                with connection.cursor() as cursor:
                    sql = f"""
                    SELECT web_inmueble.nombre AS nombre_inmueble, web_inmueble.descripcion AS descripcion_inmueble, web_region.nombre AS nombre_region
                    FROM web_inmueble
                    INNER JOIN web_region ON web_inmueble.region_id = web_region.id
                    GROUP BY web_inmueble.region_id, web_inmueble.nombre, web_inmueble.descripcion, web_region.nombre
                    HAVING web_inmueble.region_id = {criterio} 
                    ORDER BY web_inmueble.region_id ASC;
                    """
                    cursor.execute(sql)
                    inmuebles = cursor.fetchall()

                    print(criterio, region[1] +" ->", len(inmuebles))

                    if not inmuebles:
                        with open("inmuebles-region.txt", "a", encoding="utf-8") as archivo:
                            archivo.write("\tSin inmuebles registrados en la Región\n")
                    else:
                        for inmueble in inmuebles:
                            with open("inmuebles-region.txt", "a", encoding="utf-8") as archivo:
                                archivo.write("\t" + inmueble[0] + ", " + inmueble[1] +"\n")
                        archivo.close()

def consultas():

    inmueblesComuna()
    inmueblesRegion()