# Project Specification: Physical AI Textbook & RAG Chatbot

## 1. Overview
**Project Name:** Agentic AI Hackathon Entry
**Goal:** Create a comprehensive textbook for the "Physical AI & Humanoid Robotics" course, integrated with an intelligent RAG chatbot.
**Tools:** Spec-Kit Plus, Claude Code, Docusaurus, FastAPI, Qdrant, Gemini Flash.

## 2. User Stories
- **As a Student**, I want to read chapters about ROS 2 and Isaac Sim so that I can prepare for the capstone.
- **As a Developer**, I want to chat with the book using a floating widget so that I can get answers to specific technical questions.
- **As a User**, I want to translate the content into Urdu so that I can understand complex concepts in my native language.
- **As a Learner**, I want to personalize the content (Simplify/Deep Dive) to match my current knowledge level.

## 3. Technical Architecture
### Frontend
- **Framework:** Docusaurus (React)
- **Deployment:** GitHub Pages
- **Interactivity:** Custom `ChatWindow.js` component for Chat, Translation, and Personalization.

### Backend
- **Framework:** FastAPI (Python)
- **Database:** Qdrant Cloud (Vector Store)
- **AI Model:** Google Gemini 1.5 Flash (via OpenAI-compatible interface).
- **Embeddings:** Text-Embedding-004 (via OpenAI-compatible interface).

## 4. Success Metrics
- [x] Website deployed and accessible.
- [x] Chatbot answers questions accurately using RAG.
- [x] Translation feature converts text to Urdu.
- [x] Personalization feature rewrites text for different skill levels.