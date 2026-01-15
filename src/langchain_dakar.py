from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import HumanMessage, SystemMessage

api_key = "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"

llm = ChatGroq(
    model="meta-llama/llama-4-maverick-17b-128e-instruct", 
    temperature=0.3,
    groq_api_key=api_key
)

prompt = ChatPromptTemplate.from_messages([
    ("system", """Eres un profesor de un bootcamp de ciencia de datos. quiero que me ayudes
            en problemas técnicos, tanto en conceptos como en programación. Quiero que siempre que me
            respondas sea ayudándome. No dandome la solución"""),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}"),
])

chain = prompt | llm

chat_historial = ChatMessageHistory()

cadena_historial = RunnableWithMessageHistory(
    chain,
    lambda session_id: chat_historial,
    input_messages_key="input",
    history_messages_key="history",
)

print("Aula Virtual de Data Science (escribe 'salir' para terminar)\n")

while True:
    user_input = input("Alumno: ")
    if user_input.lower() in ["salir", "exit"]:
        break
    
    # Invocamos la cadena pasando un config con el session_id
    response = cadena_historial.invoke(
        {"input": user_input},
        config={"configurable": {"session_id": "bootcamp_01"}}
    )
    
    print(f"\nProfe: {response.content}\n")