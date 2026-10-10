"""
Testes E2E (Playwright) para as justificativas de sugestões de escrita.
"""
import pytest
from playwright.sync_api import Page, expect

def test_suggestion_includes_rationale(page: Page):
    """
    Ao receber uma sugestão de co-revisão, o sistema deve
    explicar o critério utilizado (ex: 'clareza', 'abnt').
    """
    page.goto("http://localhost:8501")
    page.get_by_text("Editor / Co-Revisão").click()
    page.click('button:has-text("Revisar trecho")')
    expect(page.locator('.rationale-tooltip')).to_be_visible()
    expect(page.locator('.rationale-tooltip')).to_contain_text("Critério utilizado:")
    pass
