'use client'

import { useEffect, useState } from 'react'
import { getTrace } from '@/lib/api'
import Link from 'next/link'

export default function TraceDetailPage({ params }: { params: { id: string } }) {
  const [trace, setTrace] = useState<any>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const loadTrace = async () => {
      setIsLoading(true)
      setError(null)
      try {
        const data = await getTrace(params.id)
        setTrace(data)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load trace')
      } finally {
        setIsLoading(false)
      }
    }

    loadTrace()
  }, [params.id])

  if (isLoading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="text-center py-8 text-gray-500">Loading trace...</div>
      </div>
    )
  }

  if (error || !trace) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="bg-red-100 dark:bg-red-900 text-red-700 dark:text-red-200 rounded p-4">
          {error || 'Trace not found'}
        </div>
        <Link href="/traces" className="text-blue-600 hover:underline mt-4 inline-block">
          ← Back to Traces
        </Link>
      </div>
    )
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      <Link href="/traces" className="text-blue-600 hover:underline mb-4 inline-block">
        ← Back to Traces
      </Link>

      <h1 className="text-3xl font-bold mb-8">Query Trace Details</h1>

      <div className="space-y-6">
        {/* Query Info */}
        <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Query Information</h2>
          <div className="space-y-2">
            <div>
              <span className="font-semibold">Question:</span>
              <p className="mt-1 text-gray-700 dark:text-gray-300">{trace.query_text}</p>
            </div>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span className="text-gray-500">LLM Provider:</span>
                <span className="ml-2 font-mono">{trace.llm_provider}</span>
              </div>
              <div>
                <span className="text-gray-500">Embedding Provider:</span>
                <span className="ml-2 font-mono">{trace.embedding_provider}</span>
              </div>
              <div>
                <span className="text-gray-500">Top-K:</span>
                <span className="ml-2 font-mono">{trace.top_k}</span>
              </div>
              <div>
                <span className="text-gray-500">Processing Time:</span>
                <span className="ml-2 font-mono">{trace.processing_time_ms}ms</span>
              </div>
            </div>
            <div>
              <span className="text-gray-500 text-sm">Timestamp:</span>
              <span className="ml-2 text-sm">{new Date(trace.created_at).toLocaleString()}</span>
            </div>
          </div>
        </div>

        {/* Retrieved Chunks */}
        <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Retrieved Chunks</h2>
          <div className="space-y-3">
            {trace.retrieved_chunk_ids.map((chunkId: string, idx: number) => (
              <div key={idx} className="bg-gray-50 dark:bg-gray-800 rounded p-3">
                <div className="flex justify-between items-center">
                  <span className="font-mono text-sm text-gray-600 dark:text-gray-400">
                    Chunk #{idx + 1}
                  </span>
                  <span className="text-sm text-gray-500">
                    Similarity: {(trace.similarity_scores[idx] * 100).toFixed(1)}%
                  </span>
                </div>
                <div className="mt-1 text-xs text-gray-400 font-mono break-all">
                  {chunkId}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Answer */}
        <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Generated Answer</h2>
          <p className="text-gray-700 dark:text-gray-300 whitespace-pre-wrap">
            {trace.answer_text}
          </p>
        </div>

        {/* Citations */}
        {trace.citations && trace.citations.length > 0 && (
          <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg p-6">
            <h2 className="text-xl font-semibold mb-4">Citations</h2>
            <div className="space-y-3">
              {trace.citations.map((citation: any, idx: number) => (
                <div key={idx} className="bg-gray-50 dark:bg-gray-800 rounded p-3">
                  <div className="font-semibold">
                    [{citation.number}] {citation.document_name}
                  </div>
                  <div className="text-xs text-gray-500 mt-1">
                    Chunk #{citation.chunk_index}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
