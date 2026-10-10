# OrientAI - Projeto OrientAI (Human-Computer AI Interaction)

Este repositório contém a documentação, a análise de riscos e a prova de conceito (suíte de testes automatizados e políticas de governança) da plataforma **OrientAI**.

O OrientAI é uma plataforma educacional baseada em LLMs (Modelos de Linguagem de Grande Escala) voltada para o acompanhamento de pós-graduação (mestrados e doutorados). Ele atua como um "copiloto acadêmico" que suporta, mas **não substitui**, o julgamento, a autoria e a autonomia cognitiva de professores orientadores e alunos, seguindo rigorosamente os princípios de **Human-Centered AI (OrientAI)** e as normas do **NIST AI RMF 1.0**.

---

## 🏗 Arquitetura Proposta e Valor Estratégico

A arquitetura do OrientAI foi desenhada sob três pilares fundamentais, refletidos diretamente na estrutura de pastas deste repositório:

1. **Arquitetura de Segurança e Privacidade (Privacy-First)**: Emprega um Gateway de LLM capaz de rotear dados abertos para a nuvem (ex: OpenAI) e dados sigilosos para infraestruturas locais (Ollama), mitigando riscos de *Vendor Lock-in* e vazamento de propriedade intelectual (LGPD).
2. **Arquitetura OrientAI (Human-in-the-loop)**: Nenhuma decisão acadêmica sugerida pela IA entra em vigor ou se torna visível ao aluno sem a **validação expressa do orientador**. O uso de marcas d'água, *badges* de proveniência (quem gerou o texto) e justificativas de sugestões garante transparência.
3. **Arquitetura Anti-Alucinação (Groundedness)**: O LLM é impedido de gerar textos base (não atua como *ghostwriter*) ou referências bibliográficas do zero. Ele usa RAG (Retrieval-Augmented Generation) para responder unicamente com base na literatura fornecida.

---

## ⚙️ Escolha da Stack Tecnológica (Python + Playwright)

Para a implementação da prova de conceito e validação técnica das mitigações de risco, optou-se pela utilização de **Python**, utilizando o **Pytest** integrado ao **Playwright**:

