import streamlit as st
import requests
import base64

# Configuración de la API
BASE_URL = "https://api-dakar.onrender.com"
#BASE_URL = "http://127.0.0.1:5000"


# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="BiblIA del Dakar", layout="wide")
def get_base64(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = f"""
    <style>
    .stApp {{
      background-image: url("data:image/png;base64,{bin_str}");
      background-size: cover;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)
    

# Inicializar estado de sesión
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'username' not in st.session_state:
    st.session_state.username = None

# --- FUNCIONES AUXILIARES ---
def login_usuario(username, password):
    url = f"{BASE_URL}/log_user"
    # Ajustado al formato que envías en tus tests
    payload = {"data": [username, password]}
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            res = response.json()
            # Asumimos que la API devuelve el ID si el login es correcto
            # Si tu API no devuelve el ID, tendrías que ajustarlo aquí
            if res.get('resultado') != False: 
                st.session_state.autenticado = True
                st.session_state.username = username
                # Aquí deberías obtener el ID real desde la respuesta si es posible
                st.session_state.user_id = res.get('user_id', 1) 
                return True
        return False
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return False

def registrar_usuario(username, password):
    url = f"{BASE_URL}/reg_user"
    payload = {"data": [username, password]}
    response = requests.post(url, json=payload)
    return response.status_code == 200 and response.json().get('resultado') == 'OK'

def consultar_llm(pregunta):
    url = f"{BASE_URL}/prompt_groq"
    payload = {"data": [pregunta]}
    response = requests.get(url, json=payload)
    if response.status_code == 200:
        return response.json().get('respuesta')
    return "Error al conectar con el LLM."

def guardar_chat(chat_id, user_id, pregunta, respuesta):
    url = f"{BASE_URL}/insertar_prompt"
    payload = {"data": [chat_id, user_id, pregunta, respuesta]}
    requests.post(url, json=payload)

def obtener_historial(user_id):
    url = f"{BASE_URL}/lista_prompts"
    payload = {"data": [user_id]}
    response = requests.get(url, json=payload)
   
    if response.status_code == 200:

        return response.json().get('chats',[])
    return []

# --- PANTALLA 1: MODO ANÓNIMO / HOME ---
def pantalla_anonima():
    set_background("static/home_dunas.jpg")
    st.title("🏎️ La BiblIA del DAKAR 🏎️", text_alignment="center" ,)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Login / Registro")
        tab1, tab2 = st.tabs(["Iniciar Sesión", "Registrarse"])
        
        with tab1:
            u = st.text_input("Usuario", key="login_u")
            p = st.text_input("Contraseña", type="password", key="login_p")
            if st.button("Entrar"):
                if login_usuario(u, p):
                    st.success(f"¡Bienvenido! {u}")
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas")
                    
        with tab2:
            reg_u = st.text_input("Nuevo Usuario", key="reg_u")
            reg_p = st.text_input("Nueva Contraseña", type="password", key="reg_p")
            if st.button("Crear Cuenta"):
                if registrar_usuario(reg_u, reg_p):
                    st.success("Usuario creado. Ahora puedes loguearte.")
                else:
                    st.error("No se pudo crear el usuario.")

    with col2:
        st.subheader("Haz una prueba haciéndonos una consulta")
        pregunta_test = st.text_input("Pregúntame:")
        if st.button("Consultar"):
            with st.spinner("Pensando..."):
                resp = consultar_llm(pregunta_test)
                st.write(f"**Respuesta:** {resp}")

# --- PANTALLA 2: MODO REGISTRADO ---
def pantalla_registrada():
    set_background("static/cars_dakar.jpg")
    st.title("🤖 Consulta de información del Rally DAKAR 🤖",)
    st.sidebar.title(f"Hola, {st.session_state.username}")
    
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.autenticado = False
        st.rerun()

    # Sidebar: Historial de chats
    st.sidebar.markdown("---")
    st.sidebar.subheader("Estas son tus consultas anteriores")
    historial = obtener_historial(st.session_state.user_id)
    print(len(historial))
    if len(historial) > 0:
        for chat in historial:
            
            # Mostramos la pregunta como título en el sidebar
            if st.sidebar.button(f"📄 {chat[2][:30]}...", key=f"chat_{chat[0]}"):
                st.info(f"**Pregunta:** {chat[2]}")
                st.success(f"**Respuesta:** {chat[3]}")

    # Cuerpo principal: Chat
    
    with st.form("chat_form", clear_on_submit=True):
        pregunta = st.text_area("¿Cúal es tu consulta?")
        enviado = st.form_submit_button("Preguntar")
        
        if enviado and pregunta:
            with st.spinner("Estamos procesando tu consulta..."):
                # 1. Llamar al LLM
                respuesta = consultar_llm(pregunta)
                
                # 2. Mostrar resultados
                st.write("**Respuesta:**")
                st.markdown(f"""
                                <div style="background-color: #1A1A1A; color: #FF9F00; padding: 15px; border-radius: 5px; border: 1px solid #FF9F00;">
                                    {respuesta}
                                </div>
                            """, unsafe_allow_html=True)
                
                # 3. Guardar en la base de datos
                # Usamos un ID de chat simple basado en el timestamp
                chat_id = f"Chat_{st.session_state.username}"
                guardar_chat(chat_id, st.session_state.user_id, pregunta, respuesta)
                #st.rerun() # Recargamos para que aparezca en el historial del sidebar

# --- LÓGICA DE NAVEGACIÓN ---
if st.session_state.autenticado:
    pantalla_registrada()
else:
    pantalla_anonima()