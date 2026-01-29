# AI-Powered Supplementary Learning Platform 🎓🤖
### BUET CSE FEST 2026 - Hackathon Submission

An advanced, AI-driven educational ecosystem designed to unify fragmented course resources (slides, PDFs, lab codes) into a structured, searchable, and interactive experience for university students and instructors.

---

## 🚀 core Features

### 1. Unified Content Management (CMS)
- **Categorization**: Organize materials into **Theory** and **Lab** tracks.
- **Versatile Support**: Upload and manage Lecture Slides, PDFs, Code Files, and Supplementry Notes.
- **Rich Metadata**: Supports topic-wise tagging, weekly organization, and content-type filtering.

### 2. Intelligent Search (Syntax-Aware RAG)
- **Semantic Retrieval**: Natural language search powered by **Gemini 2.5 Flash**.
- **Keyword Expansion**: Automatically expands user queries for higher accuracy.
- **Syntax-Aware Ranking**: System recognizes coding queries and prioritizes Lab/Code materials.
- **Source Grounding**: Every answer displays the exact source and excerpt from the course database.

### 3. AI-Generated Materials (Dynamic Learning)
- **Automatic Notes/Slides**: Generate comprehensive reading notes or presentation outlines from existing documents.
- **Context Fusion**: Combines **Internal Course Data** with **External Knowledge (Wikipedia)** for a 360-degree learning experience.
- **Lab Code Generation**: Generates syntactically correct Python implementations grounded in course concepts.

### 4. Validation & Quality Control
- **Syntax Linting**: Automated code validation using Python's `ast` library.
- **Reference Grounding**: Self-evaluation mechanism to ensure AI outputs aren't hallucinating and are academically reliable.

### 5. Conversational "EduBot" Interface
- **Contextual Chat**: Ask follow-up questions, request summaries, or generate materials through a persistent AI chat experience.
- **Integrated HUB**: The chat acts as an alternative interaction layer for all system features.

### 6. Premium Bonus Features 🌟
- **Handwritten Notes Digitization**: snap a photo of classroom notes/boards and convert them into digital Markdown/LaTeX documents.
- **AI Video Symphony**: Convert complex course topics into cinematic video storyboards and summary scripts.
- **Community Board with AI Bot**: A social hub for students to discuss problems, with a bot that automatically provides grounded answers to unanswered questions.

---

## 🛠️ Technology Stack
- **Backend**: Python 3.11, Django 5.2, Django REST Framework
- **Frontend**: Premium Vanilla CSS (Rich Glassmorphism UI), HTML5, Remix Icons
- **AI/LLM**: Google Gemini 2.5 Flash (Generative AI & Vision)
- **External Integration**: Wikipedia API for Encyclopedic Context
- **Tools**: `html2pdf.js` for document exports, `ast` for code linting

---

## ⚙️ Installation & Setup

1. **Clone the Project**:
   ```bash
   git clone <repository-url>
   cd BUET-CSE-FEST-2026
   ```

2. **Environment Variables**:
   Create a `.env` file in the root directory and add your Gemini API Key:
   ```env
   GEMINI_API_KEY=your_google_gemini_api_key_here
   SECRET_KEY=your_django_secret_key
   DEBUG=True
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Setup**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create Superadmin** (Optional but recommended):
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the Server**:
   ```bash
   python manage.py runserver
   ```
   Access the app at `http://127.0.0.1:8000/`

---

## 📖 Usage Guide
- **Students**: Can browse the library, use the AI Chat, Digitizer, and Video Gen tools.
- **Instructors/TAs**: Access the "Instructor Tools" section to upload materials and generate NEW course content from topics.
- **Community**: Ask questions in the Community Board to get help from peers or the EduBot.

---

## 🛡️ Content Validation Strategy
Generated content undergoes a 3-step validation:
1. **Linter**: Only syntactically correct code is shown.
2. **Grounding**: The RAG service forces citations from uploaded PDFs/Slides.
3. **External Sync**: Cross-referencing technical definitions with Wikipedia API.

---

## 🏆 Hackathon Details
- **Event**: BUET CSE FEST 2026
- **Theme**: Intelligent Academic Assistant

*Developed with ❤️ for Team Polaris*
