import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar cliente Groq
client = Groq(api_key=os.getenv("OPENAI_API_KEY"))

# Datos simulados del negocio
MOTOCICLETAS = [
    {
        "nombre": "Yamaha FZ",
        "precio": 2500,
        "descripcion": "Motocicleta deportiva con excelente rendimiento y diseño moderno. Ideal para ciudad y carretera.",
        "categoria": "deportiva"
    },
    {
        "nombre": "Honda CB125",
        "precio": 1800,
        "descripcion": "Motocicleta urbana compacta y eficiente. Perfecta para desplazamientos diarios.",
        "categoria": "urbana"
    },
    {
        "nombre": "Bajaj Pulsar",
        "precio": 2200,
        "descripcion": "Motocicleta deportiva con gran potencia y estilo agresivo. Ideal para jóvenes.",
        "categoria": "deportiva"
    },
    {
        "nombre": "Suzuki AX100",
        "precio": 1500,
        "descripcion": "Motocicleta económica y confiable. Bajo consumo de combustible.",
        "categoria": "economica"
    },
    {
        "nombre": "Kawasaki Ninja",
        "precio": 3200,
        "descripcion": "Motocicleta deportiva de alto rendimiento. Para los más exigentes.",
        "categoria": "deportiva"
    },
    {
        "nombre": "Honda CG125",
        "precio": 1600,
        "descripcion": "Motocicleta económica y robusta. Ideal para trabajo y transporte.",
        "categoria": "economica"
    }
]

REPUESTOS = [
    {
        "nombre": "Aceite Motul 10W40",
        "precio": 15,
        "compatibilidad": "Todas las motocicletas"
    },
    {
        "nombre": "Pastillas de freno delanteras",
        "precio": 25,
        "compatibilidad": "Yamaha, Honda, Bajaj"
    },
    {
        "nombre": "Batería de moto 12V",
        "precio": 45,
        "compatibilidad": "Todas las motocicletas"
    },
    {
        "nombre": "Filtro de aire",
        "precio": 12,
        "compatibilidad": "Honda, Suzuki"
    },
    {
        "nombre": "Cadena de transmisión",
        "precio": 35,
        "compatibilidad": "Todas las motocicletas"
    },
    {
        "nombre": "Bujía de encendido",
        "precio": 8,
        "compatibilidad": "Todas las motocicletas"
    },
    {
        "nombre": "Kit de luces LED",
        "precio": 30,
        "compatibilidad": "Todas las motocicletas"
    },
    {
        "nombre": "Espejos retrovisores",
        "precio": 18,
        "compatibilidad": "Yamaha, Honda, Bajaj, Suzuki"
    }
]

SERVICIOS = [
    "Cambio de aceite",
    "Ajuste de frenos",
    "Mantenimiento general",
    "Reparaciones básicas",
    "Cambio de pastillas",
    "Ajuste de cadena",
    "Revisión eléctrica",
    "Cambio de batería"
]

METODOS_PAGO = [
    "Efectivo",
    "Transferencia bancaria"
]

# System prompt del chatbot
SYSTEM_PROMPT = """Eres un asesor virtual de VelozyMoto, un negocio dedicado a la venta de motocicletas, repuestos y servicios de mantenimiento.

TU ROL:
- Actúas como vendedor y asistente de atención al cliente
- Siempre respondes en español
- Tono profesional, amigable y conversacional
- Usas emojis moderadamente
- Das respuestas cortas pero útiles
- NUNCA mencionas que eres una IA
- NUNCA sales del contexto del negocio de motocicletas

INFORMACIÓN DEL NEGOCIO:
- Productos: Motocicletas deportivas, urbanas, económicas, repuestos y accesorios
- Servicios: Cambio de aceite, ajuste de frenos, mantenimiento general, reparaciones básicas
- Métodos de pago: Efectivo, Transferencia bancaria
- Tiempo de entrega: 1 a 3 días dependiendo de la zona
- Horario: Lunes a sábado, 8:00 AM a 6:00 PM

DATOS DE MOTOCICLETAS:
""" + "\n".join([f"- {m['nombre']}: ${m['precio']} - {m['descripcion']} - Categoría: {m['categoria']}" for m in MOTOCICLETAS]) + """

DATOS DE REPUESTOS:
""" + "\n".join([f"- {r['nombre']}: ${r['precio']} - Compatible con: {r['compatibilidad']}" for r in REPUESTOS]) + """

SERVICIOS OFRECIDOS:
""" + ", ".join(SERVICIOS) + """

COMPORTAMIENTO:
1. Saluda siempre de forma amigable
2. Recomienda motocicletas según el presupuesto y necesidades del cliente
3. Recomienda repuestos según la moto del cliente
4. Proporciona información clara de productos (nombre, precio, descripción)
5. Simula cotizaciones cuando el cliente lo solicite
6. Simula agendamiento de servicios solicitando: nombre, tipo de servicio, fecha
7. Maneja objeciones como "está muy caro" ofreciendo alternativas o destacando valor
8. Si el cliente necesita ayuda compleja, ofrece escalar a un asesor humano
9. Mantén el contexto de la conversación
10. Sé natural y conversacional

EJEMPLOS DE RESPUESTAS:
- Cliente: "Busco una moto económica"
  Tú: "¡Claro! Tengo excelentes opciones económicas. La Suzuki AX100 cuesta $1500 y es muy eficiente. También la Honda CG125 por $1600, ideal para trabajo. ¿Cuál te interesa más?"

- Cliente: "Necesito frenos para una Pulsar"
  Tú: "Para tu Bajaj Pulsar, tengo pastillas de freno delanteras por $25. Son de alta calidad y compatibles con tu modelo. ¿Quieres que te prepare una cotización completa?"

- Cliente: "Está muy caro"
  Tú: "Entiendo tu preocupación. Nuestros productos tienen garantía de calidad y durabilidad. Además, ofrecemos facilidades de pago. ¿Te gustaría ver opciones más económicas o conocer nuestros servicios de mantenimiento?"

RECUERDA: Siempre mantén el rol de asesor humano, nunca digas que eres una IA."""

