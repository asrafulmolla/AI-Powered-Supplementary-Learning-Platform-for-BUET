import ast

class ContentValidator:
    def validate_code(self, code_content, language="python"):
        """
        Validates syntax of generated code.
        """
        if language.lower() == "python":
            try:
                ast.parse(code_content)
                return {"valid": True, "errors": []}
            except SyntaxError as e:
                return {"valid": False, "errors": [f"Line {e.lineno}: {e.msg}"]}
        
        # Determine strictness for other languages later
        return {"valid": True, "errors": []}

    def check_grounding(self, content, source_ids):
        """
        Checks if content is grounded in sources.
        """
        # Placeholder for RAG verification
        return {"grounded": True, "score": 0.9}
