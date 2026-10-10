"""
Testes E2E (Playwright) para edição parcial e diff de texto.
"""
import pytest
from playwright.sync_api import Page, expect

def test_partial_edit_shows_diff(page: Page):
    """
    Ao editar uma resposta gerada pela IA, o orientador consegue
    ver o diff (comparação) visual entre a proposta da IA e sua versão.
    """
    page.goto("http://localhost:8501")
    page.get_by_text("Visão do Orientador").click()
    page.click('button:has-text("Visualizar Diff")')
    expect(page.locator('.diff-added')).to_be_visible()
    expect(page.locator('.diff-removed')).to_be_visible()
    pass
