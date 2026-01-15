import requests

def test_registro_endpoint():
    url = 'http://localhost:5000/reg_user'  
    data = {'data': ["TEST", "0000"]}
    response = requests.post(url, json=data)
    assert response.status_code == 200
    assert response.json() == {'resultado': 'OK'}

def test_login_endpoint():
    url = 'http://localhost:5000/log_user'  
    data = {'data': ["TEST", "0000"]} 
    response = requests.post(url, json=data)
    assert response.status_code == 200
    assert 'resultado' in response.json()

def test_groq_endpoint():
    url = 'http://localhost:5000/prompt_groq'
    data = {'data': ["¿Cuando empezó a disputarse el Rally Dakar"]}   
    response = requests.get(url, json=data)
    assert response.status_code == 200
    assert 'respuesta' in response.json()
    
def test_insertar_endpoint():
    url = 'http://localhost:5000/insertar_prompt'  
    data = {'data': ["CHAT TEST",1,"TEST Pregunta del chat","Respuesta del chat"]}   
    response = requests.post(url, json=data)
    assert response.status_code == 200
    assert 'estado' in response.json()
    
def test_lista_chats_endpoint():
    url = 'http://localhost:5000/lista_prompts'  
    data = {'data': [0]}   
    response = requests.get(url, json=data)
    assert response.status_code == 200
    assert 'chats' in response.json()    
       