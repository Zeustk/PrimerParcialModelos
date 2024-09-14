import pygame
import sys
import numpy_financial as npf
import tkinter as tk



def evaluar_rentabilidad(costos_ope_anuales, ingresos_ventas_anuales, fn_flujos_caja, Tir, Vpn, Inversion_inicial,tasa_descue):
   

    if costos_ope_anuales >= ingresos_ventas_anuales:
       return "No rentable: costos operativos >= ingresos anuales."

    if fn_flujos_caja <= 0:
        return "No rentable: flujo de caja neto es negativo."

    if Tir <= 0:
        return "No rentable: TIR <= 0."

    if tir < tasa_descue * 100:  # tasa_descuento está en decimal, multiplicamos por 100 para comparar en porcentaje
        return "No rentable: TIR <= TASA DESCUENTO."
    if Vpn <= Inversion_inicial:
       return "No rentable: VPN <= inversión inicial."

    return "El proyecto es rentable."


# Variables globales para los valores del formulario
global precio_carbon_local, costos_extraccion, costos_transporte
global inversion_inicial, precio_nuevo_producto, demanda_mercado, tasa_crecimiento_demanda
global tasa_descuento, vida_proyecto, cantidad_carbon

# Función para solicitar entradas del usuario
def solicitar_entradas():
    # Crear una ventana de Tkinter
    root = tk.Tk()
    root.title("Entrada de Datos")

    # Función para manejar el envío de los datos
    def enviar_datos():
        global precio_carbon_local, costos_extraccion, costos_transporte
        global inversion_inicial, precio_nuevo_producto, demanda_mercado, tasa_crecimiento_demanda
        global tasa_descuento, vida_proyecto, cantidad_carbon
        
        # Asignar valores a las variables globales
        precio_carbon_local = float(entry_precio_carbon_local.get())
        costos_extraccion = float(entry_costos_extraccion.get())
        costos_transporte = float(entry_costos_transporte.get())
        inversion_inicial = float(entry_inversion_inicial.get())
        precio_nuevo_producto = float(entry_precio_nuevo_producto.get())
        demanda_mercado = float(entry_demanda_mercado.get())
        tasa_crecimiento_demanda = float(entry_tasa_crecimiento_demanda.get())
        tasa_descuento = float(entry_tasa_descuento.get())
        vida_proyecto = int(entry_vida_proyecto.get())
        cantidad_carbon = float(entry_cantidad_carbon.get())
        
        # Cerrar la ventana
        root.destroy()

    # Crear etiquetas y campos de entrada
    tk.Label(root, text="Precio del carbón local (Pc):").grid(row=0, column=0)
    entry_precio_carbon_local = tk.Entry(root)
    entry_precio_carbon_local.insert(0, "50")
    entry_precio_carbon_local.grid(row=0, column=1)


    tk.Label(root, text="Costos de extracción y producción (Ce):").grid(row=2, column=0)
    entry_costos_extraccion = tk.Entry(root)
    entry_costos_extraccion.insert(0, "20000")
    entry_costos_extraccion.grid(row=2, column=1)

    tk.Label(root, text="Costos de transporte y logística (Ct):").grid(row=3, column=0)
    entry_costos_transporte = tk.Entry(root)
    entry_costos_transporte.insert(0, "10000")
    entry_costos_transporte.grid(row=3, column=1)

    tk.Label(root, text="Inversión inicial (Ii):").grid(row=4, column=0)
    entry_inversion_inicial = tk.Entry(root)
    entry_inversion_inicial.insert(0, "200000")
    entry_inversion_inicial.grid(row=4, column=1)

    tk.Label(root, text="Precio del nuevo producto (Pn):").grid(row=5, column=0)
    entry_precio_nuevo_producto = tk.Entry(root)
    entry_precio_nuevo_producto.insert(0, "100")
    entry_precio_nuevo_producto.grid(row=5, column=1)

    tk.Label(root, text="Demanda del mercado (Dm):").grid(row=6, column=0)
    entry_demanda_mercado = tk.Entry(root)
    entry_demanda_mercado.insert(0, "10000")
    entry_demanda_mercado.grid(row=6, column=1)

    tk.Label(root, text="Tasa de crecimiento de la demanda (gd):").grid(row=7, column=0)
    entry_tasa_crecimiento_demanda = tk.Entry(root)
    entry_tasa_crecimiento_demanda.insert(0, "0.05")
    entry_tasa_crecimiento_demanda.grid(row=7, column=1)

    tk.Label(root, text="Tasa de descuento (r):").grid(row=8, column=0)
    entry_tasa_descuento = tk.Entry(root)
    entry_tasa_descuento.insert(0, "0.10")
    entry_tasa_descuento.grid(row=8, column=1)

    tk.Label(root, text="Vida útil del proyecto (Lp):").grid(row=9, column=0)
    entry_vida_proyecto = tk.Entry(root)
    entry_vida_proyecto.insert(0, "10")
    entry_vida_proyecto.grid(row=9, column=1)

    tk.Label(root, text="Cantidad de carbón (toneladas):").grid(row=10, column=0)
    entry_cantidad_carbon = tk.Entry(root)
    entry_cantidad_carbon.insert(0, "1000")
    entry_cantidad_carbon.grid(row=10, column=1)

    # Botón para enviar los datos
    boton_enviar = tk.Button(root, text="Enviar", command=enviar_datos)
    boton_enviar.grid(row=11, columnspan=2)

    # Ejecutar el bucle de la ventana
    root.mainloop()

