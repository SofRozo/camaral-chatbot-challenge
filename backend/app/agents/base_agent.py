from abc import ABC, abstractmethod
from typing import Optional
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

from app.config import settings
from app.models.schemas import AgentResponse


class BaseAgent(ABC):
    """Base class for all specialized agents."""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.llm = ChatOllama(
            model=settings.OLLAMA_MODEL,
            base_url=settings.OLLAMA_BASE_URL,
            temperature=0.7
        )
    
    @property
    @abstractmethod
    def system_prompt(self) -> str:
        """System prompt specific to this agent."""
        pass
    
    @property
    def keywords(self) -> list[str]:
        """Keywords that trigger this agent."""
        return []
    
    def _format_history(self, history: list[dict]) -> list:
        """Convert history dict to LangChain messages."""
        messages = []
        for msg in history[-6:]:  # Last 6 messages for context
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            else:
                messages.append(AIMessage(content=msg["content"]))
        return messages
    
    async def process(
        self, 
        message: str, 
        history: list[dict] = [],
        context: str = ""
    ) -> AgentResponse:
        """Process a message and return a response."""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])
        
        chain = prompt | self.llm
        
        # Add context if available
        input_text = message
        if context:
            input_text = f"Contexto relevante:\n{context}\n\nPregunta: {message}"
        
        response = await chain.ainvoke({
            "input": input_text,
            "history": self._format_history(history)
        })
        
        return AgentResponse(
            content=response.content,
            confidence=0.85,
            sources=[]
        )
    
    def matches_intent(self, message: str) -> float:
        """Check if this agent should handle the message. Returns confidence 0-1."""
        message_lower = message.lower()
        matches = sum(1 for kw in self.keywords if kw in message_lower)
        if matches == 0:
            return 0.0
        return min(matches / len(self.keywords) * 2, 1.0)
