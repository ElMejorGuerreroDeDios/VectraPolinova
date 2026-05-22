import cv2
import numpy as np
import mediapipe as mp

mp_pose = mp.solutions.pose
mp_dibujo = mp.solutions.drawing_utils

# Colores BGR
COLOR_VERDE  = (0, 200, 100)
COLOR_ROJO   = (0, 60, 220)
COLOR_BLANCO = (255, 255, 255)
COLOR_GRIS   = (60, 60, 60)
COLOR_AZUL   = (200, 120, 0)

EJERCICIOS = {
    "Sentadilla": {
        "rodilla": {"min": 63,  "max": 100},
        "cadera":  {"min": 45,  "max": 100},
    },
    "Lagartija": {
        "codo":    {"min": 60,  "max": 90},
        "hombro":  {"min": 50,  "max": 90},
    },
    "Plancha": {
        "cadera":  {"min": 160, "max": 174},
        "tobillo": {"min": 0,  "max": 100},
    },
    "Zancada": {
        "rodilla_delantera": {"min": 80,  "max": 100},
        "rodilla_trasera":   {"min": 80,  "max": 120},
        "cadera":            {"min": 140, "max": 175},
    },
}

def obtener_punto(landmarks, indice, w, h):
    lm = landmarks[indice]
    return int(lm.x * w), int(lm.y * h)

def calcular_angulo(p1, p2, p3):
    a = np.array(p1)
    b = np.array(p2)
    c = np.array(p3)
    rad = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angulo = np.abs(rad * 180.0 / np.pi)
    if angulo > 180.0:
        angulo = 360 - angulo
    return int(angulo)

def evaluar_postura(angulo, minimo, maximo):
    if minimo <= angulo <= maximo:
        return "CORRECTA"
    return "INCORRECTA"

