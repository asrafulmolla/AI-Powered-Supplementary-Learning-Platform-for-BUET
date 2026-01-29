import google.generativeai as genai
from django.conf import settings
import json
import re

class VideoService:
    def __init__(self):
        self.api_key = getattr(settings, "GEMINI_API_KEY", None)
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        else:
            self.model = None

    def generate_video_script(self, topic):
        """
        Uses Gemini to generate a video summary storyboard.
        """
        prompt = f"""
        Generate a video summary script and storyboard for a university student on the topic: '{topic}'.
        Return the result ONLY as a valid JSON object with the following structure:
        {{
            "title": "Title",
            "duration": "mm:ss",
            "scenes": [
                {{"time": "0:00-0:10", "visual": "Description", "audio": "Script"}},
                ... (at least 3 scenes)
            ]
        }}
        Do not include any markdown formatting or extra text outside the JSON.
        """
        
        if not self.model:
            return {"error": "Gemini API Key missing"}

        try:
            response = self.model.generate_content(prompt)
            raw_text = response.text.strip()
            
            # Clean up potential markdown wrapper
            if "```json" in raw_text:
                raw_text = raw_text.split("```json")[-1].split("```")[0].strip()
            elif "```" in raw_text:
                raw_text = raw_text.split("```")[-1].split("```")[0].strip()
                
            return json.loads(raw_text)
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg:
                return {
                    "title": "Quota Exceeded",
                    "duration": "0:00",
                    "scenes": [],
                    "error": "⚠️ AI Quota Exceeded (429): The free tier limit has been reached. Please wait 1 minute and try again."
                }
            return {
                "title": f"Video Explanation: {topic}",
                "duration": "1:30",
                "scenes": [
                    {"time": "0:00-0:30", "visual": "Intro Slide", "audio": f"Hi, let's learn about {topic}."},
                    {"time": "0:30-1:30", "visual": "Conceptual Diagram", "audio": "This is how part A connects to part B."}
                ],
                "error": error_msg
            }
