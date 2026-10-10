"""
Testes de segurança e roteamento para dados sensíveis.
"""
import pytest

class DataRouter:
    """Mock do roteador que direciona requisições baseadas em sensibilidade."""
    def route_request(self, text: str, is_sensitive: bool) -> str:
        """Se o dado for sensível, força o uso de LLM local."""
        if is_sensitive:
            return "Routed to Ollama (Local)"
        return "Routed to OpenAI (Cloud)"

def test_sensitive_data_routes_to_local_llm():
    """Garante que dados classificados como sensíveis vão para o modelo local."""
    router = DataRouter()
    assert router.route_request("Projeto sigiloso", is_sensitive=True) == "Routed to Ollama (Local)"
    assert router.route_request("Conceitos gerais", is_sensitive=False) == "Routed to OpenAI (Cloud)"
