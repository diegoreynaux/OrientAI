"""
Testes E2E (Playwright) para validação do RAG (Retrieval-Augmented Generation).
"""
import pytest
from playwright.sync_api import Page, expect

def test_rag_displays_uncertainty_warning(page: Page):
    """
    Testa se o aviso de incerteza obrigatório é exibido 
    quando o LLM responde com base em RAG.
    """
    page.goto("http://localhost:8501")
    page.get_by_text("Chat com RAG").click()
    page.get_by_placeholder("Faça uma pergunta...").fill("Qual o objetivo da tese?")
    page.click('button:has-text("Enviar")')
    expect(page.locator('.uncertainty-warning')).to_be_visible()
    expect(page.locator('.uncertainty-warning')).to_contain_text("Esta resposta pode conter imprecisões.")
    pass

def test_rag_shows_source_citations(page: Page):
    """
    Testa se as respostas contêm citações rastreáveis para 
    os documentos fontes carregados pelo usuário.
    """
    page.goto("http://localhost:8501")
    page.get_by_text("Chat com RAG").click()
    page.click('button:has-text("Enviar")')
    expect(page.locator('.citation-badge')).to_have_count(1)
    pass
