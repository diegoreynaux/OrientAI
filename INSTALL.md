# Guia de Instalação (Setup)

Este documento descreve o passo a passo para configurar o ambiente de desenvolvimento e executar o **OrientAI** na sua máquina local.

## 1. Pré-requisitos

Certifique-se de ter os seguintes programas instalados:
- **Python** (versão 3.10 ou superior recomendada. O projeto foi validado com a versão 3.13).
- **Git** (para clonar o repositório).

## 2. Passo a Passo

### Clonar o Repositório
Abra o seu terminal (ou PowerShell) e clone o projeto para o seu computador:
```bash
git clone URL_DO_SEU_REPOSITORIO_AQUI
cd OrientAI
```

### Criar o Ambiente Virtual (venv)
É fundamental isolar as dependências do projeto para evitar conflitos no sistema.
No Windows:
```bash
python -m venv venv
```
No Linux/macOS:
```bash
python3 -m venv venv
```

### Ativar o Ambiente Virtual
Sempre ative o ambiente virtual antes de rodar o projeto ou de instalar pacotes.
No Windows (PowerShell):
```bash
.\venv\Scripts\activate
```
No Linux/macOS:
```bash
source venv/bin/activate
```
*(Você saberá que deu certo quando a indicação `(venv)` aparecer no início da linha de comando).*

### Instalar as Dependências
Com o ambiente ativado, instale as bibliotecas necessárias (Streamlit, Pytest, Playwright, etc):
```bash
pip install -r requirements.txt
```

### Instalar os Navegadores do Playwright
Como o projeto possui uma robusta suíte de testes E2E para validação das diretrizes OrientAI, é necessário baixar os navegadores do Playwright (Chromium, etc):
```bash
playwright install
```

---

## 3. Executando o Projeto

O sistema conta com a **Aplicação Interativa** e a **Suíte de Validação E2E**.

**1. Para iniciar a interface da aplicação:**
```bash
streamlit run app.py
```
*(Isso abrirá automaticamente a interface do OrientAI no seu navegador padrão, na porta `8501`).*

**2. Para rodar a suíte de testes (com a aplicação rodando):**
Abra uma **nova janela do terminal**, ative o ambiente virtual nela e execute:
```bash
pytest
```
*(O Pytest, em conjunto com o Playwright, validará de forma automatizada todas as restrições e regras de segurança da matriz OrientAI).*

