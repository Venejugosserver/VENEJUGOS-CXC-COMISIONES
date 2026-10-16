"""Lee la tasa oficial del Banco Central de Venezuela y la guarda en tasa_bcv.json.

La usa el panel de CxC y comisiones para mostrar los montos en bolívares.
Orden de fuentes:
  1. bcv.org.ve (tasas oficiales: dólar, euro, yuan, lira y rublo).
  2. ve.dolarapi.com (dólar oficial BCV), solo si el sitio del BCV no responde.
Si ninguna responde, no toca el archivo anterior y termina con error.
"""
import datetime
import json
import re
import sys

import requests
import urllib3

urllib3.disable_warnings()  # el certificado de bcv.org.ve suele venir incompleto

SALIDA = "tasa_bcv.json"
UA = {"User-Agent": "Mozilla/5.0 (panel CxC Venejugos; tasa BCV)"}
MONEDAS = {"dolar": "usd", "euro": "eur", "yuan": "cny", "lira": "try", "rublo": "rub"}


def numero(texto):
    texto = texto.strip().replace(" ", "")
    if "," in texto:
        texto = texto.replace(".", "").replace(",", ".")
    return float(texto)


def desde_bcv():
    r = requests.get("https://www.bcv.org.ve/", headers=UA, timeout=45, verify=False)
    r.raise_for_status()
    html = r.text
    tasas = {}
    for div, codigo in MONEDAS.items():
        m = re.search(r'id="%s".*?<strong>\s*([\d.,]+)\s*</strong>' % div, html, re.S | re.I)
        if m:
            tasas[codigo] = round(numero(m.group(1)), 8)
    if not tasas.get("usd"):
        raise ValueError("no encontré la tasa del dólar en bcv.org.ve")
    m = re.search(r'Fecha\s+Valor:.*?content="(\d{4}-\d{2}-\d{2})', html, re.S | re.I)
    fecha = m.group(1) if m else datetime.date.today().isoformat()
    return {"fuente": "BCV (bcv.org.ve)", "fecha_valor": fecha, "tasas": tasas}


def desde_dolarapi():
    r = requests.get("https://ve.dolarapi.com/v1/dolares/oficial", headers=UA, timeout=30)
    r.raise_for_status()
    d = r.json()
    valor = d.get("promedio") or d.get("venta") or d.get("compra")
    if not valor:
        raise ValueError("DolarApi no trajo la tasa")
    fecha = str(d.get("fechaActualizacion") or "")[:10] or datetime.date.today().isoformat()
    return {"fuente": "BCV vía DolarApi", "fecha_valor": fecha, "tasas": {"usd": round(float(valor), 8)}}


def main():
    errores = []
    for fuente in (desde_bcv, desde_dolarapi):
        try:
            datos = fuente()
            usd = datos["tasas"]["usd"]
            if not (0 < usd < 1_000_000):
                raise ValueError(f"tasa fuera de rango: {usd}")
            datos["actualizado"] = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            with open(SALIDA, "w", encoding="utf-8") as f:
                json.dump(datos, f, ensure_ascii=False, indent=2)
            print(f"Tasa guardada: {usd} Bs. por US$ ({datos['fuente']}, fecha valor {datos['fecha_valor']})")
            return 0
        except Exception as e:  # sigue con la siguiente fuente
            errores.append(f"{fuente.__name__}: {e}")
    print("No se pudo leer la tasa:\n  " + "\n  ".join(errores), file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
