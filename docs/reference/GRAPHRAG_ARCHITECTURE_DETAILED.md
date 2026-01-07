# GraphRAG Architecture - Детальний опис

## Що таке GraphRAG?

GraphRAG (Graph Retrieval-Augmented Generation) - це розширення традиційного RAG, що використовує графові структури для покращення якості пошуку та генерації відповідей.

## Переваги GraphRAG над традиційним RAG

1. **Контекстуальні зв'язки**: розуміння відношень між концепціями
2. **Multi-hop reasoning**: здатність робити висновки через кілька кроків
3. **Кращий контекст**: збереження семантичних зв'язків між фрагментами
4. **Точніші джерела**: трейсинг логічного ланцюжка до джерел

## Архітектура

### 1. Етап індексації

```
Document → Chunking → Entity Extraction → Relationship Detection
                                ↓                    ↓
                           Neo4j Graph         Embeddings
                                ↓                    ↓
                          Graph Structure       Weaviate
```

#### Entity Extraction
- Named Entity Recognition (NER)
- Ключові концепції
- Метадані (автор, дата, категорія)

#### Relationship Detection
- Семантичні зв'язки
- Цитування/посилання
- Ієрархічні відношення

### 2. Етап retrieval

```
Query → Query Analysis → Graph Traversal + Vector Search
            ↓                        ↓
     Entity Detection         Hybrid Results
            ↓                        ↓
     Subgraph Extraction       Re-ranking
                                     ↓
                            Contextualized Chunks
```

### 3. Етап генерації

```
Contextualized Chunks → Prompt Construction → LLM
         +                       ↓              ↓
    Graph Context           Rich Prompt    Response
                                           +
                                      Source Citations
                                           +
                                      Relationship Map
```

## Приклад GraphRAG flow

**Query**: "Як React Hooks впливають на performance?"

1. **Entity Detection**: [React, Hooks, Performance]
2. **Graph Traversal**: 
   - Знайти всі документи про React Hooks
   - Знайти зв'язки з Performance topics
   - Знайти приклади/кейси
3. **Vector Search**: семантичний пошук по "hooks performance"
4. **Merge & Re-rank**: об'єднати результати з обох джерел
5. **Generate**: згенерувати відповідь з контекстом графа

## Імплементація у CiteWise RAG

### MVP Phase (без Neo4j)
- Простий RAG з Weaviate
- Метадані в PostgreSQL
- Базовий source tracking

### Phase 2 (з Neo4j)
- Entity extraction при індексації
- Graph storage в Neo4j
- Hybrid retrieval (graph + vector)
- Visual relationship display

### Phase 3 (Advanced)
- Automated graph updates
- Community detection
- Temporal graphs
- Knowledge graph reasoning

## Технічний стек

- **Graph DB**: Neo4j
- **Vector DB**: Weaviate
- **NLP**: spaCy / transformers для entity extraction
- **Graph algorithms**: Neo4j GDS (Graph Data Science)
- **Visualization**: D3.js / Cytoscape.js

## Метрики успіху

- Relevance@k порівняно з baseline RAG
- Citation accuracy
- Query latency
- User satisfaction scores

## Виклики та рішення

### Виклик 1: Latency
**Рішення**: 
- Кешування subgraphs
- Parallel execution (graph + vector)
- Incremental graph updates

### Виклик 2: Graph quality
**Рішення**:
- Supervised entity extraction
- Relationship confidence scores
- Human-in-the-loop validation

### Виклик 3: Scalability
**Рішення**:
- Sharded graphs
- Approximate graph algorithms
- Hybrid approach (critical paths in graph, bulk in vector)
