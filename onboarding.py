from __future__ import annotations

from datetime import datetime
from html import escape
import streamlit as st

VERSAO = "1.2"
DADOS = {
    "Aluno": {
        "emoji": "🎓", "email": "bruno.aluno@universidade.edu.br", "tempo": "8–12 minutos",
        "resumo": "Conheça as ferramentas de apoio ao estudo e preserve a autoria acadêmica.",
        "modulos": [
            ("Conhecendo o OrientAI", "Utilize o Chat com RAG, o Editor / Co-Revisão e a Visão do Aluno. A IA oferece apoio, não substitui a aprendizagem.", "Explore a interface e compreenda os limites das funcionalidades."),
            ("Integridade e autoria", "Produza seu próprio trabalho e declare o auxílio da IA quando as normas institucionais exigirem.", "Revise e adapte qualquer sugestão antes de incorporá-la ao texto."),
            ("Fontes e uso crítico", "Uma IA pode errar e inventar referências. Confira informações e citações nas fontes originais.", "Ao não encontrar evidência suficiente, não trate a resposta como fato."),
            ("Privacidade e responsabilidade", "Não compartilhe documentos sigilosos nem dados pessoais sem autorização. O estudante é responsável pelo texto final.", "Em caso de dúvida, consulte o orientador e as normas da instituição."),
        ],
        "questoes": [
            ("Ao usar uma referência sugerida por IA, você deve:", ["Verificar se existe e consultar a fonte original", "Usá-la sem conferência", "Considerá-la válida se parecer formal", "Evitar citar a fonte"], 0),
            ("Sobre autoria acadêmica, é correto:", ["Manter responsabilidade pelo texto e declarar IA quando exigido", "Apresentar todo texto gerado por IA como próprio", "Dispensar qualquer revisão", "Copiar o conteúdo integralmente"], 0),
            ("Se uma resposta da IA parecer incerta, você deve:", ["Verificar evidências e consultar o orientador", "Aceitá-la", "Ignorar fontes primárias", "Publicá-la sem ressalvas"], 0),
            ("É apropriado inserir dados sigilosos em um serviço externo sem autorização?", ["Não", "Sim, se ajudar na pesquisa", "Sim, se o prompt for curto", "Sim, em qualquer situação"], 0),
        ],
    },
    "Professor": {
        "emoji": "👩‍🏫", "email": "ana.prof@universidade.edu.br", "tempo": "10–15 minutos",
        "resumo": "Conheça as regras de supervisão, validação e publicação de conteúdo.",
        "modulos": [
            ("Conhecendo o OrientAI", "O OrientAI apoia atividades de orientação. O professor mantém o julgamento acadêmico e a responsabilidade pela decisão.", "Reconheça as áreas de edição, validação e acompanhamento."),
            ("Uso responsável da IA generativa", "A IA pode produzir informações imprecisas e recomendações inadequadas. Verifique evidências, referências e incertezas.", "Não trate textos gerados como pareceres definitivos."),
            ("Validação antes da publicação", "Prontuários e feedbacks gerados por IA precisam de aprovação humana prévia. Revise, edite, rejeite ou solicite reprocessamento.", "Compare as versões e registre a decisão docente."),
            ("Privacidade e transparência", "Observe a origem das sugestões, identifique conteúdos gerados por IA e evite compartilhar dados pessoais em serviços não autorizados.", "Preserve a confidencialidade e a autoria humana."),
        ],
        "questoes": [
            ("Qual boa prática deve orientar o uso da IA na orientação acadêmica?", ["Verificar as fontes das informações geradas pela IA", "Inserir dados pessoais dos alunos em qualquer prompt", "Compartilhar senhas de acesso", "Deixar a IA substituir a avaliação docente"], 0),
            ("Um feedback produzido com apoio de IA deve ser:", ["Validado pelo professor antes da publicação", "Publicado automaticamente", "Ocultado do orientador", "Enviado sem identificação"], 0),
            ("Uma recomendação com referência não verificável deve:", ["Ser corrigida ou rejeitada após verificação", "Ser tratada como comprovada", "Ser publicada com urgência", "Ter sua origem omitida"], 0),
            ("Quanto à responsabilidade pelas decisões de orientação:", ["O professor mantém a supervisão e a decisão final", "É inteiramente do modelo", "Não precisa de revisão", "É do estudante apenas"], 0),
        ],
    },
    "Revisor": {
        "emoji": "📝", "email": "carlos.revisor@universidade.edu.br", "tempo": "12–15 minutos",
        "resumo": "Aprenda a comparar versões e justificar decisões de revisão.",
        "modulos": [
            ("Papel do revisor", "Sugestões automáticas auxiliam a redação, mas não comprovam a qualidade científica.", "Diferencie sugestão automática de versão validada."),
            ("Critérios de revisão", "Analise clareza, coerência, preservação do sentido e justificativas apresentadas pela IA.", "Revise sempre a relação entre texto original e sugestão."),
            ("Comparação de versões", "Compare alterações antes de aceitar, editar ou rejeitar um trecho.", "Evite mudanças que alterem o argumento do autor sem justificativa."),
            ("Transparência e privacidade", "Identifique participação da IA e não envie dados sensíveis sem autorização.", "Registre decisões e observações para posterior conferência."),
        ],
        "questoes": [
            ("Ao receber uma sugestão da IA, o revisor deve:", ["Comparar versões e analisar a justificativa", "Aceitá-la sem leitura", "Excluir o texto do autor", "Omitir a alteração"], 0),
            ("A revisão deve prioritariamente:", ["Preservar autoria e coerência", "Alterar o sentido original", "Dispensar o autor", "Substituir todas as citações"], 0),
            ("Uma decisão de rejeição deve:", ["Ser registrada e justificada", "Ser ocultada", "Apagar histórico", "Impedir futuras revisões"], 0),
            ("Qual prática protege a privacidade?", ["Evitar exposição de dados sensíveis sem autorização", "Compartilhar conteúdo confidencial", "Publicar comentários sem revisão", "Usar qualquer provedor externo"], 0),
        ],
    },
}


