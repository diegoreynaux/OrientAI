"""
Testes E2E (Playwright) para visibilidade de pendências e marcas d'água.
"""
import pytest
from playwright.sync_api import Page, expect

def test_student_sees_watermark_on_pending_documents(page: Page):
    """
    O orientando visualiza um prontuário recém-gerado, mas com
    uma marca d'água explícita de que carece de validação.
    """
    page.goto("http://localhost:8501")
    page.get_by_text("Visão do Aluno").click()
    watermark = page.locator('.watermark-overlay')
    expect(watermark).to_be_visible()
    expect(watermark).to_have_text("Aguardando validação do orientador")
    pass
