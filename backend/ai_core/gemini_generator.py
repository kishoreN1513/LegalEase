import os
from dotenv import load_dotenv

load_dotenv()

class GeminiDocumentGenerator:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")
        self.model = None
        if self.api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel(self.model_name)
            except Exception:
                self.model = None

    def generate_document(self, document_type, parties, terms, dates):
        if self.model:
            prompt = (
                "Create a professional draft legal document.\n"
                f"Document type: {document_type}\n"
                f"Parties: {parties}\n"
                f"Effective date: {dates}\n"
                f"Terms and conditions: {terms}\n"
                "Return clear sections, headings, numbered clauses, and a signature section. "
                "Use neutral drafting language. This is a draft for review, not legal advice."
            )
            try:
                response = self.model.generate_content(prompt)
                if getattr(response, "text", None):
                    return response.text.strip()
            except Exception:
                pass
        return self._fallback(document_type, parties, terms, dates)

    def _fallback(self, document_type, parties, terms, dates):
        clauses = [x.strip() for x in terms.split(";") if x.strip()]
        clause_text = "\n".join(
            f"{i}. {c}" for i, c in enumerate(clauses, 1)
        ) or "1. The parties agree to the terms mutually documented by them."
        return (
            f"LEGAL DOCUMENT — {document_type.upper()}\n\n"
            f"1. PARTIES\n{parties}\n\n"
            f"2. EFFECTIVE DATE\n{dates}\n\n"
            f"3. PURPOSE\nThis draft {document_type} records the understanding between the parties identified above.\n\n"
            f"4. TERMS AND CONDITIONS\n{clause_text}\n\n"
            "5. GENERAL PROVISIONS\n"
            "The parties acknowledge that this document should be reviewed and customized for their specific circumstances.\n\n"
            "6. SIGNATURES\n\n"
            "Party 1: ______________________________\n"
            "Name: _________________________________\n"
            "Date: __________________________________\n\n"
            "Party 2: ______________________________\n"
            "Name: _________________________________\n"
            "Date: __________________________________\n\n"
            "DISCLAIMER\n"
            "This generated document is a draft for informational and drafting purposes only and is not legal advice.\n"
        )