def _init():
    for chave, valor in {
        "ob_identidade": None, "ob_tela": "acesso", "ob_licoes": {}, "ob_registros": {},
        "ob_logs": [], "ob_respostas": {}, "ob_questao": {}, "ob_resultados": {},
    }.items():
        if chave not in st.session_state:
            st.session_state[chave] = valor


def _evento(acao, detalhe=""):
    identidade = st.session_state.ob_identidade or {}
    st.session_state.ob_logs.append({
        "Data/hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "Usuário": identidade.get("email", "—"), "Perfil": identidade.get("perfil", "—"),
        "Ação": acao, "Detalhes": detalhe, "Versão": VERSAO,
    })


def _concluido(perfil, email):
    registro = st.session_state.ob_registros.get((email, perfil, VERSAO))
    return registro is not None


def onboarding_concluido(perfil: str | None = None) -> bool:
    """Consulta o estado de conclusão da identidade simulada nesta sessão."""
    _init()
    identidade = st.session_state.ob_identidade
    if not identidade:
        return False
    perfil_atual = perfil or identidade["perfil"]
    return _concluido(perfil_atual, identidade["email"])


def _navegar(tela):
    st.session_state.ob_tela = tela
    st.rerun()


def _css():
    st.markdown("""
    <style>
    .ob-hero{background:linear-gradient(100deg,#edf5ff,#f0efff);padding:23px;border:1px solid #dbe7fc;border-radius:16px;margin:8px 0 20px;color:#17365e}
    .ob-hero h2{margin:0 0 7px;color:#123c79;font-size:1.65rem}.ob-hero p{margin:0;color:#38577b}
    .ob-card{background:#fff;border:1px solid #dbe4f2;border-radius:14px;padding:20px 24px;margin:10px 0;color:#213b5b}
    .ob-card h3{color:#173b72;margin:0 0 12px}.ob-card p{color:#38516f}
    .ob-green{background:#ecfdf3;border:1px solid #b3e6c8;padding:18px;border-radius:13px;color:#166534}
    .ob-step{font-size:.86rem;font-weight:650;color:#416083}
    </style>""", unsafe_allow_html=True)


def _cabecalho(tela, perfil=None):
    if perfil:
        cfg = DADOS[perfil]
        st.markdown(f'<div class="ob-hero"><h2>{cfg["emoji"]} Onboarding — {escape(perfil)}</h2><p>{escape(cfg["resumo"])} · Versão {VERSAO}</p></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="ob-hero"><h2>🎓 Bem-vindo ao OrientAI</h2><p>Capacitação inicial obrigatória por perfil — demonstração</p></div>', unsafe_allow_html=True)
    etapas = ["Primeiro acesso", "Boas-vindas", "Tutorial", "Teste", "Conclusão"]
    atual = ["acesso", "boas_vindas", "tutorial", "teste", "conclusao"].index(tela)
    cols = st.columns(5)
    for idx, (col, nome) in enumerate(zip(cols, etapas)):
        with col:
            st.markdown(f'<span class="ob-step">{"✅" if idx < atual else ("🔵" if idx == atual else "⚪")} {idx+1}. {nome}</span>', unsafe_allow_html=True)
    st.progress(atual / 4)


