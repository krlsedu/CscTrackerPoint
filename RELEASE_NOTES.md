Aqui estão as Notas de Lançamento para a versão **v26.09.007**, elaboradas com foco em clareza técnica e rastreabilidade.

---

# 📝 Release Notes - v26.09.007

## Resumo
Esta versão foca na correção de uma falha crítica de precisão no cálculo de horas dentro do módulo de serviços de ponto, garantindo que a conversão de unidades de tempo esteja correta para o processamento de jornadas e feriados.

---

## 🐛 Fixes

*   **Cálculo de Jornada (PointService):** Corrigido o multiplicador de unidade de tempo utilizado nos cálculos de `expected_time` (tempo esperado) e `holiday_time` (tempo de feriado). 
    *   *Impacto:* Resolve discrepâncias onde os valores de tempo estavam sendo calculados com ordens de magnitude incorretas.
    *   *Arquivo afetado:* `service/PointService.py`
    *   *Commit:* `1eb65eb`

---

## 🚀 Features
*   *Nesta versão não foram implementadas novas funcionalidades.*

---

## 🔧 Chore
*   *Nesta versão não foram realizadas tarefas de manutenção ou infraestrutura.*

---

**Tech Lead:** Carlos Eduardo Duarte Schwalm (krlsedu)
**Data da Release:** 2026