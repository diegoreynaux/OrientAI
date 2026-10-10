"""
Testes de failover para o Gateway de LLM.
Verifica se o sistema alterna automaticamente para um provedor secundário ou local em caso de falha.
"""
import pytest

class ResilientLLMGateway:
    """Mock de Gateway com capacidade de failover automático."""
    def __init__(self):
        self.primary = "openai"
        self.secondary = "anthropic"
        self.fallback_local = "ollama"
        self.simulated_outages = []

    def simulate_outage(self, provider: str):
        """Simula a queda de um provedor."""
        self.simulated_outages.append(provider)

    def generate_with_fallback(self, prompt: str) -> str:
        """Tenta gerar o texto, fazendo fallback em caso de falha."""
        for provider in [self.primary, self.secondary, self.fallback_local]:
            if provider not in self.simulated_outages:
                return f"Success via {provider}"
        raise Exception("Todos os provedores falharam.")

def test_failover_to_secondary():
    """Testa a transição do primário para o secundário quando o primário cai."""
    gateway = ResilientLLMGateway()
    gateway.simulate_outage("openai")
    
    res = gateway.generate_with_fallback("Teste")
    assert res == "Success via anthropic"

def test_failover_to_local_ollama():
    """Testa a transição para o provedor local (Ollama) quando ambos externos caem."""
    gateway = ResilientLLMGateway()
    gateway.simulate_outage("openai")
    gateway.simulate_outage("anthropic")
    
    res = gateway.generate_with_fallback("Teste privacy")
    assert res == "Success via ollama"