def _acesso():
    _cabecalho("acesso")
    st.subheader("Primeiro acesso")
    st.info("Este login é apenas uma simulação.")
    col1, col2 = st.columns([2, 1])
    with col1:
        perfil = st.selectbox("Perfil de acesso", list(DADOS), key="ob_login_perfil")
        email = st.text_input("E-mail institucional (simulado)", value=DADOS[perfil]["email"], key=f"ob_login_email_{perfil}")
        if st.button("Entrar →", type="primary", use_container_width=True):
            email = email.strip().lower()
            if not email or "@" not in email:
                st.error("Informe um e-mail fictício válido para continuar.")
            else:
                st.session_state.ob_identidade = {"perfil": perfil, "email": email}
                _evento("Primeiro acesso", f"Perfil selecionado: {perfil}")
                _navegar("conclusao" if _concluido(perfil, email) else "boas_vindas")
    with col2:
        st.markdown(f'<div class="ob-card"><h3>👤 Perfil identificado</h3><p><strong>{escape(st.session_state.ob_login_perfil)}</strong></p><p>Onboarding obrigatório<br>Versão {VERSAO}</p></div>', unsafe_allow_html=True)


def _boas_vindas(perfil):
    _cabecalho("boas_vindas", perfil)
    st.markdown(f'<div class="ob-card"><h3>Bem-vindo(a), {escape(perfil)}!</h3><p>Antes de utilizar o OrientAI, é necessário concluir um tutorial de uso responsável da IA, políticas acadêmicas e funcionalidades do seu perfil.</p><p>⏱️ Tempo estimado: {DADOS[perfil]["tempo"]} · 📚 1 módulo integrado · ✅ 4 questões de compreensão</p></div>', unsafe_allow_html=True)
    st.write("**Você aprenderá a:**")
    for titulo, _, _ in DADOS[perfil]["modulos"]:
        st.write("✓", titulo)
    if st.button("Iniciar onboarding →", type="primary", use_container_width=True):
        _evento("Início do onboarding", f"Versão {VERSAO}")
        _navegar("tutorial")


def _tutorial(perfil):
    """Apresenta as quatro unidades de conteúdo em um único módulo por perfil."""
    _cabecalho("tutorial", perfil)
    identidade = st.session_state.ob_identidade
    chave = (identidade["email"], perfil, VERSAO)
    st.caption("MÓDULO ÚNICO — FORMAÇÃO INTEGRADA")
    st.progress(1.0)
    st.subheader(f"Treinamento completo — {perfil}")
    st.write("Leia todos os temas abaixo. Ao finalizar, confirme a leitura para acessar a avaliação.")
    for numero, (titulo, conteudo, exemplo) in enumerate(DADOS[perfil]["modulos"], 1):
        with st.container(border=True):
            st.markdown(f"#### {numero}. {titulo}")
            st.write(conteudo)
            st.info(f"Na prática: {exemplo}")
    confirmou = st.checkbox(
        "Declaro que li e compreendi todos os temas do treinamento.",
        key=f"ob_leitura_integrada_{chave}"
    )
    c1, c2 = st.columns(2)
    with c1:
        if st.button("← Voltar às boas-vindas", use_container_width=True):
            _navegar("boas_vindas")
    with c2:
        if st.button("Iniciar teste →", type="primary", disabled=not confirmou, use_container_width=True):
            # Uma única entrada no log para o módulo completo de cada perfil.
            _evento("Conclusão do módulo", f"Treinamento integrado: {perfil} (4 temas)")
            _evento("Conclusão do tutorial", "1 módulo integrado concluído")
            _navegar("teste")


def _teste(perfil):
    _cabecalho("teste", perfil)
    chave = (st.session_state.ob_identidade["email"], perfil, VERSAO)
    questoes = DADOS[perfil]["questoes"]
    indice = st.session_state.ob_questao.get(chave, 0)
    st.subheader("Teste de compreensão")
    st.caption(f"Questão {indice + 1} de {len(questoes)} — aprovação com 75% de acertos")
    st.progress((indice + 1)/len(questoes))
    enunciado, alternativas, _ = questoes[indice]
    st.write(f"**{enunciado}**")
    resposta = st.radio("Selecione a alternativa:", alternativas, index=None, key=f"ob_resposta_{chave}_{indice}")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("← Anterior", use_container_width=True):
            if indice == 0:
                _navegar("tutorial")
            st.session_state.ob_questao[chave] = indice - 1
            st.rerun()
    with c2:
        if st.button("Finalizar teste" if indice == len(questoes)-1 else "Próxima pergunta →", disabled=resposta is None, type="primary", use_container_width=True):
            st.session_state.ob_respostas.setdefault(chave, {})[indice] = alternativas.index(resposta)
            if indice < len(questoes)-1:
                st.session_state.ob_questao[chave] = indice + 1
                st.rerun()
            acertos = sum(st.session_state.ob_respostas[chave].get(i) == q[2] for i, q in enumerate(questoes))
            nota = int(100 * acertos / len(questoes))
            st.session_state.ob_resultados[chave] = nota
            aprovado = nota >= 75
            _evento("Resultado do teste", f"{acertos}/{len(questoes)} acertos ({nota}%) — {'aprovado' if aprovado else 'reprovado'}")
            if aprovado:
                st.session_state.ob_registros[chave] = {
                    "Usuário": chave[0], "Perfil": perfil, "Versão": VERSAO,
                    "Conclusão": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "Acerto": f"{nota}%", "Status": "Concluído",
                }
                _evento("Acesso liberado (simulado)", f"Perfil {perfil}, versão {VERSAO}")
                _navegar("conclusao")
            else:
                _navegar("reprovado")


