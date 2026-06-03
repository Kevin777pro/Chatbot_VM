# 🏍️ VelozyMoto AI Assistant

Un chatbot inteligente para la atención al cliente de VelozyMoto, negocio dedicado a la venta de motocicletas, repuestos y servicios de mantenimiento.

## 📋 Descripción del Proyecto

VelozyMoto AI Assistant es un sistema de chatbot conversacional que automatiza la atención al cliente utilizando inteligencia artificial. El chatbot actúa como un asesor virtual capaz de:

- Responder consultas automáticamente sobre motocicletas, repuestos y servicios
- Recomendar productos según las necesidades del cliente
- Simular cotizaciones y agendamiento de servicios
- Brindar información sobre horarios, métodos de pago y tiempos de entrega
- Manejar objeciones y escalar conversaciones cuando es necesario

## 🎯 Características Principales

- **Interfaz moderna y limpia** con Streamlit
- **Chat interactivo** con historial persistente
- **Respuestas en español** con tono profesional y amigable
- **Datos simulados** de motocicletas y repuestos
- **Botones rápidos** para acciones comunes
- **Sidebar informativo** con datos del negocio
- **Indicador de carga** mientras el chatbot responde
- **Botón para limpiar chat**

### 🆕 Funcionalidades Avanzadas

- **🔒 Panel Administrativo Seguro**: Acceso protegido por contraseña para gestión avanzada
- **😊 Análisis de Sentimientos**: Detección automática del sentimiento del usuario en cada mensaje
- **📊 Dashboard DSS**: Sistema de soporte a decisiones con métricas y visualizaciones
- **📈 Métricas y Estadísticas**: Análisis de conversaciones, satisfacción y actividad
- **📄 Reportes Semanales**: Generación automática de reportes con exportación CSV
- **⭐ Sistema de Evaluación**: Calificación del chatbot por parte de los usuarios
- **🎤 Interacción por Voz**: Simulación de atención telefónica inteligente

## 🛠️ Tecnologías Utilizadas

- **Python**: Lenguaje de programación principal
- **Streamlit**: Framework para la interfaz web
- **Groq API**: Modelo llama-3.1-8b-instant para respuestas inteligentes
- **python-dotenv**: Gestión de variables de entorno
- **pandas**: Manipulación y análisis de datos
- **plotly**: Visualizaciones interactivas
- **speechrecognition**: Reconocimiento de voz (simulado)

## 📦 Instalación

### 1. Clonar o descargar el proyecto

Asegúrate de tener los archivos del proyecto en tu directorio de trabajo.

### 2. Crear entorno virtual (recomendado)

```bash
python -m venv venv
```

### 3. Activar el entorno virtual

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

## ⚙️ Configuración

### 1. Configurar API Key de Groq

Crea un archivo `.env` en la raíz del proyecto basándote en el archivo `.env.example`:

```bash
cp .env.example .env
```

Edita el archivo `.env` y agrega tus credenciales:

```
GROQ_API_KEY=gsk-your-actual-groq-api-key-here
ADMIN_PASSWORD=your_admin_password_here
```

