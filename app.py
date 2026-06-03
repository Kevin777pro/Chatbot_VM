import os
import json
import csv
import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import speech_recognition as sr

# Cargar variables de entorno
load_dotenv()

# Configurar cliente Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

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

# Función para analizar sentiment usando IA
def analyze_sentiment(text):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "Analiza el sentiment del siguiente texto y responde SOLO con una de estas palabras exactas: Positivo, Neutral, Negativo. No agregues explicaciones."},
                {"role": "user", "content": text}
            ],
            temperature=0.1,
            max_tokens=10
        )
        sentiment = response.choices[0].message.content.strip()
        return sentiment
    except:
        return "Neutral"

# Función para guardar log de conversación
def save_conversation_log(user_message, assistant_message, sentiment):
    log_entry = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user_message": user_message,
        "assistant_message": assistant_message,
        "sentiment": sentiment
    }
    st.session_state.conversation_logs.append(log_entry)
    st.session_state.sentiment_logs.append({
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "sentiment": sentiment
    })

# Función para guardar evaluación
def save_rating(rating, comment):
    rating_entry = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "rating": rating,
        "comment": comment
    }
    st.session_state.ratings.append(rating_entry)

# Función para verificar login administrativo
def verify_admin_password(password):
    admin_password = os.getenv("ADMIN_PASSWORD", "admin123")
    return password == admin_password

# Función para exportar logs a CSV
def export_logs_to_csv(logs, filename):
    if not logs:
        return None
    df = pd.DataFrame(logs)
    csv = df.to_csv(index=False)
    return csv

# Función para exportar logs a Excel
def export_logs_to_excel(logs, filename):
    if not logs:
        return None
    df = pd.DataFrame(logs)
    excel_buffer = pd.ExcelWriter(filename, engine='openpyxl')
    df.to_excel(excel_buffer, index=False, sheet_name='Datos')
    excel_buffer.close()
    return filename

# Función para generar dashboard DSS
def show_dss_dashboard():
    st.subheader("📊 Dashboard DSS - Decision Support System")
    
    if not st.session_state.conversation_logs:
        st.info("No hay datos de conversaciones aún. El dashboard se actualizará cuando haya interacciones.")
        return
    
    # Convertir logs a DataFrame
    df_conversations = pd.DataFrame(st.session_state.conversation_logs)
    df_sentiments = pd.DataFrame(st.session_state.sentiment_logs)
    df_ratings = pd.DataFrame(st.session_state.ratings) if st.session_state.ratings else pd.DataFrame()
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_conversations = len(st.session_state.conversation_logs)
        st.metric("Total Conversaciones", total_conversations)
    
    with col2:
        if df_sentiments.empty:
            avg_sentiment = 0
        else:
            sentiment_score = df_sentiments['sentiment'].map({'Positivo': 1, 'Neutral': 0, 'Negativo': -1})
            avg_sentiment = sentiment_score.mean()
        st.metric("sentiment Promedio", f"{avg_sentiment:.2f}")
    
    with col3:
        if df_ratings.empty:
            avg_rating = 0
        else:
            avg_rating = df_ratings['rating'].mean()
        st.metric("Satisfacción Promedio", f"{avg_rating:.1f}/5")
    
    with col4:
        st.metric("Productos Consultados", len(MOTOCICLETAS))
    
    st.markdown("---")
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("😊 Distribución de sentiments")
        if not df_sentiments.empty:
            sentiment_counts = df_sentiments['sentiment'].value_counts()
            fig_sentiment = px.pie(
                values=sentiment_counts.values,
                names=sentiment_counts.index,
                title="Distribución de sentiments",
                color_discrete_map={'Positivo': '#00CC96', 'Neutral': '#EF553B', 'Negativo': '#636EFA'}
            )
            st.plotly_chart(fig_sentiment, use_container_width=True)
        else:
            st.info("No hay datos de sentiments aún.")
    
    with col2:
        st.subheader("⭐ Distribución de Ratings")
        if not df_ratings.empty:
            rating_counts = df_ratings['rating'].value_counts().sort_index()
            fig_ratings = px.bar(
                x=rating_counts.index,
                y=rating_counts.values,
                title="Distribución de Ratings",
                labels={'x': 'Rating', 'y': 'Cantidad'}
            )
            st.plotly_chart(fig_ratings, use_container_width=True)
        else:
            st.info("No hay datos de ratings aún.")
    
    st.markdown("---")
    
    # Actividad por día
    st.subheader("📅 Actividad por Día")
    if not df_conversations.empty:
        df_conversations['timestamp'] = pd.to_datetime(df_conversations['timestamp'])
        df_conversations['date'] = df_conversations['timestamp'].dt.date
        activity_by_day = df_conversations.groupby('date').size().reset_index(name='count')
        fig_activity = px.line(
            activity_by_day,
            x='date',
            y='count',
            title="Actividad de Conversaciones por Día",
            markers=True
        )
        st.plotly_chart(fig_activity, use_container_width=True)
    else:
        st.info("No hay datos de actividad aún.")
    
    st.markdown("---")
    
    # Preguntas frecuentes
    st.subheader("❓ Preguntas Frecuentes")
    if not df_conversations.empty:
        user_messages = df_conversations['user_message'].tolist()
        # Contar palabras clave
        keywords = ['moto', 'precio', 'servicio', 'repuesto', 'mantenimiento', 'pago', 'horario']
        keyword_counts = {}
        for keyword in keywords:
            keyword_counts[keyword] = sum(1 for msg in user_messages if keyword.lower() in msg.lower())
        
        fig_keywords = px.bar(
            x=list(keyword_counts.keys()),
            y=list(keyword_counts.values()),
            title="Palabras Clave Más Frecuentes",
            labels={'x': 'Palabra Clave', 'y': 'Frecuencia'}
        )
        st.plotly_chart(fig_keywords, use_container_width=True)
    else:
        st.info("No hay datos de preguntas frecuentes aún.")

