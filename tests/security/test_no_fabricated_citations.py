"""
Testes de segurança contra fabricação de citações.
"""
import pytest

class ReferenceValidator:
    """Serviço simulado que bloqueia geração de referências pelo LLM."""
    def validate_prompt(self, prompt: str) -> bool:
        """Impede prompts que peçam criação de referências inexistentes."""
        forbidden_keywords = ["crie uma referência", "invente um artigo"]
        return not any(kw in prompt.lower() for kw in forbidden_keywords)

def test_prompt_injection_for_citations_is_blocked():
    """Garante que pedidos de fabricação de referências são interceptados."""
    validator = ReferenceValidator()
    assert validator.validate_prompt("Resuma este texto.") == True
    assert validator.validate_prompt("Crie uma referência ABNT sobre IA") == False