**Nota:** 
- Para obtener una API Key de Groq, visita [https://console.groq.com/keys](https://console.groq.com/keys)
- La contraseña de administración es opcional. Si no se configura, usa `admin123` por defecto

## ▶️ Ejecución

Una vez configurado todo, ejecuta la aplicación con Streamlit:

```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

## 📱 Uso de la Aplicación

### Interfaz Principal

- **Título**: "🏍️ VelozyMoto AI Assistant"
- **Chat interactivo**: Escribe tus preguntas y recibe respuestas del asistente virtual
- **Historial persistente**: La conversación se mantiene mientras uses la aplicación

### Sidebar

- **🧭 Navegación**:
  - 💬 Chat: Interfaz principal de conversación
  - 🎤 Voz: Simulación de interacción por voz
  - ⭐ Evaluación: Sistema de calificación del chatbot
  - 🔐 Login Admin: Acceso al panel administrativo

- **Información del negocio**: Horarios, métodos de pago, tiempos de entrega
- **Botones rápidos**:
  - 🏍️ Ver motocicletas
  - 🔧 Ver repuestos
  - 🛠️ Servicios
  - 💳 Métodos de pago
- **Limpiar chat**: Reinicia la conversación

### Funcionalidades del Chatbot

El chatbot puede:

1. **Saludar al usuario** de forma amigable
2. **Recomendar motocicletas** según presupuesto y necesidades
3. **Recomendar repuestos** según el modelo de moto
4. **Informar sobre servicios** de mantenimiento
5. **Simular cotizaciones** de productos
6. **Simular agendamiento** de servicios (solicita nombre, tipo de servicio, fecha)
7. **Manejar objeciones** como "está muy caro"
8. **Escalar conversación** a un asesor humano cuando es necesario

### Ejemplos de Consultas

- "Busco una moto económica"
- "Necesito frenos para una Pulsar"
- "¿Qué servicios ofrecen?"
- "¿Cuáles son sus horarios?"
- "¿Cómo puedo pagar?"
- "Quiero agendar un mantenimiento"

## 🏍️ Datos del Negocio

### Motocicletas Disponibles

- Yamaha FZ - $2500 - Deportiva
- Honda CB125 - $1800 - Urbana
- Bajaj Pulsar - $2200 - Deportiva
- Suzuki AX100 - $1500 - Económica
- Kawasaki Ninja - $3200 - Deportiva
- Honda CG125 - $1600 - Económica

### Repuestos Principales

- Aceite Motul 10W40 - $15
- Pastillas de freno delanteras - $25
- Batería de moto 12V - $45
- Filtro de aire - $12
- Cadena de transmisión - $35
- Bujía de encendido - $8
- Kit de luces LED - $30
- Espejos retrovisores - $18

### Servicios Ofrecidos

- Cambio de aceite
- Ajuste de frenos
- Mantenimiento general
- Reparaciones básicas
- Cambio de pastillas
- Ajuste de cadena
- Revisión eléctrica
- Cambio de batería

### Información Adicional

- **Horario**: Lunes a sábado, 8:00 AM a 6:00 PM
- **Métodos de pago**: Efectivo, Transferencia bancaria
- **Tiempo de entrega**: 1 a 3 días según zona

## 🎨 Captura Esperada del Sistema

La aplicación presenta:

1. **Header** con título y subtítulo
2. **Sidebar izquierdo** con información del negocio y botones rápidos
3. **Área de chat** central con:
   - Mensaje de bienvenida automático
   - Burbujas de chat para usuario y asistente
   - Input de texto en la parte inferior
4. **Diseño moderno** con separación visual clara
5. **Iconos y emojis** moderados para mejor experiencia

## 📁 Estructura del Proyecto

```
ChatbotVM/
├── app.py              # Aplicación principal de Streamlit
├── requirements.txt    # Dependencias del proyecto
├── .env.example        # Plantilla de variables de entorno
├── .env               # Variables de entorno (crear este archivo)
└── README.md          # Documentación del proyecto
```

## 🔒 Seguridad

- **NO** hardcodear la API Key en el código
- **SIEMPRE** usar variables de entorno
- **NUNCA** compartir el archivo `.env` con tu API Key
- Agregar `.env` al archivo `.gitignore` si usas control de versiones

## 🚨 Solución de Problemas

### Error: "GROQ_API_KEY not found"

Asegúrate de:
1. Haber creado el archivo `.env`
2. Haber agregado tu API Key de Groq válida
3. Haber instalado `python-dotenv`

### Error: "Module not found"

Ejecuta:
```bash
pip install -r requirements.txt
```

### El chatbot no responde

Verifica:
1. Tu conexión a internet
2. Que tu API Key de Groq sea válida
3. Que el modelo `llama-3.1-8b-instant` esté disponible en tu cuenta

### Error en análisis de sentimientos

El análisis de sentimientos usa la misma API de Groq. Si falla, el chatbot continuará funcionando pero sin detección de sentimiento.

### Error: "Could not find PyAudio"

PyAudio es necesario para usar el micrófono en la función de voz. Para instalarlo:

**Windows:**
```bash
pip install pyaudio
```

**Linux:**
```bash
sudo apt-get install python3-pyaudio
pip install pyaudio
```

**Mac:**
```bash
brew install portaudio
pip install pyaudio
```

**Nota:** Si PyAudio no está instalado, la función de voz aún funcionará usando la opción de archivo de audio.

### No puedo acceder al panel administrativo

Verifica:
1. Que hayas configurado `ADMIN_PASSWORD` en `.env`
2. Que estés usando la contraseña correcta
3. Si no configuraste contraseña, usa `admin123`

## 📝 Notas Adicionales

- El chatbot mantiene un contexto de los últimos 10 mensajes
- Las respuestas se generan con una temperatura de 0.7 para balance entre creatividad y consistencia
- El máximo de tokens por respuesta es 500 para mantener respuestas concisas
- El sistema prompt está diseñado para mantener el rol de asesor humano sin revelar que es una IA
- **Los datos de conversaciones, sentimientos y ratings se almacenan en memoria de sesión** (se pierden al recargar)
- Para persistencia de datos en producción, considerar implementar base de datos
- El análisis de sentimientos se realiza en tiempo real usando IA de Groq
- Los reportes se pueden exportar en formato CSV para análisis externo

## 🤝 Soporte

Para problemas o consultas adicionales, contacta al equipo de desarrollo de VelozyMoto.

---

**VelozyMoto AI Assistant** - Potenciando la atención al cliente con inteligencia artificial 🏍️
