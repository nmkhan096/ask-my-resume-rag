# Ask My Resume

An interactive Q&A app that lets you query your resume using LLMs.

### Setup:
- **Vector DB**: Qdrant
- **Embedding**: Fastembed
- **LLM**: Groq OpenAI-compatible API
- **UI**: Streamlit

Features Included:
- Section filtering (multiselect)
- Adjustable retriever top_k slider
- “Sources Used” expander per answer
- User rating on each response (option to store for fine-tuning)

## Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/nmkhan096/ask-my-resume.git
cd ask-my-resume
```
### 2. Install dependencies
```
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```
### 3. Add .env file
```
# .env
GROQ_API_KEY=your_api_key
```

### 4. Run Qdrant with Docker
```
docker run -p 6333:6333 -p 6334:6334 \
   -v "$(pwd)/qdrant_storage:/qdrant/storage:z" \
   qdrant/qdrant
```

###  5. Parse your resume
Add your `.docx` resume to the `data/` folder
Run the parser script:
```
python rag_pipeline/parser.py "data/Resume.docx" \
    --sections "Work Experience" "Projects" "Education" "Skills" \
    --output "data/resume_chunks.json"
```
You can also import and use it in a notebook or script:
```
from rag_pipeline.parser import parse_resume_to_chunks

chunks = parse_resume_to_chunks("data/Resume.docx", ["Work Experience", "Projects"])
```

###  6. Load vectors into Qdrant
only run ONCE from the terminal to ingest data
```
python rag_pipeline/qdrant_setup.py \
  --input data/resume_chunks.json
```
OR in a notebook:
```
from rag_pipeline import qdrant_setup
qdrant_setup.setup_collection()
qdrant_setup.ingest_documents(docs)
qdrant_setup.create_section_index()
```

## RAG

Run the Streamlit app
```
streamlit run app.py
```

or run in test script
```
from rag_pipeline.rag import rag

print(rag("Summarise the key strengths"))
```