# Inicializar session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "show_welcome" not in st.session_state:
    st.session_state.show_welcome = True

# Configuración de la página
st.set_page_config(
    page_title="VelozyMoto AI Assistant",
    page_icon="🏍️",
    layout="wide"
)

# Sidebar con información del negocio
with st.sidebar:
    st.title("🏍️ VelozyMoto")
    st.markdown("---")
    
    st.subheader("📋 Información")
    st.markdown("""
    **Horario de atención:**
    Lunes a Sábado
    8:00 AM - 6:00 PM
    
    **Métodos de pago:**
    - Efectivo
    - Transferencia bancaria
    
    **Tiempo de entrega:**
    1 a 3 días (según zona)
    """)
    
    st.markdown("---")
    
    st.subheader("🚀 Acciones rápidas")
    
    if st.button("🏍️ Ver motocicletas"):
        st.session_state.messages.append({
            "role": "assistant",
            "content": "¡Claro! Estas son nuestras motocicletas disponibles:\n\n" + "\n".join([f"• {m['nombre']} - ${m['precio']} - {m['categoria']}" for m in MOTOCICLETAS]) + "\n\n¿Te interesa alguna en particular?"
        })
    
    if st.button("🔧 Ver repuestos"):
        st.session_state.messages.append({
            "role": "assistant",
            "content": "¡Por supuesto! Estos son nuestros repuestos principales:\n\n" + "\n".join([f"• {r['nombre']} - ${r['precio']}" for r in REPUESTOS]) + "\n\n¿Necesitas algo específico para tu moto?"
        })
    
    if st.button("🛠️ Servicios"):
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Ofrecemos los siguientes servicios:\n\n" + "\n".join([f"• {s}" for s in SERVICIOS]) + "\n\n¿Te gustaría agendar un servicio?"
        })
    
    if st.button("💳 Métodos de pago"):
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"Aceptamos los siguientes métodos de pago:\n\n" + "\n".join([f"• {p}" for p in METODOS_PAGO]) + "\n\n¿Prefieres pagar en efectivo o transferencia?"
        })
    
    st.markdown("---")
    
    if st.button("🗑️ Limpiar chat"):
        st.session_state.messages = []
        st.session_state.show_welcome = True
        st.rerun()

# Título principal
st.title("🏍️ VelozyMoto AI Assistant")
st.markdown("### Tu asesor virtual de confianza para motocicletas, repuestos y servicios")
st.markdown("---")

# Mostrar mensaje de bienvenida
if st.session_state.show_welcome and len(st.session_state.messages) == 0:
    welcome_message = "¡Hola! 👋 Bienvenido a VelozyMoto. Soy tu asesor virtual y estoy aquí para ayudarte con todo lo relacionado con motocicletas, repuestos y servicios. ¿En qué puedo asistirte hoy?"
    st.session_state.messages.append({
        "role": "assistant",
        "content": welcome_message
    })
    st.session_state.show_welcome = False

# Mostrar historial de chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input del usuario
if prompt := st.chat_input("Escribe tu mensaje aquí..."):
    # Agregar mensaje del usuario
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })
    
    # Mostrar mensaje del usuario
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generar respuesta del asistente
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                # Preparar mensajes para la API
                api_messages = [
                    {"role": "system", "content": SYSTEM_PROMPT}
                ]
                
                # Agregar historial de conversación (últimos 10 mensajes para mantener contexto)
                recent_messages = st.session_state.messages[-10:]
                api_messages.extend(recent_messages)
                
                # Llamada a la API
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=api_messages,
                    temperature=0.7,
                    max_tokens=500
                )
                
                assistant_message = response.choices[0].message.content
                
                # Mostrar respuesta
                st.markdown(assistant_message)
                
                # Agregar al historial
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": assistant_message
                })
                
            except Exception as e:
                error_message = f"Lo siento, hubo un error al procesar tu mensaje. Por favor, intenta nuevamente o contacta a un asesor humano. Error: {str(e)}"
                st.markdown(error_message)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_message
                })

# Footer
st.markdown("---")
st.markdown("💬 VelozyMoto AI Assistant - Potenciado por Inteligencia Artificial")