# Llamar a la función para obtener las entradas del usuario
solicitar_entradas()
# Inicializar Pygame
pygame.init()

# Dimensiones de la ventana
ANCHO = 1200
ALTO = 600
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Simulación de Gasificación del Carbón")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (220, 220, 220)
AZUL = (135, 206, 235)
VERDE = (34, 139, 34)
ROJO = (220, 20, 60)
MARRON = (139, 69, 19)
AMARILLO = (255, 223, 0)
NARANJA = (255, 165, 0)
GRIS_OSCURO = (169, 169, 169)
AZUL_CLARO = (173, 216, 230)
VERDE_CLARO = (144, 238, 144)


# Fuente para el texto
fuente = pygame.font.SysFont("Arial", 20)

# Variables de simulación visual
num_camiones_carbon = 3
num_camiones_producto = 2

# Posiciones iniciales de camiones
pos_camiones_carbon = [[-60 * i, 280] for i in range(num_camiones_carbon)]
pos_camiones_producto = [[600, -60 * j] for j in range(num_camiones_producto)]
pos_planta = (600, 180)  # Posición de la planta eléctrica
pos_punto_venta = (1000, 250)  # Posición del punto de venta
pos_recoleccion_mina = (10, 250)  # Posición del punto de venta



# Listas para almacenar flujos de caja y calcular VPN y TIR
flujos_de_caja = [-inversion_inicial]  # El primer flujo de caja es la inversión inicial negativa

# Inicializar tiempo
tiempo = 0

# Variables para la leyenda
ingresos_totales = 0
flujo_caja_neto = 0
vpn = 0
tir = 0
costo_operativo_anual=0

# Cargar la imagen de la planta
imagen_planta_original = pygame.image.load("planta-removebg-preview.png")

# Cargar la imagen del exportacion
imagen_mineria_original = pygame.image.load("mineria-removebg-preview.png")

# Cargar la imagen del mineria
imagen_exportacion_original = pygame.image.load("exportacion-removebg-preview.png")

# Escalar la imagen a un tamaño menor, por ejemplo, 50x50 píxeles
imagen_planta = pygame.transform.scale(imagen_planta_original, (190, 170))
imagen_exportacion = pygame.transform.scale(imagen_exportacion_original, (220, 80))
imagen_mina = pygame.transform.scale(imagen_mineria_original, (220, 80))

