# Student Assessment Task: Core Runtime, Agentic Primitives & Multimodal Systems

## 🎯 Objective
In this assessment, you will build an end-to-end multimodal incident response agent that inspects an architecture diagram in `docs/image.png`, analyzes a real-time system log in `docs/system_activity.log`, and generates a remediation action plan written directly to `docs/incident_report.md`.

---

## 📋 Task Requirements

### 1. Model Configuration & Temperature Tuning
- Initialize a multimodal model (`gemini-2.5-flash` or `gpt-4o`) using `langchain_google_genai` or `langchain_openai`.
- Explicitly configure the model parameters:
  - `temperature = 0.1` (to guarantee deterministic and precise diagnostic results).
  - `max_output_tokens = 1500`.

### 2. Multimodal Local Image Inspection
- Encode the existing architecture diagram located at `docs/image.png` into Base64 format.
- Construct a `HumanMessage` that supplies both the encoded image Data URI and a prompt asking the model to map out each active service and its respective port and status.

### 3. File Manipulation & Log Analysis
- Read the system log file from `docs/system_activity.log`.
- Pass the log content along with the visual analysis context to the model to detect root causes, error cascades, and failing services.

### 4. Custom Tool Integration
- Implement a custom `@tool` named `restart_service(service_name: str, port: int) -> str` that simulates triggering a service restart and returning a confirmation status.
- Bind the tool to the model and execute the ReAct loop if the model determines a service restart is needed.

### 5. Response Persistence
- Write the final synthesis report and mitigation log into `docs/incident_report.md`.
- Verify that `docs/incident_report.md` exists and contains non-empty analysis.

---

## 🏆 Submission Deliverables
1. A single runnable Python script or Jupyter notebook demonstrating all 5 steps.
2. The generated output file in `docs/incident_report.md`.
