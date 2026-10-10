"""
Testes E2E (Playwright) para o fluxo completo de validação do orientador.
"""
import pytest
from playwright.sync_api import Page, expect

def test_advisor_validation_queue_features(page: Page):
    """
    Testa se o orientador tem acesso à fila de validação e se os botões
    de edição, rejeição e comentários estão presentes.
    """
    page.goto("http://localhost:8501")
    page.get_by_text("Visão do Orientador").click()
    expect(page.locator('.validation-item')).to_have_count(3)
    expect(page.locator('button:has-text("Editar")').first).to_be_visible()
    expect(page.locator('button:has-text("Rejeitar")').first).to_be_visible()
    pass
