'use client'

import { useEffect } from 'react'
import type { QueryOptions } from '@/lib/api'

interface SettingsPanelProps {
  settings: QueryOptions
  onSettingsChange: (settings: QueryOptions) => void
}

export default function SettingsPanel({ settings, onSettingsChange }: SettingsPanelProps) {
  // Load from localStorage on mount
  useEffect(() => {
    const saved = localStorage.getItem('rag-settings')
    if (saved) {
      try {
        onSettingsChange(JSON.parse(saved))
      } catch (e) {
        console.error('Failed to load settings', e)
      }
    }
  }, [])

  // Save to localStorage on change
  useEffect(() => {
    localStorage.setItem('rag-settings', JSON.stringify(settings))
  }, [settings])

  return (
    <div className="flex flex-wrap gap-4 items-center">
      <div className="text-sm font-semibold text-gray-700 dark:text-gray-300">
        Settings:
      </div>

      {/* LLM Provider */}
      <div className="flex items-center gap-2">
        <label className="text-sm text-gray-600 dark:text-gray-400">LLM:</label>
        <select
          value={settings.llm_provider}
          onChange={(e) => onSettingsChange({ ...settings, llm_provider: e.target.value as any })}
          className="px-2 py-1 text-sm border border-gray-300 dark:border-gray-700 rounded dark:bg-gray-800"
        >
          <option value="groq">Groq (Llama 3.1 70B) ⚡</option>
          <option value="ollama">Ollama (Local)</option>
          <option value="openai">OpenAI</option>
        </select>
      </div>

      {/* Embedding Provider */}
      <div className="flex items-center gap-2">
        <label className="text-sm text-gray-600 dark:text-gray-400">Embeddings:</label>
        <select
          value={settings.embedding_provider}
          onChange={(e) => onSettingsChange({ ...settings, embedding_provider: e.target.value as any })}
          className="px-2 py-1 text-sm border border-gray-300 dark:border-gray-700 rounded dark:bg-gray-800"
        >
          <option value="local">Local (Sentence Transformers)</option>
          <option value="openai">OpenAI</option>
        </select>
      </div>

      {/* Top-K Slider */}
      <div className="flex items-center gap-2">
        <label className="text-sm text-gray-600 dark:text-gray-400">Top-K:</label>
        <input
          type="range"
          min="3"
          max="10"
          value={settings.top_k}
          onChange={(e) => onSettingsChange({ ...settings, top_k: parseInt(e.target.value) })}
          className="w-24"
        />
        <span className="text-sm w-6">{settings.top_k}</span>
      </div>
    </div>
  )
}
