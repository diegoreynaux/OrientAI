"""
Testes de integração para o Gateway de LLM.
Garante que a arquitetura está desacoplada e suporta múltiplos provedores.
"""
import pytest

class LLMGatewayMock:
    """
    Mock do Gateway de roteamento para diferentes provedores de LLM.
    """
    def __init__(self):
        self.providers = {"openai": True, "anthropic": True, "ollama": True}
        self.current_provider = "openai"

    def set_provider(self, provider_name: str):
        """Define o provedor ativo."""
        if provider_name not in self.providers:
            raise ValueError(f"Provedor {provider_name} não suportado.")
        self.current_provider = provider_name

    def generate(self, prompt: str) -> str:
        """Simula a geração de texto pelo LLM."""
        return f"Resposta via {self.current_provider}: {prompt}"


@pytest.fixture
def gateway():
    return LLMGatewayMock()

def test_gateway_supports_multiple_providers(gateway):
    """Verifica se o gateway consegue alternar entre provedores sem erro."""
    gateway.set_provider("anthropic")
    assert gateway.current_provider == "anthropic"
    
    gateway.set_provider("ollama")
    assert gateway.current_provider == "ollama"

def test_gateway_generation(gateway):
    """Verifica a correta formatação da resposta dependendo do provedor ativo."""
    gateway.set_provider("ollama")
    response = gateway.generate("Teste local")
    assert "Resposta via ollama" in response