# Función para mostrar reportes
def show_reports():
    st.subheader("📄 Reportes Semanales")
    
    if not st.session_state.conversation_logs:
        st.info("No hay datos para generar reportes aún.")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Estadísticas Generales")
        st.metric("Total Conversaciones", len(st.session_state.conversation_logs))
        
        if st.session_state.sentiment_logs:
            sentiment_counts = {}
            for log in st.session_state.sentiment_logs:
                sentiment_counts[log['sentiment']] = sentiment_counts.get(log['sentiment'], 0) + 1
            
            st.write("**Distribución de sentiments:**")
            for sentiment, count in sentiment_counts.items():
                emoji = "😊" if sentiment == "Positivo" else "😐" if sentiment == "Neutral" else "😞"
                st.write(f"{emoji} {sentiment}: {count}")
        
        if st.session_state.ratings:
            avg_rating = sum(r['rating'] for r in st.session_state.ratings) / len(st.session_state.ratings)
            st.write(f"**Rating Promedio:** {avg_rating:.1f}/5 ⭐")
    
    with col2:
        st.subheader("💾 Exportar Datos")
        
        # Exportar conversaciones
        if st.button("📥 Exportar Conversaciones (CSV)"):
            csv_data = export_logs_to_csv(st.session_state.conversation_logs, "conversaciones.csv")
            if csv_data:
                st.download_button(
                    label="Descargar CSV",
                    data=csv_data,
                    file_name=f"conversaciones_{datetime.datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
        
        # Exportar sentiments
        if st.button("📥 Exportar sentiments (CSV)"):
            csv_data = export_logs_to_csv(st.session_state.sentiment_logs, "sentiments.csv")
            if csv_data:
                st.download_button(
                    label="Descargar CSV",
                    data=csv_data,
                    file_name=f"sentiments_{datetime.datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
        
        # Exportar ratings
        if st.button("📥 Exportar Ratings (CSV)"):
            csv_data = export_logs_to_csv(st.session_state.ratings, "ratings.csv")
            if csv_data:
                st.download_button(
                    label="Descargar CSV",
                    data=csv_data,
                    file_name=f"ratings_{datetime.datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
    
    st.markdown("---")
    
    # Tabla de conversaciones recientes
    st.subheader("📋 Últimas Conversaciones")
    if st.session_state.conversation_logs:
        df_recent = pd.DataFrame(st.session_state.conversation_logs[-10:])
        st.dataframe(df_recent, use_container_width=True)
    else:
        st.info("No hay conversaciones registradas.")

# Función para mostrar sistema de evaluación
def show_rating_system():
    st.subheader("⭐ Evalúa tu Experiencia")
    
    st.write("¿Cómo fue tu experiencia con el asistente virtual?")
    
    # Inicializar rating seleccionado en session_state
    if "selected_rating" not in st.session_state:
        st.session_state.selected_rating = None
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("1 ⭐", key="rating_1"):
            st.session_state.selected_rating = 1
            st.rerun()
    with col2:
        if st.button("2 ⭐⭐", key="rating_2"):
            st.session_state.selected_rating = 2
            st.rerun()
    with col3:
        if st.button("3 ⭐⭐⭐", key="rating_3"):
            st.session_state.selected_rating = 3
            st.rerun()
    with col4:
        if st.button("4 ⭐⭐⭐⭐", key="rating_4"):
            st.session_state.selected_rating = 4
            st.rerun()
    with col5:
        if st.button("5 ⭐⭐⭐⭐⭐", key="rating_5"):
            st.session_state.selected_rating = 5
            st.rerun()
    
    # Mostrar rating seleccionado
    if st.session_state.selected_rating:
        st.info(f"Rating seleccionado: {st.session_state.selected_rating} ⭐")
        comment = st.text_area("Comentario opcional:", placeholder="Cuéntanos más sobre tu experiencia...", key="rating_comment")
        
        col_submit, col_cancel = st.columns(2)
        with col_submit:
            if st.button("Enviar Evaluación", key="submit_rating"):
                save_rating(st.session_state.selected_rating, comment)
                st.session_state.selected_rating = None
                st.success("¡Gracias por tu evaluación! 🎉")
                st.rerun()
        with col_cancel:
            if st.button("Cancelar", key="cancel_rating"):
                st.session_state.selected_rating = None
                st.rerun()
    
    # Mostrar estadísticas de ratings
    if st.session_state.ratings:
        st.markdown("---")
        st.subheader("📊 Estadísticas de Evaluaciones")
        avg_rating = sum(r['rating'] for r in st.session_state.ratings) / len(st.session_state.ratings)
        st.metric("Rating Promedio", f"{avg_rating:.1f}/5 ⭐")
        st.write(f"Total de evaluaciones: {len(st.session_state.ratings)}")

# Función para mostrar login administrativo
def show_admin_login():
    st.subheader("🔐 Acceso Administrativo")
    
    password = st.text_input("Contraseña:", type="password")
    
    if st.button("Ingresar"):
        if verify_admin_password(password):
            st.session_state.is_admin = True
            st.success("✅ Acceso concedido")
            st.rerun()
        else:
            st.error("❌ Contraseña incorrecta")

# Función para generar respuesta del asistente
def generate_assistant_response(user_message):
    """Genera respuesta del asistente para un mensaje del usuario"""
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
        
        # Analizar sentiment del mensaje del usuario
        sentiment = analyze_sentiment(user_message)
        
        # Guardar log de conversación
        save_conversation_log(user_message, assistant_message, sentiment)
        
        # Agregar al historial
        st.session_state.messages.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        return assistant_message, sentiment
        
    except Exception as e:
        error_message = f"Lo siento, hubo un error al procesar tu mensaje. Por favor, intenta nuevamente o contacta a un asesor humano. Error: {str(e)}"
        st.session_state.messages.append({
            "role": "assistant",
            "content": error_message
        })
        return error_message, "Neutral"

# Función para mostrar panel administrativo
def show_admin_panel():
    st.subheader("🛡️ Panel Administrativo")
    
    # Navegación del panel admin
    admin_tabs = ["Dashboard DSS", "Reportes", "Logs", "Configuración"]
    selected_tab = st.tabs(admin_tabs)
    
    with selected_tab[0]:
        show_dss_dashboard()
    
    with selected_tab[1]:
        show_reports()
    
    with selected_tab[2]:
        st.subheader("📋 Logs del Sistema")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"**Conversaciones:** {len(st.session_state.conversation_logs)}")
        with col2:
            st.write(f"**sentiments:** {len(st.session_state.sentiment_logs)}")
        with col3:
            st.write(f"**Ratings:** {len(st.session_state.ratings)}")
        
        st.markdown("---")
        
        if st.session_state.conversation_logs:
            st.write("**Últimas 5 conversaciones:**")
            for log in st.session_state.conversation_logs[-5:]:
                st.text(f"📅 {log['timestamp']}")
                st.text(f"👤 Usuario: {log['user_message'][:50]}...")
                st.text(f"🤖 Asistente: {log['assistant_message'][:50]}...")
                st.text(f"😊 sentiment: {log['sentiment']}")
                st.markdown("---")
    
    with selected_tab[3]:
        st.subheader("⚙️ Configuración")
        st.info("Configuración del sistema administrativo")
        st.write("Variables de entorno configuradas:")
        st.code(f"GROQ_API_KEY: {'✅ Configurada' if os.getenv('GROQ_API_KEY') else '❌ No configurada'}")
        st.code(f"ADMIN_PASSWORD: {'✅ Configurada' if os.getenv('ADMIN_PASSWORD') else '❌ No configurada'}")
    
    if st.button("🚪 Cerrar Sesión"):
        st.session_state.is_admin = False
        st.session_state.current_page = "chat"
        st.success("Sesión cerrada")
        st.rerun()

# Inicializar session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "show_welcome" not in st.session_state:
    st.session_state.show_welcome = True

if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

if "conversation_logs" not in st.session_state:
    st.session_state.conversation_logs = []

if "sentiment_logs" not in st.session_state:
    st.session_state.sentiment_logs = []

if "ratings" not in st.session_state:
    st.session_state.ratings = []

if "current_page" not in st.session_state:
    st.session_state.current_page = "chat"

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
    
    # Navegación principal
    st.subheader("🧭 Navegación")
    
    if st.button("💬 Chat", use_container_width=True):
        st.session_state.current_page = "chat"
        st.rerun()
    
    if st.button("⭐ Evaluación", use_container_width=True):
        st.session_state.current_page = "rating"
        st.rerun()
    
    st.markdown("---")
    
    # Sección administrativa
    st.subheader("� Administración")
    
    if st.session_state.is_admin:
        if st.button("🛡️ Panel Admin", use_container_width=True):
            st.session_state.current_page = "admin"
            st.rerun()
    else:
        if st.button("🔐 Login Admin", use_container_width=True):
            st.session_state.current_page = "login"
            st.rerun()
    
    st.markdown("---")
    
    st.subheader("� Información")
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
        st.session_state.current_page = "chat"
        st.rerun()
    
    if st.button("🔧 Ver repuestos"):
        st.session_state.messages.append({
            "role": "assistant",
            "content": "¡Por supuesto! Estos son nuestros repuestos principales:\n\n" + "\n".join([f"• {r['nombre']} - ${r['precio']}" for r in REPUESTOS]) + "\n\n¿Necesitas algo específico para tu moto?"
        })
        st.session_state.current_page = "chat"
        st.rerun()
    
    if st.button("🛠️ Servicios"):
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Ofrecemos los siguientes servicios:\n\n" + "\n".join([f"• {s}" for s in SERVICIOS]) + "\n\n¿Te gustaría agendar un servicio?"
        })
        st.session_state.current_page = "chat"
        st.rerun()
    
    if st.button("💳 Métodos de pago"):
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"Aceptamos los siguientes métodos de pago:\n\n" + "\n".join([f"• {p}" for p in METODOS_PAGO]) + "\n\n¿Prefieres pagar en efectivo o transferencia?"
        })
        st.session_state.current_page = "chat"
        st.rerun()
    
    st.markdown("---")
    
    if st.button("🗑️ Limpiar chat"):
        st.session_state.messages = []
        st.session_state.show_welcome = True
        st.rerun()