*   **Python e Pytest**: Escolhido por ser a linguagem *de facto* no ecossistema de Inteligência Artificial e dados, facilitando futuras integrações reais com as APIs de LLMs (OpenAI, LangChain, LlamaIndex). O Pytest traz extrema flexibilidade para escrever desde testes unitários da máquina de estados do orientador até testes de auditoria de segurança (*Privacy Routing*).
*   **Playwright (Python)**: Selecionado como o framework para Testes End-to-End (E2E) por sua arquitetura moderna, rápida e confiável frente aos desafios de interfaces ricas. Como os princípios do **OrientAI** baseiam-se em intervenções visuais claras (alertas obrigatórios, bloqueios de *onboarding*, marcas d'água em documentos pendentes e diff de edições), o Playwright possibilita simular e validar precisamente as interações do usuário no navegador de forma automatizada, assegurando a eficácia técnica dos controles humanos na interface.

---

## 📁 Estrutura do Repositório e Explicação dos Arquivos

### Documentos Fundacionais (Raiz)
*   **`1. OrientAI - Projeto OrientAI.docx`**: O Documento de Visão central. Detalha as necessidades dos *stakeholders*, requisitos dos módulos (Co-Revisão, Kanban, Snapshot de Reuniões) e os riscos selecionados.
*   **`2. Matriz de Risco.xlsx`**: A matriz matriz quantitativa e qualitativa, pautada no NIST AI RMF, onde os riscos de IA (Alucinação, Viés, Privacidade, Supervisão) são categorizados com suas devidas medidas preventivas e detectivas.

### `/tests/` - A Prova de Conceito (Validação OrientAI)
A suíte de testes em Python (usando Pytest e Playwright) serve como evidência técnica (Mock) de que as mitigações exigidas na matriz de risco são aplicáveis no código do projeto.

*   **`/integration/`**:
    *   `test_llm_gateway.py` e `test_llm_failover.py`: Provam que a arquitetura não está presa a um fornecedor. Se a API externa falhar, o sistema roteia para provedores secundários ou locais.
    *   `test_validation_state_machine.py`: Garante que as transições sistêmicas de aprovação do professor (Aprovar, Rejeitar, Reprocessar) não podem ser burladas sistemicamente.
*   **`/e2e/` (Testes Comportamentais de Interface)**:
    *   `test_approval_gate_spec.py`, `test_pending_visibility_spec.py`, `test_advisor_validation_spec.py`: Testam a interface do usuário para garantir que orientandos só vejam documentos do LLM após o orientador clicar no "Portão de Aprovação".
    *   `test_ai_provenance_spec.py` e `test_suggestion_rationale_spec.py`: Garantem que o sistema exibe sempre **qual** IA gerou a sugestão e **por que** ela sugeriu a mudança (Transparência).
    *   `test_rag_grounding_spec.py`: Verifica a exibição obrigatória de avisos de que "a IA pode cometer erros", prevenindo dependência excessiva.
    *   `test_onboarding_block_spec.py`: Garante que o letramento digital em IA (onboarding) seja feito obrigatoriamente no primeiro login.
*   **`/security/`**:
    *   `test_no_fabricated_citations.py`: Valida as travas contra *Prompt Injection* visando criar fontes falsas.
    *   `test_privacy_routing.py`: Evidência de triagem de dados sensíveis para o motor local.
*   **`/audit/`**:
    *   `test_llm_audit_log.py`: Garante o registro padronizado e auditável para eventuais prestação de contas (*Accountability*).

### `app.py` - Frontend Interativo (Streamlit) e Avaliação OrientAI
Para viabilizar a execução dos testes automatizados de comportamento visual (E2E), desenvolveu-se uma interface iterativa utilizando **Streamlit**. A construção deste frontend multipáginas, construído totalmente em Python, permite demonstrar de maneira exata como as diretrizes OrientAI da Matriz de Risco se aplicam visualmente e proporciona uma experiência mais dinâmica:
*   **Dashboard**: Simula o painel principal com o bloqueio de *onboarding* inibidor (impossível navegar sem aceitar o treinamento ético).
*   **Chat com RAG**: Simula a interação com o LLM (RAG), garantindo o *badge* explícito de quem gerou (ex: OpenAI GPT-4) e os alertas inibidores sobre alucinações ("pode conter imprecisões").
*   **Editor / Co-Revisão**: Simula a edição de textos evidenciando o uso de *tooltips* explicativos da IA (Ex: Critério de Clareza ABNT), validando a justificativa transparente da sugestão.
*   **Visão do Orientador**: Demonstra a fila de validação onde o orientador tem controle irrestrito. Simula ferramentas para aprovar, visualizar diff das mudanças geradas pela IA e barrar conteúdos falsos.
*   **Visão do Aluno**: O lado do orientando, exibindo uma tarja/marca d'água transversal imponente indicando "Aguardando validação do orientador" antes de aprovação.

### `/docs/` - Governança Institucional e Letramento
O arcabouço normativo que permite ao OrientAI ser adotado por uma Universidade.

*   **`/governanca/`**:
    *   `consentimento-llm.md`: Termo de consentimento explícito exigido pela LGPD.
    *   `contingencia-llm.md`: Processos para manter a universidade operando em caso de queda global dos provedores de IA.
    *   `guia-boas-praticas.md`: Regras de uso institucional delimitando até onde a IA pode ajudar na produção acadêmica.
    *   `vendor-review-checklist.md`: Procedimento para avaliar futuros fornecedores de LLM contra uso de dados acadêmicos para treino de IA.
*   **`/treinamento/`**:
    *   `uso-responsavel-ia.md`: Material de treinamento OrientAI focado nos alunos (mitigação humana).

### `/artifacts/` - Relatórios Gerados
Simulações de saídas processadas pelo sistema para fins de auditoria acadêmica.
*   **`/audit/E02-validation-log.json`**: Trilha técnica provando quando um orientador validou uma decisão que a IA tomou.
*   **`/evaluation/T02-groundedness-report.json`**: Relatório de métricas sistêmicas monitorando o quão precisas estão sendo as respostas do RAG, identificando necessidade de calibração do modelo.

### `INSTALL.md` e `requirements.txt`
Arquivos contendo as diretrizes detalhadas de instalação e todas as dependências exatas (Streamlit, Pytest, Playwright) necessárias para rodar o projeto e a suíte de validação localmente.

---

## 🛠 Como executar a validação técnica (Testes)
O repositório requer Python instalado (foi validado com 3.13). Para um tutorial completo desde a clonagem do repositório, consulte o arquivo **`INSTALL.md`**.

```bash
# 1. Ativar o ambiente virtual (PowerShell no Windows)
.\venv\Scripts\activate

# 2. Iniciar a interface do Streamlit em segundo plano (ou em um terminal separado)
streamlit run app.py

# 3. Rodar a suíte de provas de conceito (incluindo testes de segurança e E2E)
pytest
```