# Funciones de dibujo
def dibujar_arbol(x, y):
    pygame.draw.rect(ventana, MARRON, (x + 10, y + 30, 20, 50))  # Tronco del árbol
    pygame.draw.circle(ventana, VERDE, (x + 20, y + 20), 30)  # Copa del árbol

def dibujar_lineaAmarilla(x, y, direccion='horizontal'):
    if direccion == 'horizontal':
        pygame.draw.rect(ventana, AMARILLO, (x + 10, y + 270, 50, 10))  # Línea horizontal
    elif direccion == 'vertical':
        pygame.draw.rect(ventana, AMARILLO, (x + 10, y + 10, 10, 50))  # Línea vertical


def dibujar_camion(x, y, color):
    pygame.draw.rect(ventana, color, (x, y, 60, 30))
    pygame.draw.circle(ventana, NEGRO, (x + 15, y + 30), 10)
    pygame.draw.circle(ventana, NEGRO, (x + 45, y + 30), 10)
    pygame.draw.rect(ventana, BLANCO, (x + 5, y + 5, 15, 10))  # Ventanas

def dibujar_edificio(x, y, ancho, alto):
    pygame.draw.rect(ventana, GRIS_OSCURO, (x, y, ancho, alto))
    for i in range(3):
        for j in range(4):
            pygame.draw.rect(ventana, BLANCO, (x + 10 + j * 20, y + 10 + i * 30, 15, 20))

def dibujar_planta(x, y):
    ventana.blit(imagen_planta, (x, y))

def dibujar_punto_venta(x, y):
    ventana.blit(imagen_exportacion, (x, y))

def dibujar_recoleccion_mina(x, y):
    ventana.blit(imagen_mina, (x, y))    

def dibujar_carbon(x, y):
    for i in range(3):
        pygame.draw.circle(ventana, NEGRO, (x + 10 * i, y + 10 * i), 8)  # Representar carbón


# Bucle principal de simulación
reloj = pygame.time.Clock()
simulacion_activa=True

# Estados de los camiones (0: moviéndose horizontalmente, 1: moviéndose verticalmente)
estados_camiones_carbon = [0] * num_camiones_carbon
estados_camiones_producto = [0] * num_camiones_producto

