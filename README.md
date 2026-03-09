# Sistema de Gestión de Proyectos y Tareas

Aplicación de escritorio para la gestión de empleados, proyectos y tareas dentro de equipos de trabajo.

Este proyecto ha sido desarrollado como parte del **Trabajo de Fin de Grado del CFGS Desarrollo de Aplicaciones Multiplataforma (DAM)**.

La aplicación permite organizar el trabajo dentro de un equipo mediante la creación de proyectos, la división en tareas y su asignación a diferentes usuarios, permitiendo además realizar un seguimiento del progreso de cada proyecto.

---

# Descripción del proyecto

El sistema permite gestionar el trabajo dentro de un equipo mediante una plataforma que organiza proyectos, tareas y usuarios.

Cada proyecto puede dividirse en múltiples tareas que se asignan a diferentes miembros del equipo. Los usuarios pueden visualizar sus tareas, actualizar su estado y añadir comentarios para facilitar la comunicación y el seguimiento del trabajo.

El objetivo principal es ofrecer una herramienta sencilla que facilite:

* la organización del trabajo
* la asignación de responsabilidades
* el seguimiento del progreso de los proyectos

---

# Tecnologías utilizadas

| Componente           | Tecnología            |
| -------------------- | --------------------- |
| Lenguaje             | C#                    |
| Cliente              | WPF                   |
| Backend              | ASP.NET Core Web API  |
| Base de datos        | SQL Server            |
| ORM                  | Entity Framework Core |
| Control de versiones | Git                   |
| Repositorio          | GitHub                |
| IDE                  | Visual Studio 2022    |

Framework utilizado:

```
.NET 8 LTS
```

---

# Arquitectura del sistema

El proyecto sigue una arquitectura **cliente-servidor**.

```
Cliente WPF
     ↓
API REST (ASP.NET Core)
     ↓
Base de datos (SQL Server)
```

## Cliente WPF

Aplicación de escritorio encargada de la interfaz de usuario.

Funciones principales:

* mostrar proyectos y tareas
* gestión de usuarios
* visualización del progreso
* interacción con la API

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

Encargada del almacenamiento de la información del sistema.

Tablas principales:

* Usuarios
* Roles
* Proyectos
* Tareas
* Comentarios

---

# Funcionalidades principales

El sistema incluye las siguientes funcionalidades:

### Gestión de usuarios

* registro de usuarios
* inicio de sesión
* gestión de roles

### Gestión de proyectos

* creación de proyectos
* visualización del estado del proyecto
* seguimiento del progreso

### Gestión de tareas

* creación de tareas
* asignación a usuarios
* cambio de estado
* comentarios en tareas

### Seguimiento del trabajo

* panel de tareas asignadas
* filtros por estado
* visualización del progreso del proyecto

---

# Estructura del repositorio

```
/src
 ├── Cliente.Wpf
 ├── Api
 ├── Dominio
 ├── Infraestructura

/tests
 ├── Api.Tests

/docs
 ├── arquitectura
 ├── flujo-trabajo
 ├── base-datos
```

---

# Instalación del proyecto

## Requisitos

* Visual Studio 2022
* .NET 8 SDK
* SQL Server (Express o Developer)

---

## Clonar el repositorio

```bash
git clone https://github.com/usuario/proyecto-tfg.git
```

Entrar en el directorio del proyecto:

```bash
cd proyecto-tfg
```

---

# Configuración de la base de datos

1. Crear una base de datos en SQL Server
2. Configurar la cadena de conexión en el archivo:

```
appsettings.json
```

Ejemplo:

```
"ConnectionStrings": {
 "DefaultConnection": "Server=localhost;Database=GestionTareas;Trusted_Connection=True;"
}
```

---

# Ejecutar la API

1. Abrir la solución en Visual Studio
2. Seleccionar el proyecto **Api**
3. Ejecutar el proyecto

La API quedará disponible en:

```
https://localhost:xxxx
```

Swagger estará disponible en:

```
/swagger
```

---

# Ejecutar el cliente WPF

1. Seleccionar el proyecto **Cliente.Wpf**
2. Ejecutar el proyecto desde Visual Studio

La aplicación se conectará a la API para obtener los datos.

---

# Flujo de trabajo del proyecto

El proyecto utiliza un flujo de desarrollo basado en **Git Flow simplificado**.

Ramas principales:

```
main
develop
```

Ramas de trabajo:

```
feature/*
fix/*
docs/*
release/*
hotfix/*
```

El flujo de desarrollo es el siguiente:

1. Crear rama desde `develop`
2. Implementar funcionalidad
3. Realizar commits organizados
4. Subir la rama
5. Crear Pull Request
6. Revisar cambios
7. Fusionar en `develop`

---

# Convención de commits

Formato utilizado:

```
tipo(ámbito): descripción
```

Ejemplos:

```
feat(api): crear endpoint de login
feat(wpf): crear pantalla de tareas
fix(api): corregir validación de credenciales
docs(readme): añadir instrucciones de instalación
```

---

# Documentación

La documentación del proyecto se encuentra en la carpeta:

```
/docs
```

Incluye:

* arquitectura del sistema
* flujo de trabajo
* modelo de base de datos
* documentación técnica

---

# Autores

Proyecto desarrollado por estudiantes del CFGS **Desarrollo de Aplicaciones Multiplataforma (DAM)**.

Integrantes del proyecto:

* Nombre del estudiante
* Nombre del estudiante

---

# Licencia

Proyecto desarrollado con fines académicos.
