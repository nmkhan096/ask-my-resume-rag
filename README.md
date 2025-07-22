# Ask My Resume

An interactive Q&A app that lets you query your resume using LLMs and vector search.

### Tech Stack:
- **Vector DB**: Qdrant (served via Docker)
- **Embedding**: FastEmbed
- **LLM**: Groq API (OpenAI-compatible API)   
- **UI**: Streamlit

### Interface Overview:

![Demo](demo/demo.gif)

Key features include:
- A **sidebar** to:
  - Select the LLM model to use
  - Filter which resume sections to search
  - Adjust the number of context chunks retrieved (`top_k`)

- A **chat interface** where you can:
  - Ask the LLM questions about your resume
  - View the **source citations** under each response
  - Rate each answer with a 👍 / 👎 feedback
    
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
To run a Qdrant instance in a Docker container, first pull the image and start the container:
```
docker pull qdrant/qdrant

docker run -p 6333:6333 -p 6334:6334 \
   -v "$(pwd)/qdrant_storage:/qdrant/storage:z" \
   qdrant/qdrant
```

###  5. Parse your resume
Add your resume (`.docx` file) to the `data/` folder and run the parser script.

- from CLI:
```
python rag_pipeline/parser.py "data/Resume.docx" \
    --sections "Work Experience" "Projects" "Education" "Skills" \
    --output "data/resume_chunks.json"
```
- in a notebook / script:
```
from rag_pipeline.parser import parse_resume_to_chunks

chunks = parse_resume_to_chunks("data/Resume.docx", ["Work Experience", "Projects"])
```

###  6. Load vectors into Qdrant
only run ONCE to ingest data:
- CLI
```
python rag_pipeline/qdrant_setup.py \
  --input data/resume_chunks.json
```
- notebook:
```
from rag_pipeline import qdrant_setup
qdrant_setup.setup_collection()
qdrant_setup.ingest_documents(docs)
qdrant_setup.create_section_index()
```

### 7. Run the Streamlit app
- CLI
```
streamlit run app.py
```

- notebook:
```
from rag_pipeline.rag import rag

print(rag("Summarise the key strengths"))
```

## Example Questions
Ask questions like:
- *“What projects show my data science skills?”*
- *“How well does my experience match this job description?”*
- *“Summarize my strengths for a software engineering role.”*
