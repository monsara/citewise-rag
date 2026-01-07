'use client'

import { useState } from 'react'
import { queryRAG, type QueryOptions, type QueryResponse } from '@/lib/api'
import CitationCard from './CitationCard'
import SettingsPanel from './SettingsPanel'

interface Message {
  role: 'user' | 'assistant'
  content: string
  citations?: QueryResponse['citations']
  trace_id?: string
  processing_time_ms?: number
}

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [settings, setSettings] = useState<QueryOptions>({
    top_k: 5,
    llm_provider: 'groq',
    embedding_provider: 'local',
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return

    const userMessage: Message = { role: 'user', content: input }
    setMessages((prev) => [...prev, userMessage])
    setInput('')
    setIsLoading(true)
    setError(null)

    try {
      const response = await queryRAG(input, settings)
      
      const assistantMessage: Message = {
        role: 'assistant',
        content: response.answer,
        citations: response.citations,
        trace_id: response.trace_id,
        processing_time_ms: response.processing_time_ms,
      }
      
      setMessages((prev) => [...prev, assistantMessage])
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Query failed')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="flex flex-col h-full">
      {/* Settings Panel */}
      <div className="border-b border-gray-200 dark:border-gray-800 p-4">
        <SettingsPanel settings={settings} onSettingsChange={setSettings} />
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && (
          <div className="text-center text-gray-500 mt-8">
            <p className="text-lg mb-2">Ask a question about your documents</p>
            <p className="text-sm">Upload documents first in the Documents tab</p>
          </div>
        )}

        {messages.map((message, idx) => (
          <div
            key={idx}
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-3xl rounded-lg p-4 ${
                message.role === 'user'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 dark:bg-gray-800'
              }`}
            >
              <div className="whitespace-pre-wrap">{message.content}</div>
              
              {message.citations && message.citations.length > 0 && (
                <div className="mt-4 space-y-2">
                  <p className="text-sm font-semibold">Sources:</p>
                  {message.citations.map((citation, citIdx) => (
                    <CitationCard key={citIdx} citation={citation} />
                  ))}
                </div>
              )}
              
              {message.trace_id && (
                <div className="mt-2 text-xs text-gray-500 dark:text-gray-400">
                  Trace ID: {message.trace_id} | Time: {message.processing_time_ms}ms
                </div>
              )}
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-100 dark:bg-gray-800 rounded-lg p-4">
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce delay-100"></div>
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce delay-200"></div>
              </div>
            </div>
          </div>
        )}

        {error && (
          <div className="bg-red-100 dark:bg-red-900 text-red-700 dark:text-red-200 rounded-lg p-4">
            Error: {error}
          </div>
        )}
      </div>

      {/* Input */}
      <div className="border-t border-gray-200 dark:border-gray-800 p-4">
        <form onSubmit={handleSubmit} className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a question..."
            className="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Ask
          </button>
        </form>
      </div>
    </div>
  )
}
