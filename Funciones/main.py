import sys
import os
from PyQt5.QtWidgets import QApplication

# Agregamos la ruta del módulo de interfaces para que Python lo lea correctamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../interfaces/Select_exercise')))
from select_exercise import SelectExercise

def main():
    app = QApplication(sys.argv)
    menu_principal = SelectExercise()
    menu_principal.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

"""
---comentario
CORRECTOR DE POSTURA

Controles de teclado:
    1  ->  Sentadilla
    2  ->  Lagartija
    3  ->  Plancha
    4  ->  Zancada
    Q  ->  Salir
---comentario

import cv2
import mediapipe as mp
from utils import calcular_angulo, obtener_punto, evaluar_postura


# Configuracion de MediaPipe

mp_pose   = mp.solutions.pose   #ignoralo pls es un fallo visual
mp_dibujo = mp.solutions.drawing_utils  #ignoralo pls es un fallo visual


# Ejercicios y rangos de angulos
EJERCICIOS = {
    "Sentadilla": {
        "rodilla": {"min": 80,  "max": 100},
        "cadera":  {"min": 70,  "max": 110},
    },
    "Lagartija": {
        "codo":    {"min": 70,  "max": 100},
        "hombro":  {"min": 50,  "max": 90},
    },
    "Plancha": {
        "cadera":  {"min": 160, "max": 180},
        "tobillo": {"min": 80,  "max": 100},
    },
    "Zancada": {
        "rodilla_delantera": {"min": 85,  "max": 100},
        "rodilla_trasera":   {"min": 85,  "max": 100},
        "cadera":            {"min": 170, "max": 180},
    },
}

ejercicio_actual = "Sentadilla"

# Colores
COLOR_VERDE  = (0, 200, 100)
COLOR_ROJO   = (0, 60, 220)
COLOR_BLANCO = (255, 255, 255)
COLOR_GRIS   = (60, 60, 60)
COLOR_AZUL   = (200, 120, 0)


# Funciones de dibujo
def dibujar_etiqueta(frame, texto, pos, color_fondo, color_texto=COLOR_BLANCO):
    ---Dibuja un texto con fondo de color sólido.---
    x, y = pos
    (ancho_txt, alto_txt), _ = cv2.getTextSize(texto, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
    cv2.rectangle(frame, (x, y - alto_txt - 8), (x + ancho_txt + 8, y + 4), color_fondo, -1)
    cv2.putText(frame, texto, (x + 4, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color_texto, 2)


def dibujar_angulo_en_punto(frame, angulo, punto, color):
    ---Muestra el valor del ángulo flotando cerca de la articulación.---
    cv2.putText(
        frame,
        f"{angulo}°",
        (punto[0] - 20, punto[1] - 15),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55, color, 2
    )


def dibujar_panel(frame, estados, ejercicio):
    ---Dibuja el panel lateral con los ángulos y sus estados---
    cv2.rectangle(frame, (0, 0), (310, 40 + len(estados) * 35), COLOR_GRIS, -1)
    dibujar_etiqueta(frame, f"Ejercicio: {ejercicio}", (10, 30), COLOR_AZUL)
    for i, (nombre, angulo, estado) in enumerate(estados):
        color = COLOR_VERDE if estado == "CORRECTA" else COLOR_ROJO
        dibujar_etiqueta(frame, f"{nombre}: {angulo}° [{estado}]", (10, 65 + i * 35), color)


def dibujar_instrucciones(frame, h):
    ---Muestra los controles de teclado en la esquina inferior izquierda---
    instrucciones = ["1=Sentadilla", "2=Lagartija", "3=Plancha", "4=Zancada", "Q=Salir"]
    for i, txt in enumerate(instrucciones):
        cv2.putText(frame, txt, (10, h - 20 - (len(instrucciones) - 1 - i) * 22),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (150, 150, 150), 1)



# Funciones de procesamiento por ejercicio
def procesar_sentadilla(frame, landmarks, w, h):
    ---comentario
    Evalua: angulo de rodilla (cadera→rodilla→tobillo)
            angulo de cadera  (hombro→cadera→rodilla)
    Correcto al bajar: rodilla ~90°, cadera 70°–110°
    ---comentario
    rangos = EJERCICIOS["Sentadilla"]

    cadera  = obtener_punto(landmarks, 23, w, h)
    rodilla = obtener_punto(landmarks, 25, w, h)
    tobillo = obtener_punto(landmarks, 27, w, h)
    hombro  = obtener_punto(landmarks, 11, w, h)

    ang_rodilla = calcular_angulo(cadera, rodilla, tobillo)
    ang_cadera  = calcular_angulo(hombro, cadera, rodilla)

    est_rodilla = evaluar_postura(ang_rodilla, rangos["rodilla"]["min"], rangos["rodilla"]["max"])
    est_cadera  = evaluar_postura(ang_cadera,  rangos["cadera"]["min"],  rangos["cadera"]["max"])

    dibujar_angulo_en_punto(frame, ang_rodilla, rodilla,
                            COLOR_VERDE if est_rodilla == "CORRECTA" else COLOR_ROJO)
    dibujar_angulo_en_punto(frame, ang_cadera, cadera,
                            COLOR_VERDE if est_cadera == "CORRECTA" else COLOR_ROJO)

    estados = [
        ("Rodilla", ang_rodilla, est_rodilla),
        ("Cadera",  ang_cadera,  est_cadera),
    ]
    return estados, all(e[2] == "CORRECTA" for e in estados)


def procesar_lagartija(frame, landmarks, w, h):
    ---comentario
    Evalua: angulo de codo   (hombro→codo→muñeca)
            angulo de hombro  (cadera→hombro→codo)
    Al bajar: codo ~90°, hombro 50°–90° (brazos no muy abiertos)
    ---comentario
    rangos = EJERCICIOS["Lagartija"]

    hombro = obtener_punto(landmarks, 11, w, h)
    codo   = obtener_punto(landmarks, 13, w, h)
    muneca = obtener_punto(landmarks, 15, w, h)
    cadera = obtener_punto(landmarks, 23, w, h)

    ang_codo   = calcular_angulo(hombro, codo, muneca)
    ang_hombro = calcular_angulo(cadera, hombro, codo)

    est_codo   = evaluar_postura(ang_codo,   rangos["codo"]["min"],   rangos["codo"]["max"])
    est_hombro = evaluar_postura(ang_hombro, rangos["hombro"]["min"], rangos["hombro"]["max"])

    dibujar_angulo_en_punto(frame, ang_codo, codo,
                            COLOR_VERDE if est_codo == "CORRECTA" else COLOR_ROJO)
    dibujar_angulo_en_punto(frame, ang_hombro, hombro,
                            COLOR_VERDE if est_hombro == "CORRECTA" else COLOR_ROJO)

    estados = [
        ("Codo",   ang_codo,   est_codo),
        ("Hombro", ang_hombro, est_hombro),
    ]
    return estados, all(e[2] == "CORRECTA" for e in estados)


def procesar_plancha(frame, landmarks, w, h):
    ---comentario
    Evalúa: ángulo de cadera  (hombro→cadera→rodilla)
            ángulo de tobillo (rodilla→tobillo→pie)
    Cuerpo recto: cadera 160°–180° (sin hundir ni elevar)
    ---comentario
    rangos = EJERCICIOS["Plancha"]

    hombro  = obtener_punto(landmarks, 11, w, h)
    cadera  = obtener_punto(landmarks, 23, w, h)
    rodilla = obtener_punto(landmarks, 25, w, h)
    tobillo = obtener_punto(landmarks, 27, w, h)

    ang_cadera  = calcular_angulo(hombro, cadera, rodilla)
    ang_tobillo = calcular_angulo(cadera, tobillo, rodilla)

    est_cadera  = evaluar_postura(ang_cadera,  rangos["cadera"]["min"],  rangos["cadera"]["max"])
    est_tobillo = evaluar_postura(ang_tobillo, rangos["tobillo"]["min"], rangos["tobillo"]["max"])

    dibujar_angulo_en_punto(frame, ang_cadera, cadera,
                            COLOR_VERDE if est_cadera == "CORRECTA" else COLOR_ROJO)
    dibujar_angulo_en_punto(frame, ang_tobillo, tobillo,
                            COLOR_VERDE if est_tobillo == "CORRECTA" else COLOR_ROJO)

    estados = [
        ("Cadera",  ang_cadera,  est_cadera),
        ("Tobillo", ang_tobillo, est_tobillo),
    ]
    return estados, all(e[2] == "CORRECTA" for e in estados)


def procesar_zancada(frame, landmarks, w, h):
    ---comentario
    Evalua: rodilla delantera (pierna izquierda): cadera→rodilla→tobillo
            rodilla trasera   (pierna derecha):   cadera→rodilla→tobillo
            cadera: hombro→cadera→rodilla (torso erguido, ~180°)
    Al bajar: ambas rodillas ~90°, torso vertical
    ---comentario
    rangos = EJERCICIOS["Zancada"]

    # Pierna izquierda
    cadera_izq  = obtener_punto(landmarks, 23, w, h)
    rodilla_izq = obtener_punto(landmarks, 25, w, h)
    tobillo_izq = obtener_punto(landmarks, 27, w, h)

    # Pierna derecha
    cadera_der  = obtener_punto(landmarks, 24, w, h)
    rodilla_der = obtener_punto(landmarks, 26, w, h)
    tobillo_der = obtener_punto(landmarks, 28, w, h)

    # Torso
    hombro_izq = obtener_punto(landmarks, 11, w, h)

    ang_rod_del = calcular_angulo(cadera_izq, rodilla_izq, tobillo_izq)
    ang_rod_tra = calcular_angulo(cadera_der, rodilla_der, tobillo_der)
    ang_cadera  = calcular_angulo(hombro_izq, cadera_izq, rodilla_izq)

    est_rod_del = evaluar_postura(ang_rod_del, rangos["rodilla_delantera"]["min"],
                                              rangos["rodilla_delantera"]["max"])
    est_rod_tra = evaluar_postura(ang_rod_tra, rangos["rodilla_trasera"]["min"],
                                              rangos["rodilla_trasera"]["max"])
    est_cadera  = evaluar_postura(ang_cadera,  rangos["cadera"]["min"],
                                              rangos["cadera"]["max"])

    dibujar_angulo_en_punto(frame, ang_rod_del, rodilla_izq,
                            COLOR_VERDE if est_rod_del == "CORRECTA" else COLOR_ROJO)
    dibujar_angulo_en_punto(frame, ang_rod_tra, rodilla_der,
                            COLOR_VERDE if est_rod_tra == "CORRECTA" else COLOR_ROJO)
    dibujar_angulo_en_punto(frame, ang_cadera, cadera_izq,
                            COLOR_VERDE if est_cadera == "CORRECTA" else COLOR_ROJO)

    estados = [
        ("Rodilla delantera", ang_rod_del, est_rod_del),
        ("Rodilla trasera",   ang_rod_tra, est_rod_tra),
        ("Cadera (torso)",    ang_cadera,  est_cadera),
    ]
    return estados, all(e[2] == "CORRECTA" for e in estados)


# Mapa de funciones por ejercicio
PROCESADORES = {
    "Sentadilla": procesar_sentadilla,
    "Lagartija":  procesar_lagartija,
    "Plancha":    procesar_plancha,
    "Zancada":    procesar_zancada,
}


# Captura de camara

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("No se pudo abrir la camara.")
    exit()


# Bucle principal
with mp_pose.Pose(
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
) as pose:

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        h, w = frame.shape[:2]

        # BGR → RGB para MediaPipe
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_rgb.flags.writeable = False
        resultados = pose.process(frame_rgb)
        frame_rgb.flags.writeable = True
        frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

        if resultados.pose_landmarks:
            landmarks = resultados.pose_landmarks.landmark

            # Dibujar esqueleto
            mp_dibujo.draw_landmarks(
                frame,
                resultados.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                mp_dibujo.DrawingSpec(color=(0, 200, 255), thickness=2, circle_radius=3),
                mp_dibujo.DrawingSpec(color=(0, 150, 200), thickness=2)
            )

            # Procesar el ejercicio actual y obtener estados
            estados, postura_ok = PROCESADORES[ejercicio_actual](frame, landmarks, w, h)

            # Panel lateral con angulos
            dibujar_panel(frame, estados, ejercicio_actual)

            # Mensaje principal en la parte baja
            mensaje = "POSTURA CORRECTA" if postura_ok else "CORRIGE TU POSTURA"
            dibujar_etiqueta(frame, mensaje,
                             (w // 2 - 130, h - 20),
                             COLOR_VERDE if postura_ok else COLOR_ROJO)

        else:
            cv2.putText(frame, "Sin persona detectada", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (100, 100, 100), 2)

        # Instrucciones de teclado si pos quitenselo
        dibujar_instrucciones(frame, h)

        cv2.imshow("Corrector de Postura - Calistenia", frame)


        tecla = cv2.waitKey(10) & 0xFF
        if tecla == ord('q'):
            break
        elif tecla == ord('1'):
            ejercicio_actual = "Sentadilla"
        elif tecla == ord('2'):
            ejercicio_actual = "Lagartija"
        elif tecla == ord('3'):
            ejercicio_actual = "Plancha"
        elif tecla == ord('4'):
            ejercicio_actual = "Zancada"

cap.release()
cv2.destroyAllWindows()
print("Sesión terminada.")
"""