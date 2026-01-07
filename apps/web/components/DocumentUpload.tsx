'use client'

import { useState } from 'react'
import { uploadDocument } from '@/lib/api'

interface DocumentUploadProps {
  onUploadComplete?: () => void
}

export default function DocumentUpload({ onUploadComplete }: DocumentUploadProps) {
  const [file, setFile] = useState<File | null>(null)
  const [isUploading, setIsUploading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(null)
  const [isDragging, setIsDragging] = useState(false)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0])
      setError(null)
      setSuccess(null)
    }
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0])
      setError(null)
      setSuccess(null)
    }
  }

  const handleUpload = async () => {
    if (!file) return

    setIsUploading(true)
    setError(null)
    setSuccess(null)

    try {
      const result = await uploadDocument(file)
      setSuccess(`Document uploaded successfully! ${result.chunk_count} chunks created.`)
      setFile(null)
      if (onUploadComplete) {
        onUploadComplete()
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Upload failed')
    } finally {
      setIsUploading(false)
    }
  }

  return (
    <div className="space-y-4">
      {/* Drag and Drop Area */}
      <div
        onDragOver={(e) => {
          e.preventDefault()
          setIsDragging(true)
        }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={handleDrop}
        className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
          isDragging
            ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
            : 'border-gray-300 dark:border-gray-700'
        }`}
      >
        <input
          type="file"
          onChange={handleFileChange}
          accept=".txt,.md"
          className="hidden"
          id="file-upload"
        />
        <label htmlFor="file-upload" className="cursor-pointer">
          <div className="text-gray-600 dark:text-gray-400">
            <p className="text-lg mb-2">Drop a file here or click to browse</p>
            <p className="text-sm">Supported formats: .txt, .md</p>
          </div>
        </label>
      </div>

      {/* Selected File */}
      {file && (
        <div className="bg-gray-100 dark:bg-gray-800 rounded p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="font-semibold">{file.name}</p>
              <p className="text-sm text-gray-500">
                {(file.size / 1024).toFixed(2)} KB
              </p>
            </div>
            <button
              onClick={() => setFile(null)}
              className="text-red-600 hover:text-red-800"
            >
              Remove
            </button>
          </div>
        </div>
      )}

      {/* Upload Button */}
      {file && (
        <button
          onClick={handleUpload}
          disabled={isUploading}
          className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isUploading ? 'Uploading...' : 'Upload and Process'}
        </button>
      )}

      {/* Messages */}
      {error && (
        <div className="bg-red-100 dark:bg-red-900 text-red-700 dark:text-red-200 rounded p-3">
          {error}
        </div>
      )}
      {success && (
        <div className="bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-200 rounded p-3">
          {success}
        </div>
      )}
    </div>
  )
}
