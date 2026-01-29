import google.generativeai as genai
import json
import requests
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

    def get_wikipedia_context(self, query):
        """
        External context tool: simulating an MCP server wrapper over Wikipedia.
        """
        try:
            url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&exintro&explaintext&redirects=1&titles={query}"
            response = requests.get(url, timeout=5)
            data = response.json()
            pages = data['query']['pages']
            page_id = next(iter(pages))
            if page_id != "-1":
                return pages[page_id]['extract'][:1000]
            return None
        except:
            return None

    def query_ai(self, prompt):
        """
        Helper to call Google Gemini API with improved error handling.
        """
        if not self.model:
            return "Gemini API Key not configured. Please add GEMINI_API_KEY to settings.py."
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg:
                return "⚠️ AI Quota Exceeded (429): The free tier limit has been reached. Please wait 30-60 seconds and try again, or use a different API key."
            return f"Error contacting Gemini Service: {error_msg}"

    def search(self, query):
        """
        Intelligent search with Keyword Expansion and Syntax-Aware filtering.
        """
        # Part 1: Semantic Expansion (ask Gemini for keywords if it's a complex query)
        expanded_keywords = [query]
        if len(query.split()) > 3:
            expansion_prompt = f"Given the educational query '{query}', list 5-7 core technical keywords or synonyms that would help find relevant course materials or code snippets. Return ONLY keywords separated by commas."
            expanded_text = self.query_ai(expansion_prompt)
            if "Error" not in expanded_text:
                expanded_keywords.extend([k.strip() for k in expanded_text.split(',')])
        else:
            # For small queries, strip stop words for better DB matching
            stop_words = {'tell', 'me', 'about', 'what', 'is', 'the', 'how', 'to', 'explain', 'simply', 'write'}
            words = query.split()
            keywords = [w for w in words if w.lower() not in stop_words]
            if keywords:
                expanded_keywords.extend(keywords)

        # Part 2: Syntax-Aware Detection
        # If query contains programming keywords, prioritize 'CODE' file types
        code_indicators = {'code', 'def', 'function', 'implementation', 'syntax', 'error', 'debug', 'class', 'struct', 'programming'}
        is_code_search = any(word.lower() in code_indicators for word in query.split())

        # Part 3: Search Execution
        q_objects = Q()
        for word in expanded_keywords:
            if len(word) > 2:
                q_objects |= Q(title__icontains=word) | Q(description__icontains=word) | Q(text_content__icontains=word) | Q(tags__icontains=word)

        results = CourseMaterial.objects.filter(q_objects).distinct()

        # Part 4: Ranking/Prioritization
        results_list = list(results[:20])
        if is_code_search:
            # Sort CODE materials to the top
            results_list = sorted(results_list, key=lambda x: 0 if x.file_type == 'CODE' else 1)
        
        return results_list[:10]

    def get_context_with_excerpts(self, results):
        context_docs = []
        for item in results:
            content = item.text_content or item.description
            # Create a small excerpt (first 300 chars)
            excerpt = content[:300] + "..." if len(content) > 300 else content
            context_docs.append({
                "title": item.title,
                "excerpt": excerpt,
                "type": item.get_file_type_display(),
                "id": item.id
            })
        return context_docs

    def get_context_string(self, results):
        context_docs = []
        for item in results[:5]:
            content = item.text_content or item.description
            context_docs.append(f"Source: {item.title}\nContent: {content}")
        return "\n\n".join(context_docs)

    def generate_answer(self, query):
        """
        Part 2: Intelligent RAG-Based Search & Answer with External Context.
        """
        results = self.search(query)
        excerpts = self.get_context_with_excerpts(results)
        
        # Build internal context
        internal_context = "\n\n".join([f"Source: {res['title']}\nContent: {res['excerpt']}" for res in excerpts])
        
        # Part 3 Requirement: Fetch external context if needed
        external_context = ""
        if len(excerpts) < 2:
            wiki = self.get_wikipedia_context(query)
            if wiki:
                external_context = f"External Source (Wikipedia):\n{wiki}"

        prompt = f"""You are 'EduBot', a university academic assistant. 
Use the following context to answer the student's question accurately.

Internal Course Materials:
{internal_context if internal_context else 'No specific materials found in the internal library.'}

{external_context if external_context else ''}

Question: {query}

Instructions:
- Prioritize internal course materials if they are relevant.
- Use external context only for gaps or additional depth.
- Cite sources clearly (Internal Title or Wikipedia).
- If it's a coding question, provide a structured explanation.
- Keep the tone helpful, professional, and technical."""

        answer = self.query_ai(prompt)
        
        return {
            "answer": answer,
            "sources": excerpts 
        }

    def generate_learning_material(self, topic, material_type):
        """
        Part 3: Generated Learning Materials using Internal & External Context.
        """
        results = self.search(topic)
        internal_context = self.get_context_string(results)
        external_context = self.get_wikipedia_context(topic) or "No external data found."
        
        full_context = f"INTERNAL COURSE CONTEXT:\n{internal_context}\n\nEXTERNAL ENCYCLOPEDIC CONTEXT:\n{external_context}"

        if material_type == 'CODE':
            prompt = f"Write a clean, commented Python implementation for '{topic}'. Ground your code in this context:\n{full_context}\n\nOutput only the code, no markdown blocks."
        elif material_type == 'NOTE':
            prompt = f"Create structured study notes (Markdown) for '{topic}'. Use both internal and external context for a comprehensive guide:\n{full_context}"
        else:
            prompt = f"Outline a 5-slide presentation for '{topic}'. Include content for each slide. Context:\n{full_context}"

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
