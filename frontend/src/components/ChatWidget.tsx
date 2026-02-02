import { useState, useRef, useEffect } from 'react'
import { Send, X, User, Loader2 } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import { useChat, Message } from '../hooks/useChat'

interface ChatWidgetProps {
  isOpen: boolean
  onClose: () => void
}

const WELCOME_MESSAGE: Message = {
  role: 'assistant',
  content: '¡Hola! 👋 Bienvenido a CamaralBot, aquí resolveremos todas las dudas que tengas sobre nuestros productos. ¿En qué puedo ayudarte?'
}

// Avatar del bot
const BotAvatar = ({ className = "w-8 h-8" }: { className?: string }) => (
  <img src="/bot-avatar.png" alt="Camaral Bot" className={`${className} rounded-full object-cover`} />
)

export default function ChatWidget({ isOpen, onClose }: ChatWidgetProps) {
  const [input, setInput] = useState('')
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLInputElement>(null)
  
  const { messages, isLoading, suggestions, sendMessage } = useChat()
  
  // Combinar mensaje de bienvenida con mensajes del chat
  const allMessages = [WELCOME_MESSAGE, ...messages]

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  useEffect(() => {
    if (isOpen) {
      inputRef.current?.focus()
    }
  }, [isOpen])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (input.trim() && !isLoading) {
      sendMessage(input.trim())
      setInput('')
    }
  }

  const handleSuggestionClick = (suggestion: string) => {
    if (!isLoading) {
      sendMessage(suggestion)
    }
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 md:inset-auto md:bottom-6 md:right-6 md:w-[420px] md:h-[600px] bg-white md:rounded-2xl shadow-2xl flex flex-col overflow-hidden border border-gray-200 z-50">
      {/* Header */}
      <div className="bg-camaral-primary p-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <BotAvatar className="w-10 h-10" />
          <div>
            <h3 className="font-bold text-white">Camaral Bot</h3>
            <p className="text-xs text-white/80">Siempre disponible</p>
          </div>
        </div>
        <button
          onClick={onClose}
          className="w-8 h-8 rounded-full bg-white/20 flex items-center justify-center hover:bg-white/30 transition-colors"
        >
          <X className="w-5 h-5 text-white" />
        </button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-white">
        {allMessages.map((message, index) => (
          <MessageBubble key={index} message={message} />
        ))}

        {isLoading && (
          <div className="flex items-start gap-3">
            <BotAvatar />
            <div className="bg-gray-100 rounded-2xl rounded-tl-none px-4 py-3">
              <div className="flex gap-1">
                <div className="w-2 h-2 bg-camaral-primary rounded-full typing-dot" />
                <div className="w-2 h-2 bg-camaral-primary rounded-full typing-dot" />
                <div className="w-2 h-2 bg-camaral-primary rounded-full typing-dot" />
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Suggestions */}
      {suggestions.length > 0 && !isLoading && (
        <div className="px-4 pb-2 bg-white">
          <div className="flex flex-wrap gap-2">
            {suggestions.map((suggestion, index) => (
              <button
                key={index}
                onClick={() => handleSuggestionClick(suggestion)}
                className="text-xs bg-gray-100 hover:bg-camaral-primary hover:text-white text-gray-700 px-3 py-1.5 rounded-full transition-colors border border-gray-200"
              >
                {suggestion}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Input */}
      <form onSubmit={handleSubmit} className="p-4 border-t border-gray-200 bg-white">
        <div className="flex gap-2">
          <input
            ref={inputRef}
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Escribe tu pregunta..."
            className="flex-1 bg-gray-100 text-gray-900 placeholder-gray-500 rounded-full px-4 py-3 focus:outline-none focus:ring-2 focus:ring-camaral-primary"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={!input.trim() || isLoading}
            className="w-12 h-12 bg-camaral-primary rounded-full flex items-center justify-center hover:bg-camaral-accent transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? (
              <Loader2 className="w-5 h-5 text-white animate-spin" />
            ) : (
              <Send className="w-5 h-5 text-white" />
            )}
          </button>
        </div>
      </form>
    </div>
  )
}

function MessageBubble({ message }: { message: Message }) {
  const isUser = message.role === 'user'

  return (
    <div className={`flex items-start gap-3 message-enter ${isUser ? 'flex-row-reverse' : ''}`}>
      {isUser ? (
        <div className="w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 bg-camaral-primary">
          <User className="w-5 h-5 text-white" />
        </div>
      ) : (
        <BotAvatar />
      )}
      <div className={`max-w-[80%] rounded-2xl px-4 py-3 ${
        isUser 
          ? 'bg-camaral-primary text-white rounded-tr-none' 
          : 'bg-gray-100 text-gray-900 rounded-tl-none'
      }`}>
        {isUser ? (
          <p className="text-sm whitespace-pre-wrap">{message.content}</p>
        ) : (
          <div className="text-sm prose prose-sm max-w-none prose-p:my-1 prose-ul:my-1 prose-li:my-0">
            <ReactMarkdown>{message.content}</ReactMarkdown>
          </div>
        )}
      </div>
    </div>
  )
}
