import requests

def test_registro_endpoint():
    url = 'https://api-dakar.onrender.com/reg_user'  
    data = {'data': ["TEST_render", "0000"]}
    response = requests.post(url, json=data)
    assert response.status_code == 200
    assert response.json() == {'resultado': 'OK'}

def test_login_endpoint():
    url = 'https://api-dakar.onrender.com/log_user'  
    data = {'data': ["TEST", "0000"]} 
    response = requests.post(url, json=data)
    assert response.status_code == 200
    assert 'resultado' in response.json()

def test_groq_endpoint():
    url = 'https://api-dakar.onrender.com/prompt_groq'
    data = {'data': ["¿Cuando empezó a disputarse el Rally Dakar"]}   
    response = requests.get(url, json=data)
    assert response.status_code == 200
    assert 'respuesta' in response.json()
    
def test_insertar_endpoint():
    url = 'https://api-dakar.onrender.com/insertar_prompt'  
    data = {'data': ["CHAT TEST",1,"TEST Pregunta del chat","Respuesta del chat"]}   
    response = requests.post(url, json=data)
    assert response.status_code == 200
    assert 'estado' in response.json()
    
def test_lista_chats_endpoint():
    url = 'https://api-dakar.onrender.com/lista_prompts'  
    data = {'data': [1]}   
    response = requests.get(url, json=data)
    assert response.status_code == 200
    assert 'chats' in response.json()    
       