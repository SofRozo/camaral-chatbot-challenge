from typing import Optional
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

from app.config import settings
from app.models.schemas import ChatResponse, AgentResponse
from app.agents.info_agent import InfoAgent
from app.agents.sales_agent import SalesAgent
from app.agents.tech_agent import TechAgent
from app.agents.faq_agent import FAQAgent
from app.knowledge.vector_store import search_knowledge


class Orchestrator:
    """
    Orchestrator agent that routes messages to specialized agents.
    Uses intent classification to determine the best agent for each query.
    """
    
    def __init__(self):
        self.llm = ChatOllama(
            model=settings.OLLAMA_MODEL,
            base_url=settings.OLLAMA_BASE_URL,
            temperature=0
        )
        
        # Initialize specialized agents
        self.agents = {
            "info": InfoAgent(),
            "sales": SalesAgent(),
            "tech": TechAgent(),
            "faq": FAQAgent()
        }
        
        # Classification prompt
        self.classifier_prompt = ChatPromptTemplate.from_messages([
            ("system", """Eres un clasificador de intenciones para el chatbot de Camaral.
Tu trabajo es determinar qué agente especializado debe manejar cada mensaje.

AGENTES DISPONIBLES:
- info: Información general sobre Camaral (qué es, quiénes son, misión, visión, equipo)
- sales: Ventas, demos, precios, casos de uso, beneficios, ROI
- tech: Preguntas técnicas, integraciones, API, seguridad, requisitos
- faq: Preguntas frecuentes generales, soporte, pruebas, cancelaciones

INSTRUCCIONES:
1. Analiza el mensaje del usuario
2. Determina la intención principal
3. Responde SOLO con el nombre del agente (info, sales, tech, o faq)
4. Si no estás seguro, usa "info" como default

Responde únicamente con una palabra: info, sales, tech, o faq"""),
            ("human", "{message}")
        ])
        
        # Suggestions generator
        self.suggestions_prompt = ChatPromptTemplate.from_messages([
            ("system", """Basándote en la conversación, genera 3 sugerencias cortas de preguntas 
que el usuario podría querer hacer a continuación. Las sugerencias deben ser relevantes 
para Camaral (avatares AI para ventas y soporte).

Responde en formato JSON array: ["sugerencia 1", "sugerencia 2", "sugerencia 3"]
Cada sugerencia debe tener máximo 6 palabras."""),
            ("human", "Mensaje del usuario: {message}\nRespuesta del bot: {response}")
        ])
    
    async def _classify_intent(self, message: str) -> str:
        """Classify the user's intent using fast keyword matching only."""
        # Use keyword matching for fast routing (no LLM call)
        scores = {}
        for name, agent in self.agents.items():
            scores[name] = agent.matches_intent(message)
        
        # Get the best match
        max_score = max(scores.values())
        if max_score > 0:
            return max(scores, key=scores.get)
        
        # Default to info agent
        return "info"
    
    def _get_static_suggestions(self, agent_name: str) -> list[str]:
        """Get static suggestions based on the agent used (no LLM call)."""
        suggestions_map = {
            "info": ["¿Cómo funcionan los avatares?", "¿Tienen demos?", "¿Qué integraciones hay?"],
            "sales": ["¿Cuánto cuesta?", "¿Hay período de prueba?", "¿Cómo empiezo?"],
            "tech": ["¿Se integra con mi CRM?", "¿Tienen API?", "¿Es seguro?"],
            "faq": ["¿Tienen soporte 24/7?", "¿Puedo cancelar?", "¿Qué idiomas soportan?"]
        }
        return suggestions_map.get(agent_name, suggestions_map["info"])

    async def process(
        self, 
        message: str, 
        history: list[dict] = []
    ) -> ChatResponse:
        """
        Process an incoming message through the multi-agent system.
        
        1. Classify intent
        2. Retrieve relevant context from knowledge base
        3. Route to appropriate agent
        4. Generate suggestions
        5. Return formatted response
        """
        
        # Step 1: Classify intent
        agent_name = await self._classify_intent(message)
        agent = self.agents[agent_name]
        
        # Step 2: Search knowledge base for context
        context = await search_knowledge(message)
        
        # Step 3: Get response from specialized agent
        agent_response: AgentResponse = await agent.process(
            message=message,
            history=history,
            context=context
        )
        
        # Step 4: Get static suggestions (fast, no LLM call)
        suggestions = self._get_static_suggestions(agent_name)
        
        # Step 5: Return formatted response
        return ChatResponse(
            content=agent_response.content,
            agent_used=agent_name,
            confidence=agent_response.confidence,
            suggestions=suggestions
        )
