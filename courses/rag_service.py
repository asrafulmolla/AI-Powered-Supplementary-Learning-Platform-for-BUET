import google.generativeai as genai
import json
from django.conf import settings
from .models import CourseMaterial
from django.db.models import Q

class RAGService:
    def __init__(self):
        self.api_key = getattr(settings, "GEMINI_API_KEY", None)
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        else:
            self.model = None

    def query_ai(self, prompt):
        """
        Helper to call Google Gemini API
        """
        if not self.model:
            return "Gemini API Key not configured. Please add GEMINI_API_KEY to settings.py."
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Error contacting Gemini Service: {str(e)}"

    def search(self, query):
        """
        Semantic-like search using keywords.
        """
        words = query.split()
        stop_words = {'tell', 'me', 'about', 'what', 'is', 'the', 'how', 'to', 'explain'}
        keywords = [w for w in words if w.lower() not in stop_words]
        
        if not keywords:
            return CourseMaterial.objects.none()

        q_objects = Q()
        for word in keywords:
            q_objects |= Q(title__icontains=word) | Q(description__icontains=word) | Q(text_content__icontains=word) | Q(tags__icontains=word)

        return CourseMaterial.objects.filter(q_objects).distinct()

    def get_context_string(self, results):
        context_docs = []
        for item in results[:5]:
            content = item.text_content or item.description
            context_docs.append(f"Source: {item.title}\nContent: {content}")
        return "\n\n".join(context_docs)

    def generate_answer(self, query):
        """
        Part 2 & 5: Conversational RAG.
        """
        results = self.search(query)
        context = self.get_context_string(results)
        
        prompt = f"""You are 'EduBot', a university academic assistant. 
Use the provided Course Materials context to answer the student's question accurately.

Context:
{context if context else 'No specific materials found.'}

Question: {query}

Instructions:
- If context is found, summarize it accurately and cite the source titles.
- If no materials are relevant, answer based on general knowledge but clarify it's not from the course.
- Keep the tone helpful and professional."""

        answer = self.query_ai(prompt)
        
        return {
            "answer": answer,
            "sources": [{"title": r.title, "id": r.id} for r in results[:5]]
        }

    def generate_learning_material(self, topic, material_type):
        """
        Part 3: Generated Learning Materials.
        """
        results = self.search(topic)
        context_str = self.get_context_string(results)
        
        if material_type == 'CODE':
            prompt = f"Write a clean, commented Python implementation for '{topic}'. Use the following course context if relevant:\n{context_str}\n\nOutput only the code, no markdown blocks."
        elif material_type == 'NOTE':
            prompt = f"Create structured study notes (Markdown) for '{topic}'. Use this course context:\n{context_str}"
        else:
            prompt = f"Outline a 5-slide presentation for '{topic}'. Include content for each slide. Context:\n{context_str}"

        content = self.query_ai(prompt)
        
        # Clean up potential markdown wrapper
        if "```" in content:
            import re
            match = re.search(r"```(?:\w+)?\n?(.*?)```", content, re.DOTALL)
            if match:
                content = match.group(1).strip()

        validation_result = None
        if material_type == 'CODE':
            from .validation import ContentValidator
            validator = ContentValidator()
            validation_result = validator.validate_code(content, language="python")

        return {"content": content, "validation": validation_result}

    def generate_quiz(self, topic):
        """Generate a 5-question MCQ quiz based on topic and context"""
        results = self.search(topic)
        context = self.get_context_string(results)
        prompt = f"""Based on the following context, generate a 5-question multiple choice quiz about '{topic}'.
        Context: {context}
        
        Format the output AS ONLY A JSON LIST with this structure:
        [
            {{
                "question": "question text",
                "options": ["A", "B", "C", "D"],
                "answer": "correct option",
                "explanation": "why this is correct"
            }}
        ]
        Return ONLY the JSON."""
        
        if not self.model:
            return []

        try:
            response = self.model.generate_content(prompt)
            import re
            # Extract JSON array using regex
            match = re.search(r"\[.*\]", response.text, re.DOTALL)
            if match:
                return json.loads(match.group(0))
            return []
        except Exception as e:
            return []

    def provide_bangla_explanation(self, topic):
        """Advanced Feature: Bangla explanation for complex concepts"""
        prompt = f"Explain the academic concept of '{topic}' in simple Bangla, specifically for a university student. Ensure technical terms are in English but the explanation is in Bangla. Highlight key BUET level insights."
        return self.query_ai(prompt)

    def generate_flashcards(self, topic):
        """Advanced Feature: AI Flashcard Generator"""
        prompt = f"""Generate 6 high-quality academic flashcards for the topic: {topic}.
        Format as a JSON list of objects with 'front' (question/concept) and 'back' (answer/explanation).
        Keep it concise and relevant for exam preparation.
        Return ONLY valid JSON."""
        
        if not self.model:
            return []

        try:
            response = self.model.generate_content(prompt)
            import re
            # Extract JSON array using regex
            match = re.search(r"\[.*\]", response.text, re.DOTALL)
            if match:
                return json.loads(match.group(0))
            return [{"front": "Error", "back": "AI response was not in expected format."}]
        except:
            return [{"front": "Error", "back": "Failed to generate cards. Try again."}]
