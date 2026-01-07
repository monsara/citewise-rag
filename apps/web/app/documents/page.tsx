'use client'

import { useEffect, useState } from 'react'
import { getDocuments, type Document } from '@/lib/api'
import DocumentUpload from '@/components/DocumentUpload'

export default function DocumentsPage() {
  const [documents, setDocuments] = useState<Document[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const loadDocuments = async () => {
    setIsLoading(true)
    setError(null)
    try {
      const docs = await getDocuments()
      setDocuments(docs)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load documents')
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    loadDocuments()
  }, [])

  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      <h1 className="text-3xl font-bold mb-8">Document Management</h1>

      {/* Upload Section */}
      <div className="mb-12">
        <h2 className="text-xl font-semibold mb-4">Upload New Document</h2>
        <DocumentUpload onUploadComplete={loadDocuments} />
      </div>

      {/* Documents List */}
      <div>
        <h2 className="text-xl font-semibold mb-4">
          Uploaded Documents ({documents.length})
        </h2>

        {isLoading && (
          <div className="text-center py-8 text-gray-500">Loading documents...</div>
        )}

        {error && (
          <div className="bg-red-100 dark:bg-red-900 text-red-700 dark:text-red-200 rounded p-4">
            {error}
          </div>
        )}

        {!isLoading && !error && documents.length === 0 && (
          <div className="text-center py-8 text-gray-500">
            No documents uploaded yet. Upload your first document above!
          </div>
        )}

        {!isLoading && !error && documents.length > 0 && (
          <div className="space-y-4">
            {documents.map((doc) => (
              <div
                key={doc.id}
                className="border border-gray-200 dark:border-gray-800 rounded-lg p-4 hover:shadow-md transition-shadow"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h3 className="font-semibold text-lg">{doc.filename}</h3>
                    <div className="text-sm text-gray-500 mt-1 space-y-1">
                      <p>Type: {doc.file_type.toUpperCase()}</p>
                      <p>Size: {(doc.file_size / 1024).toFixed(2)} KB</p>
                      <p>Chunks: {doc.chunk_count || 0}</p>
                      <p>Uploaded: {new Date(doc.upload_date).toLocaleString()}</p>
                    </div>
                  </div>
                  <div>
                    <span
                      className={`px-3 py-1 rounded-full text-xs font-semibold ${
                        doc.status === 'completed'
                          ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                          : doc.status === 'failed'
                          ? 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
                          : 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200'
                      }`}
                    >
                      {doc.status}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
