
Current Setup:
- Vector DB: Qdrant (via qdrant_client)
- Embedding: fastembed (Jina model)
- LLM: Groq OpenAI-compatible API (LLaMA 3)
- Logic: Custom vector_search(), build_prompt(), llm(), rag()
- UI: Streamlit


`rag_pipeline/parser.py` CLI Usage:
```
python rag_pipeline/parser.py "data/Nida_Khan_Resume.docx" \
    --sections "Work Experience" "Projects" "Education" "Skills" \
    --output "data/resume_chunks.json"
```
You can also import and use it programmatically:
```
from rag_pipeline.parser import parse_resume_to_chunks

chunks = parse_resume_to_chunks("data/Nida_Khan_Resume.docx", ["Work Experience", "Projects"])
```


### rag_pipeline/qdrant_setup.py with CLI support
`rag_pipeline/qdrant_setup.py` — only run ONCE to ingest data

usage:
```
python rag_pipeline/qdrant_setup.py \
  --input data/resume_chunks.json
```

Just run once from the terminal or a notebook:

### not needed
```
python rag_pipeline/qdrant_setup.py
```
OR in a notebook:
```
from rag_pipeline import qdrant_setup
qdrant_setup.setup_collection()
qdrant_setup.ingest_documents(docs)
qdrant_setup.create_section_index()
```


### RAG

run in test script
```
from rag_pipeline.rag import rag

print(rag("Summarise the key strengths"))
```