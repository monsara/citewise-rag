'use client'

import { useEffect, useState } from 'react'
import { getTraces, type Trace } from '@/lib/api'
import Link from 'next/link'

export default function TracesPage() {
  const [traces, setTraces] = useState<Trace[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const loadTraces = async () => {
      setIsLoading(true)
      setError(null)
      try {
        const data = await getTraces(50)
        setTraces(data)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load traces')
      } finally {
        setIsLoading(false)
      }
    }

    loadTraces()
  }, [])

  return (
    <div className="container mx-auto px-4 py-8 max-w-6xl">
      <h1 className="text-3xl font-bold mb-8">Query Traces</h1>

      <p className="text-gray-600 dark:text-gray-400 mb-8">
        Inspect how the RAG pipeline processes queries. This is helpful for learning and debugging.
      </p>

      {isLoading && <div className="text-center py-8 text-gray-500">Loading traces...</div>}

      {error && (
        <div className="bg-red-100 dark:bg-red-900 text-red-700 dark:text-red-200 rounded p-4">
          {error}
        </div>
      )}

      {!isLoading && !error && traces.length === 0 && (
        <div className="text-center py-8 text-gray-500">
          No queries yet. Ask some questions in the Chat tab!
        </div>
      )}

      {!isLoading && !error && traces.length > 0 && (
        <div className="space-y-4">
          {traces.map(trace => (
            <div
              key={trace.id}
              className="border border-gray-200 dark:border-gray-800 rounded-lg p-4 hover:shadow-md transition-shadow"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <h3 className="font-semibold text-lg mb-2">{trace.query_text}</h3>
                  <div className="text-sm text-gray-600 dark:text-gray-400 mb-3 line-clamp-2">
                    {trace.answer_text}
                  </div>
                  <div className="flex flex-wrap gap-4 text-xs text-gray-500">
                    <span>LLM: {trace.llm_provider}</span>
                    <span>Embeddings: {trace.embedding_provider}</span>
                    <span>Top-K: {trace.top_k}</span>
                    <span>Time: {trace.processing_time_ms}ms</span>
                    <span>{new Date(trace.created_at).toLocaleString()}</span>
                  </div>
                </div>
                <Link
                  href={`/traces/${trace.id}`}
                  className="ml-4 px-3 py-1 bg-blue-600 text-white text-sm rounded hover:bg-blue-700"
                >
                  View Details
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
