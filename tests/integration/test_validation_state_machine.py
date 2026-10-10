"""
Testa a máquina de estados da validação de documentos pelo orientador.
Garante que o ciclo (Aprovar, Rejeitar, Reprocessar) flui corretamente.
"""
import pytest

class DocumentState:
    """Representa o estado de um documento gerado pela IA."""
    PENDING = "Aguardando validação do orientador"
    APPROVED = "Aprovado"
    REJECTED = "Rejeitado"
    REPROCESSING = "Em reprocessamento"

class ValidationMachine:
    """Máquina de estado simplificada para os prontuários de reunião."""
    def __init__(self):
        self.state = DocumentState.PENDING

    def approve(self):
        """Aprova o documento, tornando-o visível ao orientando."""
        if self.state == DocumentState.PENDING:
            self.state = DocumentState.APPROVED

    def reject(self):
        """Rejeita o documento."""
        if self.state == DocumentState.PENDING:
            self.state = DocumentState.REJECTED

    def request_reprocessing(self):
        """Solicita reprocessamento pela IA."""
        if self.state in [DocumentState.PENDING, DocumentState.REJECTED]:
            self.state = DocumentState.REPROCESSING

def test_validation_approve():
    """Garante que a aprovação muda o estado para APROVADO."""
    doc = ValidationMachine()
    doc.approve()
    assert doc.state == DocumentState.APPROVED

def test_validation_reprocess():
    """Garante que solicitar reprocessamento muda o estado corretamente."""
    doc = ValidationMachine()
    doc.reject()
    doc.request_reprocessing()
    assert doc.state == DocumentState.REPROCESSING
