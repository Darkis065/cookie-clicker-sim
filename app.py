from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


# ==========================================
# 1. TUS CLASES
# ==========================================
class Edificios:

  def __init__(self, nombre, precio, cps_ind):
    self.nombre = nombre
    self.precio = float(precio)
    self.cps_ind = float(cps_ind)
    self.nivel = 0
    self.produccion = 0.0
    self.actualizacion()

  def comprar_edificio(self):
    self.nivel += 1
    self.precio *= 1.15
    self.actualizacion()

  def comprar_mejora_doble(self):
    self.cps_ind *= 2.0
    self.actualizacion()

  def actualizacion(self):
    self.produccion = self.nivel * self.cps_ind
    self.trp = (self.precio / self.cps_ind) if self.cps_ind > 0 else 0.0

  def a_dict(self):
    return {
        "nombre": self.nombre,
        "precio": self.precio,
        "cps_ind": self.cps_ind,
        "nivel": self.nivel,
        "produccion": self.produccion,
        "trp": self.trp,
    }


class MejoraGalleta:

  def __init__(self, nombre, precio, porcentaje_aumento):
    self.nombre = nombre
    self.precio = float(precio)
    self.porcentaje = float(porcentaje_aumento)
    self.comprada = False

  def comprar(self):
    self.comprada = True

  def a_dict(self, cps_base_total):
    cps_ganado = cps_base_total * self.porcentaje
    trp = (self.precio / cps_ganado) if cps_ganado > 0 else None
    return {
        "nombre": self.nombre,
        "precio": self.precio,
        "porcentaje": self.porcentaje,
        "comprada": self.comprada,
        "trp": trp,
    }


# ==========================================
# 2. FUNCIONES DE CÁLCULO
# ==========================================
def calcular_cps_total(lista_edificios, lista_galletas):
  cps_base = sum(edificio.produccion for edificio in lista_edificios)
  mult = multiplicador_global(lista_galletas)
  return cps_base * mult


def calcular_valor_edificios(lista_edificios):
  return sorted(lista_edificios, key=lambda x: x.trp)


def multiplicador_global(lista_galletas: list):
  multiplicador = 1.0
  for galleta in lista_galletas:
    if galleta.comprada:
      multiplicador *= 1.0 + galleta.porcentaje
  return multiplicador


# ==========================================
# 3. INSTANCIAS DE EDIFICIOS Y GALLETAS
# ==========================================
cursor = Edificios("Cursor", 15, 0.1)
abuela = Edificios("Abuela", 100, 1)
granja = Edificios("Granja", 1100, 8)
mina = Edificios("Mina", 12000, 47)
fabrica = Edificios("Fábrica", 130000, 260)
banco = Edificios("Banco", 1400000, 1400)
templo = Edificios("Templo", 20000000, 7800)
torre_de_magos = Edificios("Torre de magos", 330000000, 44000)
envio = Edificios("Envío", 5100000000, 260000)
lab_de_alquimia = Edificios("Lab. de alquimia", 75000000000, 1600000)
portal = Edificios("Portal", 1000000000000, 10000000)
maquina_del_tiempo = Edificios("Máquina del tiempo", 14000000000000, 65000000)
condensador_de_antimateria = Edificios(
    "Condensador de antimateria", 170000000000000, 430000000
)
prisma = Edificios("Prisma", 2100000000000000, 2900000000)
generador_de_suerte = Edificios(
    "Generador de suerte", 26000000000000000, 21000000000
)
motor_fractal = Edificios("Motor fractal", 310000000000000000, 150000000000)
consola_de_javascript = Edificios(
    "Consola de JavaScript", 71000000000000000000, 1100000000000
)
idleverso = Edificios("Idleverso", 12000000000000000000000, 8300000000000)
panadero_cortex = Edificios(
    "Panadero Cortex", 1900000000000000000000000, 64000000000000
)
tu = Edificios("Tú", 540000000000000000000000000, 510000000000000)

