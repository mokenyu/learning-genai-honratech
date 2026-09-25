# Student Assessment Task: Prompt Engineering, LCEL & Compositional Chains

## 🎯 Objective
Construct a multi-stage technical documentation digest and automated translation pipeline using LangChain Expression Language (LCEL), `ChatPromptTemplate`, and `RunnableParallel`.

---

## 📋 Task Requirements

### 1. Multi-Turn Chat Template Design
- Construct a `ChatPromptTemplate` with:
  - A `SystemMessage` establishing a Senior Technical Editor persona.
  - A `MessagesPlaceholder(variable_name="history")` for conversational context.
  - A `HumanMessage` receiving a technical article or code snippet.

### 2. Parallel Processing with `RunnableParallel`
- Ingest raw technical text from `docs/sec_policy_204.txt`.
- Build an LCEL chain using `RunnableParallel` that simultaneously executes:
  1. **Executive Summary**: Produces a 3-bullet summary for C-level executives.
  2. **Technical Key Takeaways**: Extracts specific protocols, timeouts, and requirements.
  3. **Spanish Translation**: Translates the executive summary into Spanish.

### 3. Output Formatting & StrOutputParser
- Connect each parallel branch to a `StrOutputParser()`.
- Aggregate the parallel results into a unified markdown briefing.

### 4. Persistence
- Save the generated multi-language briefing to `docs/technical_digest.md`.

---

## 🏆 Submission Deliverables
1. Runnable Python script or notebook executing the LCEL pipeline.
2. The generated output file at `docs/technical_digest.md`.
