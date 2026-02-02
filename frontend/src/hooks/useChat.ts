import { useState, useCallback } from 'react'

export interface Message {
  role: 'user' | 'assistant'
  content: string
  agent?: string
}

interface ChatResponse {
  content: string
  agent_used: string
  confidence: number
  suggestions: string[]
}

const API_URL = '/api/chat'

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [suggestions, setSuggestions] = useState<string[]>([
    '¿Qué es Camaral?',
    '¿Cómo funcionan los avatares?',
    '¿Puedo ver una demo?'
  ])
  const [sessionId] = useState(() => `session_${Date.now()}`)

  const sendMessage = useCallback(async (content: string) => {
    if (!content.trim()) return

    // Add user message
    const userMessage: Message = { role: 'user', content }
    setMessages(prev => [...prev, userMessage])
    setIsLoading(true)
    setSuggestions([])

    try {
      const response = await fetch(`${API_URL}/message`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: content,
          session_id: sessionId
        }),
      })

      if (!response.ok) {
        throw new Error('Failed to get response')
      }

      const data: ChatResponse = await response.json()

      // Add assistant message
      const assistantMessage: Message = {
        role: 'assistant',
        content: data.content,
        agent: data.agent_used
      }
      setMessages(prev => [...prev, assistantMessage])
      setSuggestions(data.suggestions || [])

    } catch (error) {
      console.error('Chat error:', error)
      
      // Add error message
      const errorMessage: Message = {
        role: 'assistant',
        content: 'Lo siento, hubo un error al procesar tu mensaje. Por favor, intenta de nuevo.',
      }
      setMessages(prev => [...prev, errorMessage])
      setSuggestions([
        '¿Qué es Camaral?',
        '¿Tienen soporte técnico?'
      ])
    } finally {
      setIsLoading(false)
    }
  }, [sessionId])

  const clearMessages = useCallback(() => {
    setMessages([])
    setSuggestions([
      '¿Qué es Camaral?',
      '¿Cómo funcionan los avatares?',
      '¿Puedo ver una demo?'
    ])
  }, [])

  return {
    messages,
    isLoading,
    suggestions,
    sendMessage,
    clearMessages
  }
}
