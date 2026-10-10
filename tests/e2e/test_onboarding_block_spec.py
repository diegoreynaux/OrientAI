"""
Testes E2E (Playwright) para o bloqueio de acesso sem onboarding.
"""
import pytest
from playwright.sync_api import Page, expect

def test_new_user_must_complete_onboarding(page: Page):
    """
    Um usuário recém cadastrado não pode acessar o sistema
    antes de concluir o treinamento obrigatório de IA responsável.
    """
    page.goto("http://localhost:8501")
    page.get_by_text("Dashboard (Onboarding)").click()
    modal_text = page.get_by_text("Treinamento Obrigatório OrientAI")
    expect(modal_text).to_be_visible()
    expect(page.locator('.dashboard-content')).not_to_be_visible()
    pass
