# Student Assessment Task: Context Engineering & Retrieval-Augmented Generation (RAG)

## 🎯 Objective
Construct a fully grounded enterprise compliance assistant using LangChain, dense embeddings, vector store retrieval, and source attribution, ingesting enterprise policies from the `docs/` folder.

---

## 📋 Task Requirements

### 1. Document Ingestion & Chunking
- Ingest policy documents from `docs/sec_policy_204.txt` and `docs/ops_policy_501.txt`.
- Apply `RecursiveCharacterTextSplitter` with `chunk_size = 200` and `chunk_overlap = 30`.
- Preserve source metadata pointing to the respective `docs/` file paths.

### 2. Embeddings & Vector Store Indexing
- Initialize dense embeddings (`GoogleGenerativeAIEmbeddings` or `OpenAIEmbeddings`).
- Index the document chunks into an `InMemoryVectorStore` or `Chroma` database.
- Configure a retriever to fetch the top 2 most relevant chunks (`k=2`).

### 3. Grounded LCEL RAG Chain
- Create a `ChatPromptTemplate` that strictly instructs the model to answer only based on the retrieved context and cite source document names.
- Assemble the LCEL chain: `{"context": retriever | format_docs, "question": RunnablePassthrough()} | prompt | model | StrOutputParser()`.

### 4. Hallucination Guardrail Verification
- Test query A (In-domain): *"What is the policy for emergency break-glass access?"* -> Verify grounded answer with citation.
- Test query B (Out-of-domain): *"What is the CEO's stock grant vesting schedule?"* -> Verify the model refuses to hallucinate and indicates the information is not in the documentation.

### 5. Architectural Comparison Analysis
- Include a 1-page markdown report defending why RAG was chosen for this problem over Fine-Tuning and System Prompting, evaluating freshness, data privacy, and hallucination risk.
- Save the analysis report to `docs/rag_architecture_defense.md`.

---

## 🏆 Submission Deliverables
1. Runnable script or notebook executing the RAG pipeline.
2. The generated analysis report in `docs/rag_architecture_defense.md`.
