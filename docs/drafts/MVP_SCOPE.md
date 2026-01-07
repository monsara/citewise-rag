# MVP Scope - CiteWise RAG

## Мета MVP
Створити працюючу RAG систему з базовим функціоналом для валідації концепції та збору feedback від користувачів.

## Функціональні вимоги

### Must Have (P0)

#### 1. Завантаження документів
- [ ] Upload PDF/TXT/MD файлів
- [ ] Chunking документів
- [ ] Генерація embeddings
- [ ] Збереження в Weaviate
- [ ] Метадані в PostgreSQL

#### 2. Чат інтерфейс
- [ ] Текстове поле для запитів
- [ ] Відображення відповідей
- [ ] Історія чату (session-based)
- [ ] Typing indicator

#### 3. RAG Pipeline
- [ ] Векторний пошук по query
- [ ] Retrieval top-k релевантних chunks
- [ ] Формування prompt з контекстом
- [ ] Генерація відповіді через LLM
- [ ] Повернення відповіді + джерел

#### 4. Source Citations
- [ ] Відображення джерел під відповіддю
- [ ] Посилання на оригінальні документи
- [ ] Виділення релевантних фрагментів

### Should Have (P1)

#### 5. Управління документами
- [ ] Список завантажених документів
- [ ] Видалення документів
- [ ] Пошук по документах

#### 6. Покращення якості
- [ ] Re-ranking результатів
- [ ] Фільтрація нерелевантних chunks
- [ ] Confidence scores для джерел

#### 7. User Experience
- [ ] Loading states
- [ ] Error handling
- [ ] Responsive design (mobile-friendly)

### Could Have (P2)

#### 8. Advanced features
- [ ] Multi-document conversations
- [ ] Експорт чату
- [ ] Теми/категорії документів
- [ ] Пошук по історії чатів

### Won't Have (для MVP)

- ❌ GraphRAG (Neo4j integration)
- ❌ Аутентифікація користувачів
- ❌ Multi-tenancy
- ❌ Advanced analytics
- ❌ Візуалізація зв'язків
- ❌ Collaborative features
- ❌ Fine-tuning embeddings
- ❌ Custom LLM models

## Технічні обмеження MVP

### Frontend
- Базовий UI без складних анімацій
- Одна тема (dark/light toggle не потрібен)
- Без інтернаціоналізації

### Backend
- Без rate limiting
- Без advanced caching
- Без мікросервісної архітектури (можна спростити)

### ML
- Використання готових embeddings (OpenAI/Sentence Transformers)
- Базовий chunking (без smart splitting)
- Без custom retrieval strategies

### Infrastructure
- Docker Compose (без Kubernetes)
- Локальний deployment
- Без CI/CD pipelines

## Метрики успіху MVP

### Функціональні метрики
- ✅ Користувач може завантажити документ за < 30 сек
- ✅ Отримання відповіді за < 5 сек
- ✅ Точність джерел > 80%
- ✅ Система обробляє документи до 50 сторінок

### Технічні метрики
- ✅ Uptime > 95%
- ✅ < 10% помилок при запитах
- ✅ Розмір індексу < 1GB на 100 документів

### User Experience
- ✅ Інтуїтивний UI (не потребує інструкцій)
- ✅ Зрозумілі error messages
- ✅ Responsive на desktop і mobile

## Timeline (орієнтовний)

### Week 1-2: Infrastructure & Backend
- Setup monorepo
- Docker Compose configuration
- NestJS API skeleton
- FastAPI ML service skeleton
- Database schemas

### Week 3-4: Core RAG Pipeline
- Document upload & processing
- Embeddings generation
- Weaviate integration
- Basic retrieval

### Week 5-6: LLM Integration & Sources
- OpenAI/LLM integration
- Prompt engineering
- Source citation logic
- Response formatting

### Week 7-8: Frontend & Polish
- Next.js UI
- Chat interface
- Document management
- Testing & bug fixes

## Пост-MVP плани

1. **Phase 2**: GraphRAG integration (4-6 weeks)
2. **Phase 3**: User authentication (2-3 weeks)
3. **Phase 4**: Analytics & monitoring (2-3 weeks)
4. **Phase 5**: Production deployment (3-4 weeks)

## Ризики та мітігації

| Ризик | Ймовірність | Вплив | Мітігація |
|-------|-------------|-------|-----------|
| LLM API costs | Висока | Середній | Використання локальної моделі як fallback |
| Векторний пошук повільний | Середня | Високий | Оптимізація chunking, індексів |
| Низька якість відповідей | Середня | Високий | Prompt engineering, тестування |
| Складність deployment | Низька | Середній | Docker Compose спрощує |

## Критерії готовності

MVP вважається готовим, якщо:

1. ✅ Всі Must Have функції імплементовані
2. ✅ Система працює без критичних багів
3. ✅ Демо можна показати stakeholders
4. ✅ Базова документація написана
5. ✅ Можливо отримати feedback від 5+ тестових користувачів
