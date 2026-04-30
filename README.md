# VectraPolinova

> Aplicación de escritorio para gestión de ejercicios y autenticación de usuarios desarrollada en Python con PyQt5.

## 📋 Descripción

VectraPolinova es una aplicación de escritorio construida con **PyQt5** que proporciona una interfaz gráfica moderna para la gestión de ejercicios físicos. El proyecto incluye un sistema de autenticación (login/registro) y una pantalla de selección de ejercicios con visualización de ejemplos en formato GIF.

## ✨ Características

- **Sistema de Autenticación**
  - Ventana de inicio de sesión (Login)
  - Ventana de registro de usuarios
  - Mostrar/ocultar contraseña con checkbox
  - Validación visual de campos

- **Interfaz Moderna**
  - Ventanas sin marco (Frameless Windows)
  - Personalización de barra de título con botones personalizados
  - Botones de minimizar, maximizar y cerrar
  - Arrastrar ventana desde cualquier punto
  - Redimensionar ventana con QSizeGrip
  - Transición suave entre estados normal/maximizado

- **Gestión de Ejercicios**
  - Pantalla de selección de ejercicios con imágenes
  - Visualización de ejemplos en formato GIF
  - Navegación entre ejercicios

- **Recursos Multimedia**
  - Carga de imágenes (PNG, JPG)
  - Reproducción de animaciones GIF
  - Iconos personalizados para controles de ventana

## 📁 Estructura del Proyecto

```
VectraPolinova/
├── didi.txt                          # Archivo de notas
├── interfaces/
│   ├── Login/
│   │   ├── login.py                  # Ventana de inicio de sesión
│   │   ├── login.ui                  # Diseño Qt Designer
│   │   ├── register.py               # Ventana de registro
│   │   ├── register.ui               # Diseño Qt Designer
│   │   └── images/
│   │       ├── resources.qrc         # Recursos Qt
│   │       ├── user.png              # Logo de usuario
│   │       ├── minimize.png          # Icono minimizar
│   │       ├── minimize_2.png         # Icono normal
│   │       ├── maximize.png          # Icono maximizar
│   │       └── exit.png              # Icono cerrar
│   │
│   └── Select_exercise/
│       ├── select_exercise.py        # Ventana de selección
│       ├── select_exercise.ui        # Diseño Qt Designer
│       ├── examples.py               # Ventana de ejemplos GIF
│       ├── examples.ui               # Diseño Qt Designer
│       ├── exercises/
│       │   ├── exercises.qrc         # Recursos de ejercicios
│       │   ├── lagartijas.jpg        # Imagen ejercicio
│       │   ├── sentadillas.jpg      # Imagen ejercicio
│       │   ├── plancha.jpg          # Imagen ejercicio
│       │   ├── zancadas.jpg         # Imagen ejercicio
│       │   ├── lagartijas.gif       # Animación ejemplo
│       │   ├── sentadilla.gif       # Animación ejemplo
│       │   ├── plancha.gif           # Animación ejemplo
│       │   └── zancada.gif          # Animación ejemplo
│       └── images/
│           └── interface_buttons.qrc # Recursos de interfaz
```

## 🛠️ Requisitos

- **Python 3.8+**
- **PyQt5** (versión 5.x)

### Dependencias

```
PyQt5>=5.15.0
```

## 📦 Instalación

1. **Clonar o descargar el proyecto**

2. **Crear un entorno virtual (recomendado)**

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate
   ```

3. **Instalar las dependencias**

   ```powershell
   pip install PyQt5
   ```

4. **Ejecutar la aplicación**

   ```powershell
   # Desde el directorio interfaces/Login
   python login.py

   # O desde interfaces/Select_exercise
   python select_exercise.py
   ```

## 🚀 Uso

### Ventana de Login

1. Ejecutar `login.py`
2. Ingresar credenciales
3. Marcar "Mostrar contraseña" para visualizar el texto
4. Click en "Regístrate" para abrir la ventana de registro

### Ventana de Registro

1. Ejecutar `register.py` o acceder desde Login
2. Completar los campos requeridos
3. Utilizar los controles de ventana personalizados

### Selección de Ejercicios

1. Ejecutar `select_exercise.py`
2. Seleccionar un ejercicio haciendo click en el botón correspondiente
3. Se abrirá una ventana con la animación GIF del ejercicio

### Controles de Ventana

| Botón | Acción |
|-------|--------|
| Minimizar | Reduce la ventana a la barra de tareas |
| Maximizar | Alterna entre tamaño normal y pantalla completa |
| Cerrar | Cierra la aplicación |
| Arrastrar | Mover la ventana desde cualquier punto del área superior |

## 🔧 Puntos a Mejorar

### Alta Prioridad

- [ ] **Sistema de autenticación funcional**
  - Implementar validación de credenciales contra base de datos
  - Hash de contraseñas (no almacenar en texto plano)
  - Sesiones de usuario

- [ ] **Gestión de base de datos**
  - Integrar SQLite u otra base de datos
  - CRUD completo para usuarios y ejercicios

- [ ] **Navegación entre ventanas**
  - Conectar Login → Select Exercise
  - Implementar cierre de sesión

### Media Prioridad

- [ ] **Manejo de errores**
  - Try/except en operaciones críticas
  - Mensajes de error amigables para el usuario
  - Logging de errores

- [ ] **Validación de datos**
  - Validar formato de email
  - Longitud mínima de contraseña
  - Campos obligatorios

- [ ] **Internationalization (i18n)**
  - Preparar strings para traducción
  - Soporte para múltiples idiomas

### Baja Prioridad

- [ ] **Mejoras visuales**
  - Animaciones de transición entre ventanas
  - Efectos hover en botones
  - Temas/oscuridad

- [ ] **Documentación de código**
  - Docstrings en todas las clases y métodos
  - Type hints para funciones

- [ ] **Testing**
  - Pruebas unitarias con pytest
  - Pruebas de integración

### Refactorizaciones Sugeridas

1. **Patrón MVC/MVP**
   - Separar lógica de presentación de negocio
   - Crear modelos para datos

2. **Código reutilizable**
   - Crear clase base `BaseWindow` para ventanas comunes
   - Extraer lógica de controles de ventana

3. **Recursos externos**
   - Mover rutas de imágenes a constantes o archivo de configuración
   - Usar rutas relativas absolutas

## 📄 Licencia

Este proyecto es con fines educativos.

## 👤 Autor

Proyecto desarrollado como parte de un aprendizaje en PyQt5.

---

*Última actualización: 29 de abril de 2026*