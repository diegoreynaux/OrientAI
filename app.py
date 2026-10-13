import streamlit as st
from onboarding import render_onboarding

st.set_page_config(page_title="OrientAI - OrientAI", layout="wide")

# Usaremos injeção de HTML/CSS seguro para simular os badges e alertas exigidos pelo OrientAI
st.markdown("""
<style>
    .uncertainty-warning { color: #dc2626; font-weight: bold; font-size: 0.9em; padding: 10px; background-color: #fee2e2; border-radius: 5px; margin-bottom: 10px; border-left: 4px solid #dc2626; }
    .ai-provenance-badge { font-size: 0.75em; color: #6b7280; margin-top: 8px; font-style: italic; }
    .citation-badge { background-color: #fef08a; padding: 2px 4px; border-radius: 4px; font-size: 0.8em; color: #854d0e; }
    .editor-ai-suggestion { background-color: #eff6ff; color: #1e3a8a; border-bottom: 2px solid #60a5fa; padding: 2px; }
    .rationale-tooltip { background-color: #1f2937; color: white; padding: 10px; border-radius: 5px; margin-top: 10px; font-size: 0.9em; }
    .status-badge { background-color: #fef08a; color: #854d0e; padding: 2px 6px; border-radius: 12px; font-size: 0.8em; font-weight: bold; }
    .status-badge-published { background-color: #bbf7d0; color: #166534; padding: 2px 6px; border-radius: 12px; font-size: 0.8em; font-weight: bold; }
    .watermark-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; display: flex; justify-content: center; align-items: center; pointer-events: none; z-index: 9999; }
    .watermark-text { color: rgba(239, 68, 68, 0.2); font-weight: bold; font-size: 5rem; transform: rotate(-45deg); text-align: center; line-height: 1.1; }
    .diff-removed { color: #dc2626; background-color: #fee2e2; padding: 2px; font-family: monospace; }
    .diff-added { color: #166534; background-color: #dcfce3; padding: 2px; font-family: monospace; }
</style>
""", unsafe_allow_html=True)

st.sidebar.image("https://cdn-icons-png.flaticon.com/512/4240/4240833.png", width=50)
st.sidebar.markdown("### OrientAI")
st.sidebar.markdown("---")
menu = st.sidebar.radio("Navegação", ["Dashboard (Onboarding)", "Chat com RAG", "Editor / Co-Revisão", "Visão do Orientador", "Visão do Aluno"])
st.sidebar.markdown("---")
st.sidebar.caption("🔒 Protegido pelas políticas OrientAI")

if menu == "Dashboard (Onboarding)":
    from onboarding import render_onboarding
    render_onboarding()

elif menu == "Chat com RAG":
    st.title("Chat com a Pesquisa (RAG) 📚")
    
    st.info("Simulação do módulo de chat que busca informações nos PDFs da sua pesquisa.")
    
    # Fake history
    with st.chat_message("user"):
        st.write("Quais são os principais autores da minha fundamentação teórica?")
    with st.chat_message("assistant"):
        st.write("Com base nos documentos fornecidos, os principais autores citados são Foucault e Bourdieu.")
    
    st.markdown("---")
    
    query = st.text_input("Faça uma pergunta...", placeholder="Faça uma pergunta...")
    if st.button("Enviar", key="btn_enviar"):
        st.markdown("""
            <div style="border-left: 4px solid #3b82f6; padding-left: 10px; margin-top: 20px;">
                <div class="uncertainty-warning">Esta resposta pode conter imprecisões. Verifique as fontes primárias antes de incorporar ao trabalho acadêmico.</div>
                <p>A metodologia baseia-se na abordagem fenomenológica <span class="citation-badge">[Ref: Heidegger, p.42]</span>.</p>
                <div class="ai-provenance-badge">Gerado por: OpenAI GPT-4o</div>
            </div>
        """, unsafe_allow_html=True)


elif menu == "Editor / Co-Revisão":
    st.title("Editor Acadêmico & Co-Revisão 📝")
    st.info("O editor integrado permite que a IA sugira melhorias na sua tese, mas o controle é 100% seu.")
    st.write("Trecho atual do seu texto:")
    
    st.markdown("""
        <div style="border: 1px solid #ccc; padding: 15px; border-radius: 5px;">
            <p>O presente estudo tem como escopo...</p>
            <span class="editor-ai-suggestion">O escopo do presente estudo é...</span>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Revisar trecho", key="btn_revisar"):
        st.markdown("""
            <div class="rationale-tooltip">
                <strong>Critério utilizado: Clareza e Concisão (ABNT)</strong><br>
                O texto original possui ambiguidade referencial.
            </div>
        """, unsafe_allow_html=True)


elif menu == "Visão do Orientador":
    st.title("Fila de Validação - Orientador 👨‍🏫")
    st.info("Nenhuma decisão ou geração da IA é repassada ao orientando sem aprovação prévia.")
    st.write("Aprovações pendentes geradas pela IA:")
    
    st.markdown("<div class='validation-item' style='border: 1px solid #ccc; padding: 15px; margin-bottom: 10px;'>", unsafe_allow_html=True)
    cols = st.columns([4, 1])
    with cols[0]:
        st.markdown("**Prontuário de Reunião #12**")
    with cols[1]:
        if "published" not in st.session_state:
            st.session_state.published = False
        
        if not st.session_state.published:
            st.markdown("<span class='status-badge'>Pendente</span>", unsafe_allow_html=True)
        else:
            st.markdown("<span class='status-badge-published'>Publicado</span>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)
    with col_btn1:
        st.button("Editar ✏️", help="Editar", key="btn_editar")
    with col_btn2:
        st.button("Rejeitar ❌", help="Rejeitar", key="btn_rejeitar")
    with col_btn3:
        if st.button("Visualizar Diff", key="btn_diff"):
            st.session_state.show_diff = True
    with col_btn4:
        if st.button("Validar e Publicar", key="btn_publicar"):
            st.session_state.published = True
            st.rerun()

    if st.session_state.get("show_diff", False):
        st.markdown("""
            <div style="margin-top: 15px; border: 1px solid #ddd; padding: 10px;">
                <div class="diff-removed">- O aluno fará a pesquisa em 10 dias.</div>
                <div class="diff-added">+ O aluno entregará o capítulo em 15 dias.</div>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<div class='validation-item' style='border: 1px solid #ccc; padding: 15px; margin-bottom: 10px;'><strong>Revisão Cap 1</strong></div>", unsafe_allow_html=True)
    st.markdown("<div class='validation-item' style='border: 1px solid #ccc; padding: 15px;'><strong>Avaliação Artigo Qualis</strong></div>", unsafe_allow_html=True)


elif menu == "Visão do Aluno":
    st.markdown("""
        <div class="watermark-overlay">
            <div class="watermark-text">Aguardando validação <br>do orientador</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.title("Seu Prontuário 🎓")
    st.warning("⚠️ **Atenção:** Este texto foi gerado automaticamente a partir da reunião e ainda aguarda a validação do seu professor.")
    
    st.markdown("""
    ### Resumo da Reunião - 10/10/2026
    
    **Tópicos Discutidos:**
    - Revisão da fundamentação teórica do Capítulo 2.
    - Ajuste no cronograma de submissão ao comitê de ética.
    
    **Próximos Passos (Sugeridos pela IA):**
    1. Ler os novos artigos sugeridos na pasta `Referências`.
    2. Enviar a versão final da introdução até sexta-feira.
    """)

