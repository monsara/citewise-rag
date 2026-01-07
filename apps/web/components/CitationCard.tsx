'use client'

import { useState } from 'react'
import type { Citation } from '@/lib/api'

interface CitationCardProps {
  citation: Citation
}

export default function CitationCard({ citation }: CitationCardProps) {
  const [isExpanded, setIsExpanded] = useState(false)

  return (
    <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded p-3 text-sm">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="font-semibold">
            [{citation.number}] {citation.document_name}
          </div>
          <div className="text-xs text-gray-500 mt-1">
            Chunk #{citation.chunk_index} | Similarity: {(citation.similarity_score * 100).toFixed(1)}%
          </div>
          <div className="mt-2 text-gray-700 dark:text-gray-300">
            {isExpanded ? citation.text : citation.text}
          </div>
        </div>
        {citation.text.endsWith('...') && (
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="ml-2 text-blue-600 hover:text-blue-800 text-xs"
          >
            {isExpanded ? 'Less' : 'More'}
          </button>
        )}
      </div>
    </div>
  )
}