# Título principal según página actual
page_titles = {
    "chat": "💬 Chat",
    "rating": "⭐ Evaluación",
    "login": "🔐 Login Administrativo",
    "admin": "🛡️ Panel Administrativo"
}

st.title(f"🏍️ VelozyMoto AI Assistant - {page_titles.get(st.session_state.current_page, 'Chat')}")
st.markdown("---")

# Lógica de navegación entre páginas
if st.session_state.current_page == "chat":
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
    
    # Verificar si PyAudio está instalado para mostrar botón de voz
    pyaudio_available = True
    try:
        import pyaudio
    except ImportError:
        pyaudio_available = False
    
    # Input del usuario con opción de voz
    # Botón de voz arriba del chat
    col_voice = st.columns([1, 4])
    with col_voice[0]:
        if pyaudio_available:
            if st.button("🎤", key="voice_button", help="Grabar mensaje de voz"):
                st.session_state.show_voice_recorder = True
                st.rerun()
        else:
            st.button("🎤", key="voice_button", help="PyAudio no instalado", disabled=True)
    with col_voice[1]:
        st.empty()
    
    # Input de chat estándar de Streamlit (soporta Enter para enviar)
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
                assistant_message, sentiment = generate_assistant_response(prompt)
                
                # Mostrar respuesta
                st.markdown(assistant_message)
                
                # Mostrar indicador de sentimiento
                emoji_sentiment = "😊" if sentiment == "Positivo" else "😐" if sentiment == "Neutral" else "😞"
                st.caption(f"{emoji_sentiment} Sentimiento detectado: {sentiment}")
    if st.session_state.get("show_voice_recorder", False):
        st.markdown("---")
        st.subheader("🎤 Grabar Mensaje de Voz")
        
        r = sr.Recognizer()
        
        col_mic, col_file, col_cancel = st.columns(3)
        
        with col_mic:
            use_mic = st.checkbox("🎤 Micrófono", value=True)
        
        with col_file:
            use_file = st.checkbox("📁 Archivo", value=False)
        
        with col_cancel:
            if st.button("❌ Cancelar", key="cancel_voice"):
                st.session_state.show_voice_recorder = False
                st.rerun()
        
        if use_mic and pyaudio_available:
            if st.button("🎙️ Grabar", key="record_in_chat"):
                try:
                    with st.spinner("Escuchando... Habla ahora"):
                        with sr.Microphone() as source:
                            r.adjust_for_ambient_noise(source, duration=1)
                            audio = r.listen(source, timeout=5, phrase_time_limit=10)
                            text = r.recognize_google(audio, language='es-ES')
                            
                            # Agregar mensaje del usuario
                            st.session_state.messages.append({
                                "role": "user",
                                "content": f"[Voz] {text}"
                            })
                            
                            # Generar respuesta
                            with st.chat_message("user"):
                                st.markdown(f"[Voz] {text}")
                            
                            with st.chat_message("assistant"):
                                with st.spinner("Generando respuesta..."):
                                    assistant_message, sentiment = generate_assistant_response(f"[Voz] {text}")
                                    st.markdown(assistant_message)
                                    emoji_sentiment = "😊" if sentiment == "Positivo" else "😐" if sentiment == "Neutral" else "😞"
                                    st.caption(f"{emoji_sentiment} Sentimiento detectado: {sentiment}")
                            
                            st.session_state.show_voice_recorder = False
                            st.rerun()
                            
                except sr.WaitTimeoutError:
                    st.error("⏱️ Tiempo de espera agotado")
                except sr.UnknownValueError:
                    st.error("❌ No se pudo entender el audio")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        
        elif use_file:
            audio_file = st.file_uploader("Sube archivo de audio", type=['wav', 'aiff', 'flac'], key="voice_file_upload")
            if audio_file and st.button("🔊 Procesar", key="process_in_chat"):
                try:
                    with st.spinner("Procesando audio..."):
                        with sr.AudioFile(audio_file) as source:
                            audio_data = r.record(source)
                        text = r.recognize_google(audio_data, language='es-ES')
                        
                        # Agregar mensaje del usuario
                        st.session_state.messages.append({
                            "role": "user",
                            "content": f"[Voz - Archivo] {text}"
                        })
                        
                        # Generar respuesta
                        with st.chat_message("user"):
                            st.markdown(f"[Voz - Archivo] {text}")
                        
                        with st.chat_message("assistant"):
                            with st.spinner("Generando respuesta..."):
                                assistant_message, sentiment = generate_assistant_response(f"[Voz - Archivo] {text}")
                                st.markdown(assistant_message)
                                emoji_sentiment = "😊" if sentiment == "Positivo" else "😐" if sentiment == "Neutral" else "😞"
                                st.caption(f"{emoji_sentiment} Sentimiento detectado: {sentiment}")
                        
                        st.session_state.show_voice_recorder = False
                        st.rerun()
                        
                except sr.UnknownValueError:
                    st.error("❌ No se pudo entender el audio")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

elif st.session_state.current_page == "rating":
    show_rating_system()

elif st.session_state.current_page == "login":
    show_admin_login()

elif st.session_state.current_page == "admin":
    if st.session_state.is_admin:
        show_admin_panel()
    else:
        st.error("❌ No tienes acceso administrativo")
        if st.button("Volver al Chat"):
            st.session_state.current_page = "chat"
            st.rerun()

# Footer
st.markdown("---")
st.markdown("💬 VelozyMoto AI Assistant - Potenciado por Inteligencia Artificial")





