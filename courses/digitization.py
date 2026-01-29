import google.generativeai as genai
from django.conf import settings

class DigitizationService:
    def __init__(self):
        self.api_key = getattr(settings, "GEMINI_API_KEY", None)
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        else:
            self.model = None

    def digitize(self, image_file):
        """
        Uses Gemini Vision to digitize handwritten notes from the actual image.
        """
        if not self.model:
            return "Gemini API Key missing."

        try:
            # Read the image content
            image_data = image_file.read()
            
            # Prepare the multimodal prompt
            prompt = "Digitize these handwritten engineering notes into a professional Markdown document. Use LaTeX for equations and formulas. Keep the structure clean and academic."
            
            # Pass both the prompt and the image data
            response = self.model.generate_content([
                prompt,
                {
                    "mime_type": image_file.content_type if hasattr(image_file, 'content_type') else "image/jpeg",
                    "data": image_data
                }
            ])
            
            return response.text.strip()
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg:
                return "⚠️ AI Quota Exceeded (429): The free tier limit has been reached. Please wait 1 minute and try again."
            return f"Digitization error: {error_msg}"
