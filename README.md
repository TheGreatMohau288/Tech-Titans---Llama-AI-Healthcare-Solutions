# Tech Titans - Healthcare AI Hackathon Project

Welcome to the Tech Titans repository for the WeThinkCode Hackathon. Our team is developing an innovative AI solution leveraging the Llama API to tackle critical healthcare problems.

## Project Overview

Our project leverages the power of the Llama API to enhance personalized medicine and patient care by analyzing diverse health data sources, including medical history, real-time vital signs, and lifestyle factors. The solution aims to provide:

- Real-time patient monitoring with proactive alerts for early intervention
- Data-driven insights to optimize treatment plans
- The ability to transform unstructured clinical notes into clear, concise, and structured medical summaries. 
- AI-powered assistance to support healthcare providers and patients alike
- Access so that clinicians can upload or paste notes, and the system will automatically extract key information such as symptoms, vital signs, diagnoses, medications, test results, and follow-up plans.
- Produces patient-friendly summaries for easier communication.

By automating note summarization, CNSA reduces administrative burden, accelerates clinical decision-making, and enhances the accuracy and clarity of documentation.

## Features

- Upload or paste clinician notes (text or PDF)
- Generate structured clinical summaries
- Produce patient-friendly summaries
- Export results in PDF or JSON format for EHR integration
- Fast, local AI processing using Meta LLaMA via Ollama

## Technical Architecture

- Frontend Layer – Provides text input, file upload, buttons to generate summaries, and display panels for clinician and patient outputs.
- Backend Layer – Handles logic, formats prompts, sends notes to LLaMA via Ollama, validates, and structures outputs.
- AI Processing Layer – Normalizes medical text, extracts entities, summarizes notes, and generates structured JSON outputs.
- Data Handling & Security – In-memory processing only, no long-term storage, input/output sanitization, optional HTTPS.
- Output Layer – Produces structured summaries, patient-friendly text, PDF exports, and JSON outputs for EHR compatibility.

## Technologies Used

- Llama API (Meta's advanced language model)
- HTML, CSS, and JavaScript
- Python and RESTful APIs for integrations
- SQLite for data management
- Cloud deployment for scalability

## Getting Started

1. Clone this repository
2. Install required dependencies
3. Configure API keys and environment variables for Llama API access
4. Run the application locally or deploy to your preferred platform

## Contribution

We welcome contributions from developers/students passionate about healthcare innovation. Please open issues for bug reports or feature requests and submit pull requests for proposed changes.

## License

This project is licensed under the MIT License.

---

For additional context, Llama AI significantly boosts healthcare solutions by enabling precise patient monitoring and personalized treatment adjustments, which form the foundation of our hackathon project.