def dibujar_etiqueta(frame, texto, pos, color_fondo, color_texto=COLOR_BLANCO):
    x, y = pos
    (ancho_txt, alto_txt), _ = cv2.getTextSize(texto, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
    cv2.rectangle(frame, (x, y - alto_txt - 8), (x + ancho_txt + 8, y + 4), color_fondo, -1)
    cv2.putText(frame, texto, (x + 4, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color_texto, 2)

def dibujar_angulo_en_punto(frame, angulo, punto, color):
    cv2.putText(frame, f"{angulo}°", (punto[0] - 20, punto[1] - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2)

def dibujar_panel(frame, estados, ejercicio):
    cv2.rectangle(frame, (0, 0), (310, 40 + len(estados) * 35), COLOR_GRIS, -1)
    dibujar_etiqueta(frame, f"Ejercicio: {ejercicio}", (10, 30), COLOR_AZUL)
    for i, (nombre, angulo, estado) in enumerate(estados):
        color = COLOR_VERDE if estado == "CORRECTA" else COLOR_ROJO
        dibujar_etiqueta(frame, f"{nombre}: {angulo}° [{estado}]", (10, 65 + i * 35), color)

def dibujar_instrucciones(frame, h):
    instrucciones = ["1=Sentadilla", "2=Lagartija", "3=Plancha", "4=Zancada", "Q=Salir"]
    for i, txt in enumerate(instrucciones):
        cv2.putText(frame, txt, (10, h - 20 - (len(instrucciones) - 1 - i) * 22),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (150, 150, 150), 1)

# --- PROCESADORES INDIVIDUALES DE EJERCICIOS ---
def procesar_sentadilla(frame, landmarks, w, h):
    rangos = EJERCICIOS["Sentadilla"]
    cadera  = obtener_punto(landmarks, 23, w, h)
    rodilla = obtener_punto(landmarks, 25, w, h)
    tobillo = obtener_punto(landmarks, 27, w, h)
    hombro  = obtener_punto(landmarks, 11, w, h)
    ang_rodilla = calcular_angulo(cadera, rodilla, tobillo)
    ang_cadera  = calcular_angulo(hombro, cadera, rodilla)
    est_rodilla = evaluar_postura(ang_rodilla, rangos["rodilla"]["min"], rangos["rodilla"]["max"])
    est_cadera  = evaluar_postura(ang_cadera,  rangos["cadera"]["min"],  rangos["cadera"]["max"])
    dibujar_angulo_en_punto(frame, ang_rodilla, rodilla, COLOR_VERDE if est_rodilla == "CORRECTA" else COLOR_ROJO)
    dibujar_angulo_en_punto(frame, ang_cadera, cadera, COLOR_VERDE if est_cadera == "CORRECTA" else COLOR_ROJO)
    estados = [("Rodilla", ang_rodilla, est_rodilla), ("Cadera",  ang_cadera,  est_cadera)]
    return estados, all(e[2] == "CORRECTA" for e in estados)

def procesar_lagartija(frame, landmarks, w, h):
    rangos = EJERCICIOS["Lagartija"]
    hombro = obtener_punto(landmarks, 11, w, h)
    codo   = obtener_punto(landmarks, 13, w, h)
    muneca = obtener_punto(landmarks, 15, w, h)
    cadera = obtener_punto(landmarks, 23, w, h)
    ang_codo   = calcular_angulo(hombro, codo, muneca)
    ang_hombro = calcular_angulo(cadera, hombro, codo)
    est_codo   = evaluar_postura(ang_codo,   rangos["codo"]["min"],   rangos["codo"]["max"])
    est_hombro = evaluar_postura(ang_hombro, rangos["hombro"]["min"], rangos["hombro"]["max"])
    dibujar_angulo_en_punto(frame, ang_codo, codo, COLOR_VERDE if est_codo == "CORRECTA" else COLOR_ROJO)
    dibujar_angulo_en_punto(frame, ang_hombro, hombro, COLOR_VERDE if est_hombro == "CORRECTA" else COLOR_ROJO)
    estados = [("Codo",   ang_codo,   est_codo), ("Hombro", ang_hombro, est_hombro)]
    return estados, all(e[2] == "CORRECTA" for e in estados)

def procesar_plancha(frame, landmarks, w, h):
    rangos = EJERCICIOS["Plancha"]
    hombro  = obtener_punto(landmarks, 11, w, h)
    cadera  = obtener_punto(landmarks, 23, w, h)
    rodilla = obtener_punto(landmarks, 25, w, h)
    tobillo = obtener_punto(landmarks, 27, w, h)
    ang_cadera  = calcular_angulo(hombro, cadera, rodilla)
    ang_tobillo = calcular_angulo(cadera, tobillo, rodilla)
    est_cadera  = evaluar_postura(ang_cadera,  rangos["cadera"]["min"],  rangos["cadera"]["max"])
    est_tobillo = evaluar_postura(ang_tobillo, rangos["tobillo"]["min"], rangos["tobillo"]["max"])
    dibujar_angulo_en_punto(frame, ang_cadera, cadera, COLOR_VERDE if est_cadera == "CORRECTA" else COLOR_ROJO)
    dibujar_angulo_en_punto(frame, ang_tobillo, tobillo, COLOR_VERDE if est_tobillo == "CORRECTA" else COLOR_ROJO)
    estados = [("Cadera",  ang_cadera,  est_cadera), ("Tobillo", ang_tobillo, est_tobillo)]
    return estados, all(e[2] == "CORRECTA" for e in estados)

def procesar_zancada(frame, landmarks, w, h):
    rangos = EJERCICIOS["Zancada"]
    cadera_izq  = obtener_punto(landmarks, 23, w, h)
    rodilla_izq = obtener_punto(landmarks, 25, w, h)
    tobillo_izq = obtener_punto(landmarks, 27, w, h)
    cadera_der  = obtener_punto(landmarks, 24, w, h)
    rodilla_der = obtener_punto(landmarks, 26, w, h)
    tobillo_der = obtener_punto(landmarks, 28, w, h)
    hombro_izq  = obtener_punto(landmarks, 11, w, h)
    ang_rod_del = calcular_angulo(cadera_izq, rodilla_izq, tobillo_izq)
    ang_rod_tra = calcular_angulo(cadera_der, rodilla_der, tobillo_der)
    ang_cadera  = calcular_angulo(hombro_izq, cadera_izq, rodilla_izq)
    est_rod_del = evaluar_postura(ang_rod_del, rangos["rodilla_delantera"]["min"], rangos["rodilla_delantera"]["max"])
    est_rod_tra = evaluar_postura(ang_rod_tra, rangos["rodilla_trasera"]["min"], rangos["rodilla_trasera"]["max"])
    est_cadera  = evaluar_postura(ang_cadera,  rangos["cadera"]["min"], rangos["cadera"]["max"])
    dibujar_angulo_en_punto(frame, ang_rod_del, rodilla_izq, COLOR_VERDE if est_rod_del == "CORRECTA" else COLOR_ROJO)
    dibujar_angulo_en_punto(frame, ang_rod_tra, rodilla_der, COLOR_VERDE if est_rod_tra == "CORRECTA" else COLOR_ROJO)
    dibujar_angulo_en_punto(frame, ang_cadera, cadera_izq, COLOR_VERDE if est_cadera == "CORRECTA" else COLOR_ROJO)
    estados = [
        ("Rodilla delantera", ang_rod_del, est_rod_del),
        ("Rodilla trasera",   ang_rod_tra, est_rod_tra),
        ("Cadera (torso)",    ang_cadera,  est_cadera),
    ]
    return estados, all(e[2] == "CORRECTA" for e in estados)

PROCESADORES = {
    "Sentadilla": procesar_sentadilla,
    "Lagartija":  procesar_lagartija,
    "Plancha":    procesar_plancha,
    "Zancada":    procesar_zancada,
}

def abrir_camara_mediapipe(ejercicio_inicial):
    ejercicio_actual = ejercicio_inicial
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return
        
    # === CONFIGURACIÓN DE LA VENTANA (Agrega estas dos líneas) ===
    # 1. Permite que la ventana sea redimensionable por el sistema operativo
    cv2.namedWindow("Corrector de Postura - Calistenia", cv2.WINDOW_NORMAL)
    # 2. Fuerza a que mantenga la proporción (Aspect Ratio) para no deformar tu cara/cuerpo
    cv2.setWindowProperty("Corrector de Postura - Calistenia", cv2.WND_PROP_ASPECT_RATIO, cv2.WINDOW_KEEPRATIO)
    # =============================================================

    with mp_pose.Pose(min_detection_confidence=0.6, min_tracking_confidence=0.6) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break
            
            frame = cv2.flip(frame, 1)
            h, w = frame.shape[:2]
            
            # ... (el resto de tu código de procesamiento se queda exactamente igual) ...
            
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_rgb.flags.writeable = False
            resultados = pose.process(frame_rgb)
            frame_rgb.flags.writeable = True
            frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

            if resultados.pose_landmarks:
                landmarks = resultados.pose_landmarks.landmark
                mp_dibujo.draw_landmarks(
                    frame, resultados.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                    mp_dibujo.DrawingSpec(color=(0, 200, 255), thickness=2, circle_radius=3),
                    mp_dibujo.DrawingSpec(color=(0, 150, 200), thickness=2)
                )
                estados, postura_ok = PROCESADORES[ejercicio_actual](frame, landmarks, w, h)
                dibujar_panel(frame, estados, ejercicio_actual)
                mensaje = "POSTURA CORRECTA" if postura_ok else "CORRIGE TU POSTURA"
                dibujar_etiqueta(frame, mensaje, (w // 2 - 130, h - 20), COLOR_VERDE if postura_ok else COLOR_ROJO)
            else:
                cv2.putText(frame, "Sin persona detectada", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (100, 100, 100), 2)

            dibujar_instrucciones(frame, h)
            
            # El nombre de la ventana debe coincidir exactamente con el de namedWindow arriba
            cv2.imshow("Corrector de Postura - Calistenia", frame)
            
            tecla = cv2.waitKey(10) & 0xFF
            if tecla == ord('q') or tecla == ord('Q'): break
            elif tecla == ord('1'): ejercicio_actual = "Sentadilla"
            elif tecla == ord('2'): ejercicio_actual = "Lagartija"
            elif tecla == ord('3'): ejercicio_actual = "Plancha"
            elif tecla == ord('4'): ejercicio_actual = "Zancada"
            
    cap.release()
    cv2.destroyAllWindows()

"""import numpy as np

def calcular_angulo(a, b, c):
   
    a = np.array(a)
    b = np.array(b)
    c = np.array(c) 

    # Vectores desde B hacia A y desde B hacia C
    ba = a - b
    bc = c - b

    # Formula del coseno para obtener el angulo entre los vectores
    coseno = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-6)
    coseno = np.clip(coseno, -1.0, 1.0)  # Evita errores de redondeo
    angulo = np.degrees(np.arccos(coseno))

    return round(angulo, 1)


def obtener_punto(landmarks, indice, w, h):
    ---comentario
    Extrae las coordenadas [x, y] de un landmark en pixeles.
    
    Parámetros:
        landmarks : lista de landmarks de MediaPipe
        indice    : indice del punto (ver tabla abajo)
        w, h      : ancho y alto del frame de la camara
    
    Retorna:
        [x, y] en pixeles
    
    Indices importantes de MediaPipe Pose:
        11 = hombro izquierdo    12 = hombro derecho
        13 = codo izquierdo      14 = codo derecho
        15 = muñeca izquierda    16 = muñeca derecha
        23 = cadera izquierda    24 = cadera derecha
        25 = rodilla izquierda   26 = rodilla derecha
        27 = tobillo izquierdo   28 = tobillo derecho
    ---comentario
    lm = landmarks[indice]
    return [int(lm.x * w), int(lm.y * h)]


def evaluar_postura(angulo, minimo, maximo):

    if minimo <= angulo <= maximo:
        return "Correcto"
    else:
        return "Incorrecto"
"""