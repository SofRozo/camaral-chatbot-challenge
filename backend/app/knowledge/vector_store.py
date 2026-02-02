from langchain_core.documents import Document
from typing import Optional

from app.config import settings

# Simple in-memory storage for quick setup
_documents: list[Document] = []


# Initial knowledge about Camaral
CAMARAL_KNOWLEDGE = [
    {
        "content": """Camaral es la plataforma líder para crear Avatares AI que participan en reuniones 
        de ventas y soporte. La plataforma permite a empresas escalar sus operaciones de ventas y 
        atención al cliente mediante humanos digitales que interactúan de manera natural y profesional.""",
        "metadata": {"category": "general", "topic": "about"}
    },
    {
        "content": """Los Avatares de Camaral son humanos digitales potenciados por inteligencia artificial.
        Pueden participar en videollamadas, responder preguntas, presentar productos, y calificar leads.
        Utilizan modelos de lenguaje avanzados para mantener conversaciones naturales y contextuales.""",
        "metadata": {"category": "product", "topic": "avatars"}
    },
    {
        "content": """Camaral ofrece integraciones con las principales plataformas empresariales:
        - CRMs: Salesforce, HubSpot, Pipedrive, Zoho
        - Calendarios: Google Calendar, Outlook, Calendly
        - Video: Zoom, Google Meet, Microsoft Teams
        - Ecommerce: Shopify, WooCommerce
        También cuenta con API REST para integraciones personalizadas.""",
        "metadata": {"category": "tech", "topic": "integrations"}
    },
    {
        "content": """Los casos de uso principales de Camaral incluyen:
        1. Ventas: Calificación de leads, presentaciones de producto, agendamiento de citas
        2. Soporte: Respuesta a consultas frecuentes, escalamiento inteligente
        3. Onboarding: Guía a nuevos clientes en el uso de productos
        4. Demos: Presentaciones personalizadas 24/7""",
        "metadata": {"category": "sales", "topic": "use_cases"}
    },
    {
        "content": """Beneficios de implementar Camaral:
        - Aumento del 40% en capacidad de atención
        - Reducción del 60% en tiempo de respuesta
        - Disponibilidad 24/7/365
        - Consistencia en la calidad de cada interacción
        - Análisis detallado de conversaciones
        - Reducción de costos operativos""",
        "metadata": {"category": "sales", "topic": "benefits"}
    },
    {
        "content": """La seguridad en Camaral es prioritaria:
        - Encriptación end-to-end de todas las conversaciones
        - Cumplimiento con GDPR y regulaciones de privacidad
        - Servidores certificados SOC 2
        - Opción de deployment on-premise para Enterprise
        - Auditorías de seguridad regulares""",
        "metadata": {"category": "tech", "topic": "security"}
    },
    {
        "content": """Planes y precios de Camaral:
        - Starter: Ideal para pequeñas empresas, incluye 1 avatar y 500 interacciones/mes
        - Professional: Para empresas en crecimiento, avatares ilimitados, 5000 interacciones/mes
        - Enterprise: Solución completa con deployment personalizado, soporte 24/7
        Ofrecemos período de prueba de 14 días sin compromiso.""",
        "metadata": {"category": "sales", "topic": "pricing"}
    },
    {
        "content": """Camaral fue co-fundada por emprendedores con experiencia en Grayola, Suuper, 
        y GTM Supersonic. El equipo combina expertise en inteligencia artificial, ventas B2B, 
        y experiencia de usuario para crear la mejor solución de avatares para empresas.""",
        "metadata": {"category": "general", "topic": "team"}
    },
    {
        "content": """El proceso de implementación de Camaral:
        1. Llamada de discovery (30 min): Entendemos tus necesidades
        2. Demo personalizada: Mostramos cómo funcionaría para tu caso
        3. Configuración (2-4 semanas): Personalizamos el avatar con tu información
        4. Entrenamiento: Ajustamos el avatar basado en feedback
        5. Lanzamiento: Go-live con soporte continuo""",
        "metadata": {"category": "sales", "topic": "implementation"}
    },
    {
        "content": """Soporte técnico de Camaral:
        - Plan Starter: Soporte por email, respuesta en 24 horas
        - Plan Professional: Chat en vivo, respuesta en 4 horas
        - Plan Enterprise: Soporte dedicado 24/7, Account Manager asignado
        Base de conocimientos y documentación disponible para todos los planes.""",
        "metadata": {"category": "faq", "topic": "support"}
    }
]


async def initialize_vector_store():
    """Initialize the knowledge base with Camaral documents."""
    global _documents
    
    # Create documents from knowledge base
    _documents = [
        Document(
            page_content=item["content"],
            metadata=item["metadata"]
        )
        for item in CAMARAL_KNOWLEDGE
    ]
    
    print(f"✅ Loaded {len(_documents)} documents into knowledge base")


async def search_knowledge(query: str, k: int = 3) -> str:
    """Search the knowledge base for relevant information."""
    global _vector_store
    
    """Search the knowledge base for relevant information using keyword matching."""
    global _documents
    
    if not _documents:
        return ""
    
    try:
        query_lower = query.lower()
        query_words = set(query_lower.split())
        
        # Score documents by keyword overlap
        scored_docs = []
        for doc in _documents:
            content_lower = doc.page_content.lower()
            score = sum(1 for word in query_words if word in content_lower)
            if score > 0:
                scored_docs.append((score, doc))
        
        # Sort by score and take top k
        scored_docs.sort(key=lambda x: x[0], reverse=True)
        top_docs = [doc for _, doc in scored_docs[:k]]
        
        if not top_docs:
            return ""
        
        context = "\n\n".join([doc.page_content for doc in top_docs])
        return context
        
    except Exception as e:
        print(f"Error searching knowledge base: {e}")
        return ""


async def add_document(content: str, metadata: dict = {}):
    """Add a new document to the knowledge base."""
    global _documents
    
    try:
        doc = Document(page_content=content, metadata=metadata)
        _documents.append(doc)
        return True
    except Exception as e:
        print(f"Error adding document: {e}")
        return False
