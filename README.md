# 🏎️ DAKAR-KB: la BiblIA del DAKAR
BBDD con consultas sobre el rally Dakar

Este repositorio contiene el ecosistema completo de una aplicación diseñada para interactuar con modelos de lenguaje avanzados (LLM) proporcionando información técnica y general sobre el Rally Dakar, manteniendo la persistencia de datos y seguridad de usuarios.

**Ubicación del Proyecto:** `https://github.com/jonkar-diazperez/DAKAR-KB.git`

---

## 📝 Descripción
El proyecto consiste en una aplicación de IA que permite a los usuarios realizar consultas mediante lenguaje natural sobre datos históricos del rally Paris-Dakar. El sistema identifica si el usuario está registrado para ofrecer una experiencia personalizada, incluyendo el acceso a su histórico de consultas anteriores.

---

## 🚀 Tecnologías Utilizadas
* **Lenguaje:** ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
* **Frontend:** ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
* **Base de Datos:** ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
* **IA/LLM:** Groq Cloud API (openai/gpt-oss-120b)
* **Seguridad:** Hashing de contraseñas con `bcrypt`
* **Hosting cloud:** Render

---

## 🛠️ Características Principales
1.  **Gestión de Usuarios:** Sistema de registro e inicio de sesión seguro (las contraseñas nunca se almacenan en texto plano).
2.  **Modo Dual:**
    * **Home (Anónimo):** Pantalla de bienvenida con acceso a pruebas rápidas del LLM.
    * **Panel de Piloto (Registrado):** Interfaz personalizada con acceso al historial de chats.
3.  **Historial Persistente:** Cada consulta y respuesta se guarda en Postgres vinculada al ID del usuario.
4.  **Diseño Adaptativo:** Inyección de CSS dinámico para cambiar la estética según el estado de la sesión.

---

## 🔌 Estructura de la API
Los endpoints están desplegados en: `https://api-dakar.onrender.com`

| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `POST` | `/reg_user` | Registra un nuevo usuario (Hashing con bcrypt). |
| `POST` | `/log_user` | Valida credenciales y devuelve acceso. |
| `GET` | `/prompt_groq` | Envía una consulta al modelo LLM. |
| `POST` | `/insertar_prompt` | Guarda la pregunta y respuesta en la BD. |
| `GET` | `/lista_prompts` | Recupera los chats anteriores de un usuario. |

---

## 💾 Esquema de Base de Datos (Postgres)
El sistema utiliza dos tablas relacionadas para garantizar la integridad:

* **`usuarios`**: 
    * `id` (PK), `username` (Unique), `password_hash`.
* **`historial_chats`**: 
    * `id` (PK), `chat_session_id`, `user_id` (FK), `pregunta`, `respuesta`, `timestamp`.

---

## ⚙️ Instalación y Ejecución Local

1.  **Clonar o acceder al directorio:**
    ```bash
    cd "C:\DS REPO JCDP\DAKAR-KB"
    ```

2.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Ejecutar la aplicación:**
    ```bash
    streamlit run main.py
    ```

---

> **Nota:** El proyecto está configurado para conectar con una base de datos Postgres remota y los servicios de Groq a través de variables de entorno o parámetros configurados en el backend.

Desarrollado para el proyecto **DAKAR-KB** - Enero 2026.