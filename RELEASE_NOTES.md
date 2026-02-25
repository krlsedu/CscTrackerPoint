Aqui estão as Notas de Release para a versão **v26.09.005**, consolidando as melhorias de arquitetura, correções lógicas e atualizações de infraestrutura.

---

# 📝 Release Notes - v26.09.005

## Resumo
Esta versão foca na maturidade da aplicação, trazendo uma refatoração significativa para utilização de bibliotecas core compartilhadas, otimização de performance em cálculos matemáticos com vetorização e a implementação de fluxos de CI/CD automatizados.

---

## 🚀 Features

- **Processamento de Ponto:** Implementação de lógica avançada para processamento de tempo trabalhado e cálculo de dias úteis.
- **Otimização de Performance:** Utilização de vetorização (Pandas) para o cálculo de feriados e horas esperadas, reduzindo a latência de processamento.
- **Gestão de Feriados:** Incorporação de horas de feriado no somatório de tempo esperado.
- **Observabilidade:** Implementação de logging estruturado utilizando `logging.getLogger` e integração com **Prometheus Metrics** para monitoramento.
- **API & Segurança:** 
    - Adição de suporte a **CORS**.
    - Nova rota `GET /register` para consulta de registros.
    - Implementação de flag `edited` para rastreabilidade de alterações manuais em pontos.
- **DevOps:** 
    - Implementação de workflow no **GitHub Actions** para criação automática de releases.
    - Utilitário de notificações para falhas críticas.

---

## 🐛 Fixes

- **Cálculos Matemáticos:** Correção no multiplicador de tempo para garantir consistência no cálculo de horas esperadas.
- **Manipulação de Dados:** Ajuste no tratamento de `reset_index` em DataFrames para evitar perda de índices operacionais.
- **Casos de Borda:** Correção na lógica de processamento para sequências de ponto único (entradas sem saída correspondente).
- **Tipagem:** Ajuste na inicialização de contadores no `PointService` para garantir consistência de tipos (inteiros).

---

## 🔧 Chore

- **Refatoração de Código:** Remoção de classes redundantes (`HttpRepository`, `Interceptor`, `Utils`) em favor da biblioteca centralizada `csctracker-py-core`.
- **Gestão de Dependências:** 
    - Atualização do Python e dependências no `requirements.txt` (Pandas, csctracker-py-core).
    - Sincronização frequente com versões estáveis do core tracker.
- **Infraestrutura Docker:** Melhoria no setup do container com inclusão de `.dockerignore` e otimização do `Dockerfile`.
- **CI/CD:** Atualização de scripts do Jenkins e automação de builds disparados por commits.

---

### 💡 Notas do Tech Lead
> "Esta release marca a transição do projeto para um modelo de dependência de pacotes core, o que reduz o débito técnico local e facilita a manutenção. A migração para cálculos vetorizados com Pandas é um ganho essencial de escalabilidade para o serviço de PointService."

**Assinado:**
*Tech Lead Responsável* 
v26.09.005 | 2026