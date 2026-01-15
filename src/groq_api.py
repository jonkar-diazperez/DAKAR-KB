from groq import Groq
CLAVE_API = "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"

def groq_p(p):
    client = Groq(api_key=CLAVE_API)
    respuesta = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        #model="groq/compound",
        messages=[
        {
            "role": "system",
            "content": "Eres un experto en el Rally Paris-Dakar que tiene información de todas las ediciones que se han disputado desde su inicio en la edición de 1979 hasta la que está en curso en este año 2026.\nTienes información histórica de los participantes en cada edición, los vehículos que conducían, las categorías a las que pertenecen, la marca y sus características técnicas en cuanto a motor, tracción, dimensiones y, por supuesto, su posición en la clasificación en cada etapa. De cada vehículo tienes fotos para mostrar junto a la respuesta, si lo piden el usuario."
        },
        {
            "role": "assistant",
            "content": "Muéstra un resumen y una tabla con la respuesta a la pregunta y la foto principal. Si hay más información, pregúnta al usuario si quiere verla para mostrarla a continuación. No es necesario que incluyas las fuentes."
        },
        {
            "role": "user",
            "content": f"{p}"
        },

        ]
    )
    '''
        temperature=1,
        max_completion_tokens=8192,
        top_p=1,
        reasoning_effort="medium",
        stream=True,
        stop=None
        '''

    print(respuesta.choices[0].message.content)
    return respuesta.choices[0].message.content
'''
    for chunk in completion:
        print(chunk.choices[0].delta.content or "", end="")
'''