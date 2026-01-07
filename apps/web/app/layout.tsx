import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import Link from 'next/link'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'CiteWise RAG',
  description: 'Learning-focused RAG system with source citations',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="min-h-screen flex flex-col">
          {/* Header */}
          <header className="border-b border-gray-200 dark:border-gray-800">
            <div className="container mx-auto px-4 py-4">
              <nav className="flex items-center justify-between">
                <Link href="/" className="text-xl font-bold">
                  CiteWise RAG <span className="text-sm font-normal text-gray-500">v0.1</span>
                </Link>
                <div className="flex gap-6">
                  <Link href="/" className="hover:text-blue-600">
                    Chat
                  </Link>
                  <Link href="/documents" className="hover:text-blue-600">
                    Documents
                  </Link>
                  <Link href="/traces" className="hover:text-blue-600">
                    Traces
                  </Link>
                </div>
              </nav>
            </div>
          </header>

          {/* Main content */}
          <main className="flex-1">{children}</main>

          {/* Footer */}
          <footer className="border-t border-gray-200 dark:border-gray-800 py-4">
            <div className="container mx-auto px-4 text-center text-sm text-gray-500">
              Learning &gt; Features | Clarity &gt; Abstraction | Control &gt; Automation
            </div>
          </footer>
        </div>
      </body>
    </html>
  )
}
