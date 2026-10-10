"""
Testes E2E (Playwright) para o portão de aprovação do orientador.
"""
import pytest
from playwright.sync_api import Page, expect

def test_advisor_must_approve_before_publishing(page: Page):
    """
    O fluxo exige que o orientador clique no botão de aprovar
    antes de um prontuário ir para o perfil do orientando.
    """
    page.goto("http://localhost:8501")
    page.get_by_text("Visão do Orientador").click()
    approve_button = page.locator('button:has-text("Validar e Publicar")')
    expect(approve_button).to_be_visible()
    approve_button.click()
    expect(page.locator('.status-badge-published')).to_have_text("Publicado")
    pass
