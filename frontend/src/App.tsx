import { useState } from 'react'
import ChatWidget from './components/ChatWidget'
import { Sparkles, Zap, Shield } from 'lucide-react'

function App() {
  const [showChat, setShowChat] = useState(false)

  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section */}
      <div className="container mx-auto px-4 py-16">
        <header className="text-center mb-16">
          <div className="flex items-center justify-center gap-3 mb-6">
            <img src="/bot-avatar.png" alt="Camaral" className="w-14 h-14" />
            <h1 className="text-4xl font-bold text-gray-900">Camaral</h1>
          </div>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Avatares AI que transforman tus procesos de ventas y soporte
          </p>
        </header>

        {/* Features Grid */}
        <div className="grid md:grid-cols-3 gap-8 max-w-4xl mx-auto mb-16">
          <div className="bg-white rounded-2xl p-6 border border-gray-200 shadow-sm hover:shadow-md transition-shadow">
            <Sparkles className="w-10 h-10 text-camaral-primary mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Humanos Digitales
            </h3>
            <p className="text-gray-600 text-sm">
              Avatares que interactúan de manera natural en videollamadas
            </p>
          </div>
          
          <div className="bg-white rounded-2xl p-6 border border-gray-200 shadow-sm hover:shadow-md transition-shadow">
            <Zap className="w-10 h-10 text-camaral-primary mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Disponibilidad 24/7
            </h3>
            <p className="text-gray-600 text-sm">
              Atención constante sin fatiga ni inconsistencias
            </p>
          </div>
          
          <div className="bg-white rounded-2xl p-6 border border-gray-200 shadow-sm hover:shadow-md transition-shadow">
            <Shield className="w-10 h-10 text-camaral-primary mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Seguridad Total
            </h3>
            <p className="text-gray-600 text-sm">
              Encriptación end-to-end y cumplimiento GDPR
            </p>
          </div>
        </div>

        {/* CTA */}
        <div className="text-center">
          <button
            onClick={() => setShowChat(true)}
            className="bg-camaral-primary hover:bg-camaral-accent text-white font-bold py-4 px-8 rounded-full text-lg transition-all duration-300 shadow-lg hover:scale-105"
          >
            Habla con nuestro ChatBot
          </button>
          <p className="text-gray-500 mt-4 text-sm">
            Pregunta lo que quieras sobre Camaral
          </p>
        </div>
      </div>

      {/* Chat Widget */}
      <ChatWidget isOpen={showChat} onClose={() => setShowChat(false)} />

      {/* Floating Chat Button */}
      {!showChat && (
        <button
          onClick={() => setShowChat(true)}
          className="fixed bottom-6 right-6 w-16 h-16 bg-camaral-primary rounded-full flex items-center justify-center shadow-lg hover:scale-110 transition-transform duration-300"
        >
          <img src="/bot-avatar.png" alt="Chat" className="w-12 h-12 rounded-full" />
        </button>
      )}
    </div>
  )
}

export default App
