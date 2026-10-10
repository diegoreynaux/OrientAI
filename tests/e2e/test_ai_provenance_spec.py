"""
Testes E2E (Playwright) para proveniência da IA (Provider/Model e Autoria).
"""
import pytest
from playwright.sync_api import Page, expect

def test_ai_provenance_badge_is_visible(page: Page):
    """
    Verifica se a interface exibe permanentemente o provedor 
    e o modelo (ex: OpenAI / GPT-4o) que gerou a resposta.
    """
    page.goto("http://localhost:8501")
    page.get_by_text("Chat com RAG").click()
    page.click('button:has-text("Enviar")')
    expect(page.locator('.ai-provenance-badge')).to_be_visible()
    expect(page.locator('.ai-provenance-badge')).to_contain_text("Gerado por:")
    pass

def test_visual_distinction_of_ai_content(page: Page):
    """
    Testa se no editor, o conteúdo gerado/sugerido pela IA
    tem uma distinção visual (ex: cor de fundo diferente ou borda).
    """
    page.goto("http://localhost:8501")
    page.get_by_text("Editor / Co-Revisão").click()
    expect(page.locator('.editor-ai-suggestion')).to_have_css("background-color", "rgb(239, 246, 255)")
    pass
