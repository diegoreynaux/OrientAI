# Plano de Contingência para Substituição de Provedor LLM

## 1. Objetivo
Estabelecer as diretrizes e procedimentos para manter a continuidade do serviço da plataforma OrientAI em caso de falha sistêmica, descontinuação ou degradação inaceitável do provedor de LLM primário.

## 2. Cenários de Ativação
- Indisponibilidade da API do provedor primário superior a 2 horas.
- Mudança abrupta e prejudicial nos Termos de Uso (ex: uso forçado de dados para treinamento).
- Alteração significativa de custos inviabilizando a operação.

## 3. Procedimento de Failover
1. O Gateway de IA detectará a falha.
2. A transição para o provedor secundário será acionada via variável de ambiente `LLM_FALLBACK_ACTIVE=true`.
3. Todos os roteamentos subsequentes utilizarão o novo endpoint sem alteração no código fonte.

## 4. Retorno à Operação Normal
Somente ocorrerá após avaliação do comitê técnico e confirmação de estabilidade de 24h.
