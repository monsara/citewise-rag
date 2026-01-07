# Архітектура CiteWise RAG

## Огляд

CiteWise RAG - це система, що поєднує традиційний RAG з можливостями графового пошуку для надання точних відповідей з джерелами.

## Компоненти системи

### 1. Frontend (Next.js)
- Інтерфейс чату
- Завантаження документів
- Відображення джерел
- Візуалізація зв'язків (для GraphRAG)

### 2. API Layer (NestJS)
- GraphQL API
- Аутентифікація/авторизація
- Оркестрація запитів
- Кешування (Redis)

### 3. ML Service (FastAPI)
- Генерація embeddings
- Векторний пошук (Weaviate)
- Ре-ранкінг результатів
- GraphRAG logic (пізніше)

### 4. Data Layer
- **PostgreSQL**: метадані документів, користувачі, історія чатів
- **Weaviate**: векторне сховище для семантичного пошуку
- **Neo4j**: графова база для GraphRAG (пізніше)
- **Redis**: кешування, черги

## Потік даних

```
User Query → Next.js → NestJS API → FastAPI ML Service
                ↓                           ↓
            GraphQL                    Embeddings
                ↓                           ↓
            PostgreSQL                  Weaviate
                                            ↓
                                       Retrieved Docs
                                            ↓
                                       LLM (OpenAI/Local)
                                            ↓
                                       Response + Sources
```

## Масштабування

- Горизонтальне масштабування FastAPI workers
- Реплікація Weaviate
- PostgreSQL read replicas
- Redis cluster для кешування

## Безпека

- JWT аутентифікація
- Rate limiting
- Валідація вхідних даних
- Ізоляція даних користувачів
