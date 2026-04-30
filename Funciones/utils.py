import numpy as np

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
    """
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
    """
    lm = landmarks[indice]
    return [int(lm.x * w), int(lm.y * h)]


def evaluar_postura(angulo, minimo, maximo):

    if minimo <= angulo <= maximo:
        return "Correcto"
    else:
        return "Incorrecto"