def _reprovado(perfil):
    chave = (st.session_state.ob_identidade["email"], perfil, VERSAO)
    st.error(f"Resultado: {st.session_state.ob_resultados.get(chave, 0)}%. São necessários pelo menos 75% para aprovação.")
    st.write("Revise o módulo integrado e tente novamente. Nenhuma conclusão foi registrada.")
    if st.button("Revisar tutorial e refazer o teste", type="primary"):
        st.session_state.ob_questao[chave] = 0
        st.session_state.ob_respostas[chave] = {}
        st.session_state.pop(f"ob_leitura_integrada_{chave}", None)
        for i in range(len(DADOS[perfil]["questoes"])):
            st.session_state.pop(f"ob_resposta_{chave}_{i}", None)
        _evento("Nova tentativa do onboarding")
        _navegar("tutorial")


def _conclusao(perfil):
    _cabecalho("conclusao", perfil)
    identidade = st.session_state.ob_identidade
    registro = st.session_state.ob_registros.get((identidade["email"], perfil, VERSAO))
    if not registro:
        _navegar("boas_vindas")
    st.markdown(f'<div class="ob-green"><h3>✅ Onboarding concluído!</h3>Você concluiu o treinamento do perfil <strong>{escape(perfil)}</strong> (versão {VERSAO}).</div>', unsafe_allow_html=True)
    st.write("")
    c1,c2,c3 = st.columns(3)
    c1.metric("Módulos concluídos", "1/1")
    c2.metric("Acerto no teste", registro["Acerto"])
    c3.metric("Status", "Aprovado")
    st.caption(f"Registro simulado: {registro['Conclusão']}")
    st.success("Acesso liberado no protótipo.")
    st.balloons()
    if st.button("Acessar o sistema →", type="primary"):
        st.info("Volte ao menu lateral para navegar pelos módulos da aplicação.")


def _registros():
    st.divider()
    esquerda, direita = st.columns(2)
    with esquerda:
        with st.container(border=True):
            st.markdown("**🗃️ Registros de conclusão por versão (simulados)**")
            registros = list(st.session_state.ob_registros.values())
            if registros:
                st.dataframe(registros, hide_index=True, use_container_width=True)
            else:
                st.info("Nenhuma conclusão nesta sessão.")
    with direita:
        with st.container(border=True):
            st.markdown("**📋 Log de auditoria (simulado)**")
            if st.session_state.ob_logs:
                st.dataframe(list(reversed(st.session_state.ob_logs)), hide_index=True, use_container_width=True)
            else:
                st.info("Nenhum evento registrado.")
    with st.expander(f"📘 Guia de boas práticas de IA — versão {VERSAO}"):
        st.markdown("- Preserve a autoria e declare uso de IA quando exigido.\n- Verifique informações, citações e referências nas fontes originais.\n- Não compartilhe dados pessoais ou sigilosos sem autorização.\n- A decisão acadêmica requer supervisão humana.\n- Diferencie conteúdos humanos e sugestões de IA.")


def render_onboarding():
    """Renderiza todo o onboarding no Dashboard. Chamada pública para app.py."""
    _init()
    _css()
    st.title("Onboarding OrientAI")
    st.caption("Protótipo visual · dados simulados")
    tela = st.session_state.ob_tela
    if tela == "acesso":
        _acesso()
    else:
        identidade = st.session_state.ob_identidade
        if not identidade:
            _navegar("acesso")
        perfil = identidade["perfil"]
        if tela == "boas_vindas":
            _boas_vindas(perfil)
        elif tela == "tutorial":
            _tutorial(perfil)
        elif tela == "teste":
            _teste(perfil)
        elif tela == "reprovado":
            _reprovado(perfil)
        elif tela == "conclusao":
            _conclusao(perfil)
    st.divider()
    identidade = st.session_state.ob_identidade
    if identidade:
        a,b = st.columns([4,1])
        with a:
            st.caption(f"Usuário de demonstração: {identidade['email']} | Perfil: {identidade['perfil']}")
        with b:
            if st.button("Trocar perfil", use_container_width=True):
                _evento("Troca de perfil")
                st.session_state.ob_identidade = None
                _navegar("acesso")
    _registros()
