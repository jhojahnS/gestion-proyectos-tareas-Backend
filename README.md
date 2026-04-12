# API - Sistema de Gestión de Proyectos y Tareas

API REST para la gestión de usuarios, proyectos y tareas dentro de equipos de trabajo.

Este proyecto se desarrolla como parte del **Trabajo de Fin de Grado del CFGS Desarrollo de Aplicaciones Multiplataforma (DAM)**.

**Este repositorio contiene únicamente el BACKEND del sistema.**  
El cliente (WPF) se encuentra en un repositorio independiente.

---

# Descripción del proyecto

La API permite gestionar el trabajo dentro de un equipo mediante una plataforma que organiza proyectos, tareas y usuarios.

Cada proyecto puede dividirse en múltiples tareas que se asignan a distintos miembros del equipo. Los usuarios pueden consultar sus tareas, actualizar su estado y añadir comentarios para facilitar el seguimiento del trabajo.

El objetivo del sistema es facilitar:

* la organización del trabajo  
* la distribución de responsabilidades  
* el seguimiento del progreso de los proyectos  
* la comunicación entre miembros del equipo  

---

# Tecnologías utilizadas

| Componente           | Tecnología |
|--------------------|----------|
| Backend            | Python     |
| Framework API      | FastAPI    |
| Base de datos      | SQL        |
| ORM                | SQLAlchemy |
| Control versiones  | Git        |
| Repositorio        | GitHub     |

---

# Arquitectura del sistema

El proyecto sigue una arquitectura **cliente-servidor**.

<img width="381" height="521" alt="image" src="https://github.com/user-attachments/assets/7edfa4bb-a716-409b-858d-76d5d87f3229" />

---

## API REST

La API gestiona la lógica de negocio del sistema.
Responsabilidades:

* autenticación de usuarios
* gestión de proyectos
* gestión de tareas
* validación de datos
* acceso a la base de datos

## Base de datos

Encargada de almacenar la información del sistema.
Tablas principales:

* Usuarios
* Roles
* Proyectos
* Tareas
* Comentarios

# Estructura del repositorio

```
gestion-proyectos-tareas-backend
│
├── .github/workflows
├── app
│   ├── routers
│   ├── models
│   ├── schemas
│   ├── services
│   └── main.py
│
├── Dockerfile
├── main.py
├── requirements.txt
└── README.md
```
# Instalación del proyecto

## Requisitos

*Python 3.14 
*Base de datos SQL
*Git

# Ejecutar la API

Clonar el repositorio:
```text
git clone https://github.com/jhojahnS/gestion-proyectos-tareas-Backend.git
cd gestion-proyectos-tareas-Backend
```

Crear entorno virtual:
```text
python -m venv venv
```
Activar entorno:
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
Documentación automática:
```
http://localhost:8000/docs
```
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

Gestión de tareas

* creación de tareas
* asignación de tareas a usuarios
* cambio de estado
* comentarios en tareas
---
# Flujo de trabajo del proyecto

El proyecto utiliza un flujo de trabajo basado en **Git Flow simplificado**.

## Ramas principales
```
main
develop
````

main: contiene versiones estables
Rama protegida
No se permiten commits directos

develop: rama de integración
Rama protegida
No se trabaja directamente
Solo recibe cambios mediante Pull Request

## Ramas de trabajo

```
feature/*
fix/*
hotfix/*
docs/*
```
Ejemplos

```
feature/api-login
feature/gestion-proyectos
fix/error-login
hotfix/login-error
docs/readme
```

## Flujo de desarrollo

Actualizar la rama develop
```bash
git checkout develop
git pull origin develop
```
Crear rama de trabajo
```bash
git checkout -b feature/nombre-funcionalidad
```
Desarrollar funcionalidad nueva y realizar commits organizados
```bash
git add .
git commit -m "feat(api): crear endpoint"
```
Subir rama
```bash
git push -u origin feature/nombre-funcionalidad
```
Crear Pull Request
Se revisara código y si esta todo correcto se integraran los cambios en develop

## Estrategia de merge

Se utiliza rebase para mantener un historial limpio.
Actualizar develop:
```bash
git checkout develop
git pull origin develop
```
Volver a la rama:
```bash
git checkout feature/nombre-funcionalidad
```
Rebase:
```bash
git rebase develop
```
Resolver conflictos:
```bash
git add .
git rebase --continue
```
Abortar rebase en caso de que sea necesario:
```bash
git rebase --abort
```
## Convención de commits
Formato utilizado:
```
tipo(ambito): descripción
```
Tipos
```
feat → nueva funcionalidad
fix → corrección de errores
docs → documentación
refactor → mejora de código
style → cambios visuales
```

Ejemplos correctos
feat(api): crear endpoint de login
fix(api): corregir validación
docs(readme): añadir instalación

Ejemplos incorrectos
cambios
arreglos
subo todo

## Pull Requests

Toda integración se realiza mediante Pull Request.
Debe incluir:

* descripción clara
* cambios realizados
* como probar la funcionalidad

## Documentación
La documentación técnica se encuentra en:
/docs
Incluye:

* arquitectura del sistema
* modelo de base de datos
* flujo de trabajo
* análisis del sistema

# Integración continua (CI) con GitHub Actions

El proyecto incorpora un sistema de integración continua (CI) mediante **GitHub Actions**, que permite automatizar la verificación del backend en cada cambio realizado en el repositorio.

## Objetivo

El objetivo del pipeline es garantizar que el código:

- Cumple unos estándares mínimos de calidad
- No contiene errores de sintaxis
- Puede ser construido correctamente como imagen Docker

Este proceso se ejecuta automáticamente en cada **Pull Request** y en cada **push** a las ramas principales.

---

## Ejecución del pipeline

El workflow se ejecuta en los siguientes casos:

- Al realizar un **push** en las ramas:
  - `main`
  - `develop`

- Al crear o actualizar una **Pull Request** hacia:
  - `main`
  - `develop`

---

## Etapas del pipeline

El pipeline está compuesto por las siguientes fases:

### 1. Descarga del repositorio

Se obtiene el código fuente del repositorio en la máquina virtual de GitHub Actions.

---

### 2. Configuración del entorno

- Se instala **Python 3.14**
- Se actualiza `pip`
- Se instalan las dependencias del proyecto definidas en `requirements.txt`

---

### 3. Chequeo de calidad del codigo (Lint)

Se ejecuta un análisis estático del código utilizando con `flake8`, que permite detectar:

- Errores de sintaxis
- Problemas de estilo
- Variables no utilizadas
- Posibles malas prácticas

Este paso ayuda a mantener un código limpio y consistente.

---

### 4. Verificación básica del proyecto

Se ejecuta el siguiente comando:

```bash
python -m compileall .
```
Este proceso comprueba que todos los archivos Python del proyecto:
* Son sintácticamente correctos
* Pueden ser compilados sin errores

### 5. Construcción de la imagen Docker

Se construye una imagen Docker del backend mediante:
```bash 
docker build -t backend-api .
``` 
Este paso verifica que:

* El Dockerfile es correcto
* El proyecto puede ser empaquetado correctamente
* El backend es desplegable en un entorno containerizado

### Beneficios

La integración de este pipeline permite:

* Detectar errores automáticamente antes de integrar cambios
* Mejorar la calidad del código
* Evitar que código defectuoso llegue a producción
* Garantizar que el proyecto es desplegable mediante Docker
* Seguir buenas prácticas utilizadas en entornos profesionales

## Autores

* Jhojahn Sebastian Ramirez Marin
* Irene Gomez Cañada
