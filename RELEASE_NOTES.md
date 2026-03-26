Aqui está o Release Notes técnico para a versão **v26.13.001**, focado em correções críticas na lógica de cálculo de horas.

---

# 📝 Release Notes - v26.13.001

## Resumo
Esta versão foca na correção de bugs críticos no motor de cálculo de horas (`PointService`), especificamente no tratamento de feriados e ajustes de unidades de tempo, garantindo que o banco de horas e as expectativas de jornada reflitam os valores reais configurados.

---

## 🐛 Fixes

### Cálculo de Jornada e Feriados (`PointService`)
*   **Ajuste de Horas Customizadas:** Corrigida a lógica de cálculo do `holiday_time` para considerar corretamente os ajustes de horas customizados. Anteriormente, o sistema poderia ignorar exceções de jornada em dias de feriado.
*   **Correção de Unidade de Tempo:** Corrigido o multiplicador de unidade de tempo nos campos `expected_time` (tempo esperado) e `holiday_time` (tempo de feriado). Esta falha causava discrepâncias de escala nos cálculos de horas totais.

## 🔧 Chore
*   **Versionamento:** Atualização dos arquivos de controle `version.txt` e sincronização do histórico no `RELEASE_NOTES.md`.
*   **Build:** Trigger de build para a linhagem da versão 26.

---

### 🛠 Detalhes Técnicos (Diff Stats)
- **Arquivos alterados:** 3
- **Impacto principal:** `service/PointService.py` (Lógica de negócio de ponto eletrônico).
- **Commits analisados:** `d77a7c1`, `69c8f82`, `1eb65eb`.

---
**Tech Lead:** Carlos Eduardo Duarte Schwalm