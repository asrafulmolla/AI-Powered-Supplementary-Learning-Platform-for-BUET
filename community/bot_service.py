from courses.rag_service import RAGService

class BotService:
    @staticmethod
    def generate_reply(post_content):
        """
        Uses the RAG service to generate a helpful reply based on course materials.
        """
        rag = RAGService()
        # Treat the post content as a query
        answer_data = rag.generate_answer(post_content)
        
        reply_text = f"🤖 **(Auto-Bot)**: Hi! I noticed nobody replied yet. "
        reply_text += f"Here is some info from the course materials:\n\n{answer_data['answer']}\n\n"
        if answer_data.get('sources'):
             reply_text += "Ref: " + ", ".join([s['title'] for s in answer_data['sources']])
        
        return reply_text
