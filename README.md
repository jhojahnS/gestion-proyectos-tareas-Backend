# Sistema de Gestión de Proyectos y Tareas

Aplicación de escritorio para la gestión de empleados, proyectos y tareas dentro de equipos de trabajo.

Este proyecto se desarrolla como parte del **Trabajo de Fin de Grado del CFGS Desarrollo de Aplicaciones Multiplataforma (DAM)**.

El sistema permite organizar proyectos de trabajo, dividirlos en tareas y asignarlos a diferentes usuarios según su rol dentro del sistema.

---

# Descripción del proyecto

La aplicación permite gestionar el trabajo dentro de un equipo mediante una plataforma que organiza proyectos, tareas y usuarios.

Cada proyecto puede dividirse en múltiples tareas que se asignan a distintos miembros del equipo. Los usuarios pueden consultar sus tareas, actualizar su estado y añadir comentarios para facilitar el seguimiento del trabajo.

El objetivo del sistema es facilitar:

* la organización del trabajo
* la distribución de responsabilidades
* el seguimiento del progreso de los proyectos
* la comunicación entre miembros del equipo

---

# Tecnologías utilizadas

| Componente           | Tecnología |
| -------------------- | ---------- |
| Cliente              | WPF        |
| Lenguaje cliente     | C#         |
| Backend              | Python     |
| Framework API        | FastAPI    |
| Base de datos        | SQL        |
| ORM                  | SQLAlchemy |
| Control de versiones | Git        |
| Repositorio          | GitHub     |

---

# Arquitectura del sistema

El proyecto sigue una arquitectura **cliente-servidor**.

```text
Cliente WPF (C#)
        ↓ HTTP / JSON
API REST (FastAPI - Python)
        ↓
Base de datos SQL
```

## Cliente WPF

Aplicación de escritorio encargada de la interfaz de usuario.

Responsabilidades principales:

* mostrar proyectos y tareas
* gestión de usuarios
* visualización del progreso
* comunicación con la API mediante HTTP

---

## API REST

La API gestiona la lógica de negocio del sistema.

Responsabilidades:

* autenticación de usuarios
* gestión de proyectos
* gestión de tareas
* validación de datos
* acceso a la base de datos

---

## Base de datos

Encargada de almacenar la información del sistema.

Tablas principales:

* Usuarios
* Roles
* Proyectos
* Tareas
* Comentarios

---

# Estructura del repositorio

```text
gestion-proyectos-tareas
│
├── README.md
│
├── api-python
│   ├── app
│   │   ├── routers
│   │   ├── models
│   │   ├── schemas
│   │   ├── services
│   │   └── main.py
│   │
│   └── requirements.txt
│
├── cliente-wpf
│   ├── Cliente.Wpf.sln
│   └── Cliente.Wpf
│
├── docs
│
└── tests
```

---

# Instalación del proyecto

## Requisitos

* Python 3.10 o superior
* Visual Studio 2022
* .NET 8
* Base de datos SQL
* Git

---

# Ejecutar la API

Entrar en la carpeta de la API:

```bash
cd api-python
```

Crear entorno virtual:

```bash
python -m venv venv
```

Activar entorno:

Windows

```bash
venv\Scripts\activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Ejecutar la API:

```bash
uvicorn app.main:app --reload
```

La API estará disponible en:

```
http://localhost:8000
```

Documentación automática de la API:

```
http://localhost:8000/docs
```

---

# Ejecutar el cliente WPF

1. Abrir **Visual Studio**
2. Abrir la solución:

```
cliente-wpf/Cliente.Wpf.sln
```

3. Ejecutar el proyecto

La aplicación se conectará a la API para obtener los datos.

---

# Funcionalidades principales

El sistema incluye las siguientes funcionalidades:

## Gestión de usuarios

* registro de usuarios
* inicio de sesión
* gestión de roles

## Gestión de proyectos

* creación de proyectos
* visualización de proyectos
* seguimiento del progreso

## Gestión de tareas

* creación de tareas
* asignación de tareas a usuarios
* cambio de estado
* comentarios en tareas

---

# Flujo de trabajo del proyecto

El proyecto utiliza un flujo de trabajo basado en **Git Flow simplificado**.

Ramas principales:

```
main
develop
```

Ramas de desarrollo:

```
feature/*
fix/*
docs/*
release/*
hotfix/*
```

Flujo de trabajo:

1. Crear rama desde `develop`
2. Desarrollar funcionalidad
3. Realizar commits organizados
4. Subir cambios
5. Crear Pull Request
6. Revisar código
7. Fusionar en `develop`

---

# Convención de commits

Formato utilizado:

```
tipo(ambito): descripción
```

Ejemplos:

```
feat(api): crear endpoint de login
feat(wpf): crear pantalla de tareas
fix(api): corregir validación de credenciales
docs(readme): añadir guía de instalación
```

---

# Documentación

La documentación técnica del proyecto se encuentra en la carpeta:

```
/docs
```

Incluye:

* arquitectura del sistema
* modelo de base de datos
* flujo de trabajo
* análisis del sistema

---

# Autores

* Jhojahn Sebastian Ramirez Marin
* Irene Gomez Cañada

---

