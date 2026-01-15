from flask import Flask, request, jsonify
import pandas as pd
import groq_api as g
import bbdd_render as bd

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/", methods = ['GET'])
def main():
    return "API de DAKAR KB"

# 1. Llamada a GROQ para obtener respuesta a partir del prompt introducido por el usuario
@app.route("/prompt_groq", methods = ['GET'])
def prompt_groq():
    """{'data': ["Consulta usuario"]}"""
    try:
        pregunta = request.get_json()
        print(pregunta)
        if not pregunta or 'data' not in pregunta:
            return jsonify({"Error":"No se han proporcionado datos"}), 400

        pregunta = pregunta.get("data", None) 
        print("----------------------", pregunta)
        groq_r = g.groq_p(pregunta)
        
        print("*"*50, groq_r)
        #return jsonify(groq_r), 200
        return jsonify({"respuesta": f"{groq_r}"}), 200
    except ValueError:
        return jsonify({"Error":"No se han proporcionado datos válidos"}), 400   
    except Exception as e:
        return jsonify({"Error": f"Se ha producido un error ----- {e}:\nTipo: {type(e)=}"}), 500 

# 2. Insertar chat GROQ en BBDD
@app.route("/insertar_prompt", methods = ['POST'])
def insertar_prompt():
    try:
        """{'data': [
            "Título del chat",
            id_usuario,
            "Pregunta del chat",
            "Respuesta del chat"]}"""    
        chat_data = request.get_json()
        if not chat_data or 'data' not in chat_data:
            return jsonify({"Error":"No se han proporcionado datos"}), 400
        insert_est = bd.sql_insert_chat(chat_data["data"][0],chat_data["data"][1],chat_data["data"][2],chat_data["data"][3])
        print(insert_est)
        if insert_est == 'OK':
            print("Interacción guardada en el historial.")
            return jsonify({"respuesta": f"Chat guardado en el historial con id: {chat_data["data"][0]}",
                            "estado": insert_est}), 200
        else:
            return jsonify({"Error": f"Error al guardar en BBDD de chats"}), 400
    except ValueError:
        return jsonify({"Error":"No se han proporcionado datos válidos"}), 400   
    except Exception as e:
        return jsonify({"Error": f"Error al guardar en BBDD de chats: {e}\nTipo: {type(e)=}"}), 500 

# 3. Obtener conversaciones de un usuario de la BBDD
@app.route("/lista_prompts", methods = ['GET'])
def lista_prompts():
    try:
        """{'data': [
            id_usuario
            ]}"""    
        user_data = request.get_json()
        if not user_data or 'data' not in user_data:
            return jsonify({"Error":"No se han proporcionado datos"}), 400
        print(user_data["data"][0])
        chats_user = bd.sql_query_chats(user_data["data"][0])
        print(type(chats_user))
        #if type(chats_user) == "np.array" 
        return jsonify({"chats": chats_user}), 200
    except ValueError:
        return jsonify({"Error":"No se han proporcionado datos válidos"}), 400   
    except Exception as e:
        return jsonify({"Error": f"Error al consultar chats del usuario en BBDD: {e}\nTipo: {type(e)=}"}), 500 

# 4. Registrar usuario en BBDD
@app.route("/reg_user", methods = ['POST'])
def reg_user():
    try:
        """{'data': [
            "login_usuario",
            "clave_string"
            ]}"""    
        user_data = request.get_json()
        if not user_data or 'data' not in user_data:
            return jsonify({"Error":"No se han proporcionado datos"}), 400
        registro_status = bd.registrar_usuario(user_data["data"][0], user_data["data"][1])
        return jsonify({"resultado": registro_status}), 200
    except ValueError:
        return jsonify({"Error":"No se han proporcionado datos válidos"}), 400   
    except Exception as e:
        return jsonify({"Error": f"Error al registrar el usuario: {e}\nTipo: {type(e)=}"}), 500 

# 4. Validar login usuario
@app.route("/log_user", methods = ['POST'])
def log_user():
    try:
        """{'data': [
            "login_usuario",
            "clave_string"
            ]}"""    
        user_data = request.get_json()
        if not user_data or 'data' not in user_data:
            return jsonify({"Error":"No se han proporcionado datos"}), 400
        login_status, user_id = bd.verificar_login(user_data["data"][0], user_data["data"][1])
        return jsonify({"resultado": login_status,
                        "user_id": user_id}), 200
    except ValueError:
        return jsonify({"Error":"No se han proporcionado datos válidos"}), 400   
    except Exception as e:
        return jsonify({"Error": f"Error login del usuario: {e}\nTipo: {type(e)=}"}), 500 

app.run(host="0.0.0.0", port=5000)
