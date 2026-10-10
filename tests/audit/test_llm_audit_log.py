"""
Testes de infraestrutura de logs e auditoria.
"""
import pytest
from datetime import datetime

class AuditLogger:
    """Gera logs imutáveis e padronizados de interação com o LLM."""
    def __init__(self):
        self.logs = []

    def log_interaction(self, user_id, module, model):
        """Registra a interação contendo usuário, módulo, modelo, data e hora."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "module": module,
            "model": model
        }
        self.logs.append(entry)
        return entry

def test_audit_log_contains_required_fields():
    """Verifica se o log salva todas as propriedades exigidas pela governança."""
    logger = AuditLogger()
    entry = logger.log_interaction(user_id="prof_123", module="Co-Revisao", model="gpt-4o")
    
    assert "timestamp" in entry
    assert entry["user_id"] == "prof_123"
    assert entry["module"] == "Co-Revisao"
    assert entry["model"] == "gpt-4o"