edf = [
    cursor,
    abuela,
    granja,
    mina,
    fabrica,
    banco,
    templo,
    torre_de_magos,
    envio,
    lab_de_alquimia,
    portal,
    maquina_del_tiempo,
    condensador_de_antimateria,
    prisma,
    generador_de_suerte,
    motor_fractal,
    consola_de_javascript,
    idleverso,
    panadero_cortex,
    tu,
]

glts = [
    MejoraGalleta("Plain cookies", 16, 0.01),
    MejoraGalleta("Sugar cookies", 110, 0.01),
    MejoraGalleta("Oatmeal raisin cookies", 550, 0.01),
    MejoraGalleta("Peanut butter cookies", 2750, 0.01),
    MejoraGalleta("Coconut cookies", 13750, 0.01),
    MejoraGalleta("White chocolate cookies", 68750, 0.02),
    MejoraGalleta("Macadamia nut cookies", 343750, 0.02),
    MejoraGalleta("Double-chip cookies", 1718750, 0.02),
    MejoraGalleta("White chocolate macadamia nut cookies", 8593750, 0.02),
    MejoraGalleta("All-chocolate cookies", 42968750, 0.02),
    MejoraGalleta("Dark chocolate cookies", 214843750, 0.03),
    MejoraGalleta("Milk chocolate cookies", 1074218750, 0.03),
    MejoraGalleta("Brown sugar cookies", 5371093750, 0.03),
    MejoraGalleta("Hazelnut cookies", 26855468750, 0.03),
    MejoraGalleta("Fudge cookies", 134277343750, 0.03),
    MejoraGalleta("Sprinkles cookies", 671386718750, 0.04),
    MejoraGalleta("Apple cookies", 3356933593750, 0.04),
    MejoraGalleta("Shortbread cookies", 16784667968750, 0.04),
    MejoraGalleta("Pastry dragon cookies", 83923339843750, 0.04),
    MejoraGalleta("Rich butter cookies", 419616699218750, 0.05),
    MejoraGalleta("Crispy rice cookies", 2098083496093750, 0.05),
    MejoraGalleta("Chocolate chip cookies", 10490417480468750, 0.05),
    MejoraGalleta("Cinnamon cookies", 52452087402343750, 0.05),
    MejoraGalleta("Vanilla cookies", 262260437011718750, 0.05),
]

mapa_edificios = {e.nombre: e for e in edf}
mapa_galletas = {g.nombre: g for g in glts}


# ==========================================
# 4. ENDPOINTS DE FLASK
# ==========================================
@app.route("/")
def index():
  return render_template("index.html")


@app.route("/api/estado", methods=["GET"])
def obtener_estado():
  cps_total = calcular_cps_total(edf, glts)
  cps_base = sum(e.produccion for e in edf)
  edificios_ordenados = calcular_valor_edificios(edf)

  return jsonify({
      "cps_total": cps_total,
      "edificios": [e.a_dict() for e in edf],
      "galletas": [g.a_dict(cps_base) for g in glts],
      "recomendados": [e.a_dict() for e in edificios_ordenados[:3]],
  })


@app.route("/api/comprar_edificio", methods=["POST"])
def comprar_edificio():
  data = request.json or {}
  nombre = data.get("nombre")
  if nombre in mapa_edificios:
    mapa_edificios[nombre].comprar_edificio()
  return obtener_estado()


@app.route("/api/mejora_doble", methods=["POST"])
def mejora_doble():
  data = request.json or {}
  nombre = data.get("nombre")
  if nombre in mapa_edificios:
    mapa_edificios[nombre].comprar_mejora_doble()
  return obtener_estado()


@app.route("/api/comprar_galleta", methods=["POST"])
def comprar_galleta():
  data = request.json or {}
  nombre = data.get("nombre")
  if nombre in mapa_galletas:
    mapa_galletas[nombre].comprar()
  return obtener_estado()


if __name__ == "__main__":
  app.run(debug=True)