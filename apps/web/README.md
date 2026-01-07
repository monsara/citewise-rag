# CiteWise RAG - Web UI

Next.js frontend for the CiteWise RAG system.

## Setup

```bash
# Install dependencies
npm install

# Copy environment template
cp .env.local.example .env.local
# Edit .env.local
```

## Configuration

Edit `.env.local`:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Run

```bash
# Make sure FastAPI backend is running first
# Then start Next.js dev server
npm run dev
```

Open http://localhost:3000

## Features

### Chat Interface (/)
- Ask questions about uploaded documents
- View answers with source citations
- Configure LLM and embedding providers
- Adjust Top-K parameter

### Documents (/documents)
- Upload TXT and MD files
- View all uploaded documents
- See processing status and metadata

### Traces (/traces)
- Inspect query traces for debugging
- See retrieved chunks and similarity scores
- Understand how answers were generated

## Project Structure

```
web/
├── app/
│   ├── page.tsx              # Chat interface
│   ├── documents/page.tsx    # Document management
│   ├── traces/page.tsx       # Query traces list
│   ├── traces/[id]/page.tsx  # Trace details
│   ├── layout.tsx            # Root layout
│   └── globals.css           # Global styles
├── components/
│   ├── ChatInterface.tsx     # Main chat component
│   ├── CitationCard.tsx      # Citation display
│   ├── SettingsPanel.tsx     # Provider settings
│   └── DocumentUpload.tsx    # File upload
└── lib/
    └── api.ts                # API client
```

## Technology Stack

- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- React Hooks
