# Camaral ChatBot - Sistema Multiagente

<div align="center">

**Sistema de ChatBot inteligente con arquitectura multiagente para Camaral**

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-121212?style=for-the-badge&logo=chainlink&logoColor=white)](https://langchain.com/)
[![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)

</div>

---

## 📋 Descripción

Este proyecto implementa un **ChatBot multiagente** para Camaral, la plataforma de Avatares AI para ventas y soporte. El sistema utiliza una arquitectura de orquestador con agentes especializados para proporcionar respuestas precisas y contextuales.

### 🎯 Características Principales

- **🎭 Sistema Multiagente**: Orquestador inteligente que delega a 4 agentes especializados
- **🧠 RAG (Retrieval Augmented Generation)**: Base de conocimiento vectorial para respuestas precisas
- **⚡ Tiempo Real**: WebSocket para comunicación instantánea
- **💬 Sugerencias Inteligentes**: Generación automática de preguntas de seguimiento
- **🎨 UI Moderna**: Interfaz atractiva con modo widget embebible
- **📊 Clasificación de Intención**: Enrutamiento inteligente basado en keywords + LLM

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (React + Vite)                   │
│                    Chat Widget + Landing Page                    │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FastAPI Backend                             │
│              REST API + WebSocket + CORS                         │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    🎭 ORQUESTADOR                                │
│         Clasifica intención → Delega → Consolida                │
└─────────────────────────────────────────────────────────────────┘
           │              │              │              │
           ▼              ▼              ▼              ▼
    ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
    │ 🏢 Info  │   │ 💼 Sales │   │ 🔧 Tech  │   │ ❓ FAQ   │
    │  Agent   │   │  Agent   │   │  Agent   │   │  Agent   │
    └──────────┘   └──────────┘   └──────────┘   └──────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    📦 ChromaDB Vector Store                      │
│                   Knowledge Base de Camaral                      │
└─────────────────────────────────────────────────────────────────┘
```

### 🤖 Agentes Especializados

| Agente | Responsabilidad | Ejemplos |
|--------|-----------------|----------|
| **Info Agent** | Información general de Camaral | "¿Qué es Camaral?", "¿Quién fundó la empresa?" |
| **Sales Agent** | Ventas, demos, ROI | "¿Puedo ver una demo?", "¿Cuánto cuesta?" |
| **Tech Agent** | Integraciones, API, seguridad | "¿Se integra con Salesforce?", "¿Cómo funciona?" |
| **FAQ Agent** | Preguntas frecuentes | "¿Tienen soporte 24/7?", "¿Puedo cancelar?" |

---

## 🚀 Instalación y Ejecución

### Prerrequisitos

- Python 3.11+
- Node.js 18+
- API Key de OpenAI

### 1. Backend

```bash
# Navegar al directorio backend
cd backend

# Crear entorno virtual
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
copy .env.example .env
# Editar .env y agregar tu OPENAI_API_KEY

# Ejecutar servidor
uvicorn app.main:app --reload --port 8000
```

### 2. Frontend

```bash
# Navegar al directorio frontend
cd frontend

# Instalar dependencias
npm install

# Ejecutar en modo desarrollo
npm run dev
```

### 3. Acceder a la Aplicación

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## 📁 Estructura del Proyecto

```
camaral-chatbot-challenge/
├── backend/
│   ├── app/
│   │   ├── agents/           # Agentes especializados
│   │   │   ├── orchestrator.py   # Orquestador principal
│   │   │   ├── base_agent.py     # Clase base
│   │   │   ├── info_agent.py     # Agente de información
│   │   │   ├── sales_agent.py    # Agente de ventas
│   │   │   ├── tech_agent.py     # Agente técnico
│   │   │   └── faq_agent.py      # Agente FAQ
│   │   ├── api/
│   │   │   └── routes/
│   │   │       ├── chat.py       # Endpoints de chat
│   │   │       └── health.py     # Health checks
│   │   ├── knowledge/
│   │   │   └── vector_store.py   # Base vectorial
│   │   ├── models/
│   │   │   └── schemas.py        # Modelos Pydantic
│   │   ├── config.py             # Configuración
│   │   └── main.py               # Entry point
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── ChatWidget.tsx    # Widget de chat
│   │   ├── hooks/
│   │   │   └── useChat.ts        # Hook de chat
│   │   ├── App.tsx               # Componente principal
│   │   └── index.css             # Estilos
│   ├── package.json
│   └── vite.config.ts
├── docker-compose.yml
└── README.md
```

---

## 🔧 API Endpoints

### REST API

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/api/chat/message` | Enviar mensaje y recibir respuesta |
| `DELETE` | `/api/chat/session/{id}` | Limpiar historial de sesión |
| `GET` | `/health` | Estado del servicio |

### WebSocket

| Endpoint | Descripción |
|----------|-------------|
| `ws://localhost:8000/api/chat/ws/{session_id}` | Chat en tiempo real |

### Ejemplo de Request

```json
POST /api/chat/message
{
  "message": "¿Qué es Camaral?",
  "session_id": "user123"
}
```

### Ejemplo de Response

```json
{
  "content": "Camaral es la plataforma líder para crear Avatares AI...",
  "agent_used": "info",
  "confidence": 0.85,
  "suggestions": [
    "¿Cómo funcionan los avatares?",
    "¿Puedo ver una demo?",
    "¿Qué integraciones tienen?"
  ]
}
```

---

## 🛠️ Stack Tecnológico

| Capa | Tecnología |
|------|------------|
| **Backend** | FastAPI, Python 3.11 |
| **Agentes** | LangChain, OpenAI GPT-4 |
| **Vector DB** | ChromaDB |
| **Frontend** | React 18, TypeScript, Vite |
| **Estilos** | TailwindCSS |
| **Real-time** | WebSockets |

---

## ✨ Funcionalidades Adicionales

1. **🎯 Clasificación Híbrida**: Combina keywords + LLM para mejor routing
2. **💡 Sugerencias Dinámicas**: Genera preguntas de seguimiento relevantes
3. **📱 Widget Embebible**: Fácil de integrar en cualquier sitio web
4. **🔄 Historial de Conversación**: Mantiene contexto entre mensajes
5. **⚡ Respuestas en Streaming** (WebSocket): UX fluida y natural

---

## 👥 Autor

Desarrollado para el reto Camaral - Makers Challenge

---

## 📄 Licencia

MIT License - Libre para uso y modificación