while simulacion_activa:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Dibujar fondo
    ventana.fill(VERDE_CLARO)

    # Dibujar calles
    pygame.draw.rect(ventana, NEGRO, (0, 250, ANCHO, 80))  # Calle horizontal más ancha
    pygame.draw.rect(ventana, NEGRO, (pos_planta[0] + 40, 0, 80, ALTO))  # Calle vertical más ancha

    # Dibujar árboles alrededor
    for x in range(50, ANCHO, 150):
        dibujar_arbol(x-50, 300)
    for x in range(50, ANCHO, 150):
        dibujar_arbol(x-50, 50)

    # Dibujar edificios
    for x in range(100, ANCHO, 300):
        dibujar_edificio(x, 50, 80, 100)
    for x in range(100, ANCHO, 300):
        dibujar_edificio(x, 400, 80, 100)

    # Dibujar líneas amarillas en la calle horizontal
    for x in range(50, ANCHO, 150):
        dibujar_lineaAmarilla(x, 10, 'horizontal')

    # Dibujar líneas amarillas en la calle vertical
    for y in range(50, ALTO, 150):
        dibujar_lineaAmarilla(660, y, 'vertical')


    # Dibujar planta eléctrica, carbón y punto de venta
    dibujar_planta(pos_planta[0], pos_planta[1])
    dibujar_carbon(pos_planta[0] + 70, pos_planta[1] + 60)
    dibujar_punto_venta(pos_punto_venta[0], pos_punto_venta[1])
    dibujar_recoleccion_mina(pos_recoleccion_mina[0], pos_recoleccion_mina[1])

    # Mover camiones de carbón
    for i in range(num_camiones_carbon):
        if estados_camiones_carbon[i] == 0:  # Movimiento horizontal
            if pos_camiones_carbon[i][0] < pos_planta[0] + 40:
                pos_camiones_carbon[i][0] += 2  # Movimiento hacia la planta
            else:
                estados_camiones_carbon[i] = 1  # Cambiar a movimiento vertical
        elif estados_camiones_carbon[i] == 1:  # Movimiento vertical
            if pos_camiones_carbon[i][1] < ALTO:
                pos_camiones_carbon[i][1] += 2  # Movimiento hacia abajo en la calle vertical
            else:
                pos_camiones_carbon[i] = [-60 * i, 280]  # Reiniciar al punto de partida
                estados_camiones_carbon[i] = 0  # Cambiar a movimiento horizontal

        dibujar_camion(pos_camiones_carbon[i][0], pos_camiones_carbon[i][1], VERDE)

    # Mover camiones de producto
    for j in range(num_camiones_producto):
        if estados_camiones_producto[j] == 0:  # Movimiento vertical
            if pos_camiones_producto[j][1] < pos_punto_venta[1]:
                pos_camiones_producto[j][1] += 2  # Movimiento hacia el punto de venta
            else:
                estados_camiones_producto[j] = 1  # Cambiar a movimiento horizontal
        elif estados_camiones_producto[j] == 1:  # Movimiento horizontal
            if pos_camiones_producto[j][0] < pos_punto_venta[0]:
                pos_camiones_producto[j][0] += 2  # Movimiento hacia la derecha
            else:
                # Al llegar al punto de venta, pasar un año
                tiempo += 1

                # Actualizar ingresos, costos operativos y flujos de caja
                ingresos_totales = demanda_mercado * precio_nuevo_producto
               
                costo_operativo_anual = (costos_extraccion + costos_transporte + (precio_carbon_local * cantidad_carbon)) * (1 + demanda_mercado/10000)
                flujo_caja_neto = ingresos_totales - costo_operativo_anual
             
                flujos_de_caja.append(flujo_caja_neto)
                demanda_mercado += demanda_mercado * tasa_crecimiento_demanda  # Incremento de la demanda
                
               
                # Recalcular VPN y TIR
                vpn = npf.npv(tasa_descuento, flujos_de_caja)
            
                tir = npf.irr(flujos_de_caja) * 100  # Convertir TIR a porcentaje
              

                # Reiniciar posición del camión
                pos_camiones_producto[j] = [600, -60 * j]
                estados_camiones_producto[j] = 0  # Reiniciar estado

        dibujar_camion(pos_camiones_producto[j][0], pos_camiones_producto[j][1], NARANJA)

    # Dibujar leyenda y estadísticas
    pygame.draw.rect(ventana, BLANCO, (10, 15, 460, 235))
    

    rentabilidad= evaluar_rentabilidad(costos_ope_anuales=costo_operativo_anual,ingresos_ventas_anuales=ingresos_totales,fn_flujos_caja=flujo_caja_neto,Tir=tir,Vpn=vpn,Inversion_inicial=inversion_inicial,tasa_descue=tasa_descuento)


    texto_leyenda = [
        "- Verde: Transporte de carbón",
        "- Naranja: Transporte de producto",
        f"Año actual: {tiempo}",
        f"Ingresos por la venta del nuevo producto (Iv): ${ingresos_totales:.2f}",
        f"Costos operativos Anuales del proyecto (Co): ${costo_operativo_anual:.2f}",
        f"Flujo de caja neto (Fn): ${flujo_caja_neto:.2f}",
        f"VPN: ${vpn:.2f}",
        f"TIR: {tir:.2f}%",
        f"{rentabilidad}",
    ]
    for i, linea in enumerate(texto_leyenda):
        texto = fuente.render(linea, True, NEGRO)
        ventana.blit(texto, (20, 20 + 25 * i))

    pygame.display.flip()
    reloj.tick(60)  # 60 FPS

    # Verificar si el tiempo ha alcanzado la vida del proyecto
    if tiempo >= vida_proyecto:

        print(f"Simulación terminada después de {tiempo} años.")
        simulacion_activa=False
