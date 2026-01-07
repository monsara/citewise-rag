# Архітектурні рішення

## ADR-001: Вибір технологічного стеку

**Дата**: 2026-01-07
**Статус**: Прийнято

### Контекст
Необхідно обрати технології для реалізації RAG системи з можливістю майбутнього розширення до GraphRAG.

### Рішення

#### Frontend
- **Next.js 14+** (App Router)
  - SSR/SSG для SEO
  - Server Components для оптимізації
  - TypeScript для type safety

#### Backend API
- **NestJS** з GraphQL
  - Модульна архітектура
  - Вбудована підтримка TypeScript
  - GraphQL для гнучких запитів

#### ML Service
- **FastAPI**
  - Швидкість та продуктивність
  - Async підтримка
  - Зручна інтеграція з Python ML libs

#### Databases
- **Weaviate**: векторне сховище (краще за Pinecone для self-hosted)
- **PostgreSQL**: реляційні дані
- **Neo4j**: графова БД для GraphRAG
- **Redis**: кешування та черги

### Наслідки
- Складність інфраструктури (4 БД)
- Потреба в DevOps експертизі
- Можливість поетапного розгортання

---

## ADR-002: Поетапний підхід до GraphRAG

**Дата**: 2026-01-07
**Статус**: Прийнято

### Контекст
GraphRAG - складна технологія, повна імплементація може затримати MVP.

### Рішення
Розробка у 3 фази:

**Phase 1 (MVP)**: Базовий RAG
- Weaviate для векторного пошуку
- Простий source tracking
- PostgreSQL для метаданих

**Phase 2**: GraphRAG foundation
- Додавання Neo4j
- Entity extraction
- Basic graph traversal

**Phase 3**: Advanced GraphRAG
- Multi-hop reasoning
- Community detection
- Temporal graphs

### Наслідки
- Швидший час до MVP
- Можливість валідації перед складними інвестиціями
- Поступове зростання складності

---

## ADR-003: Monorepo structure

**Дата**: 2026-01-07
**Статус**: Прийнято

### Контекст
Три окремі додатки (web, api, ml) з спільним кодом.

### Рішення
Використання monorepo з:
- `apps/` для applications
- `packages/shared/` для спільного коду
- Окремі `package.json` для кожного app
- Shared TypeScript types

### Альтернативи
- Окремі репозиторії (складніше sync)
- Git submodules (застаріле)

### Наслідки
- Простіша координація змін
- Єдиний CI/CD pipeline
- Shared dependencies management

---

## ADR-004: GraphQL замість REST

**Дата**: 2026-01-07
**Статус**: Прийнято

### Контекст
Вибір API архітектури між GraphQL та REST.

### Рішення
GraphQL для основного API:
- Гнучкі запити (важливо для UI з різними views)
- Strongly typed schema
- Ефективність (no over-fetching)

REST для ML service:
- Простота
- Стандартні ендпоінти для embeddings

### Наслідки
- Потреба в GraphQL expertise
- Складніший debugging
- Кращий developer experience для frontend

---

## ADR-005: Docker Compose для локальної розробки

**Дата**: 2026-01-07
**Статус**: Прийнято

### Контекст
Множина залежностей (PostgreSQL, Weaviate, Redis, Neo4j).

### Рішення
Docker Compose для:
- Локальної розробки
- CI/CD testing
- Швидкого onboarding

Kubernetes для production (пізніше).

### Наслідки
- Легкий старт для нових розробників
- Консистентне середовище
- Потреба в Docker знаннях
