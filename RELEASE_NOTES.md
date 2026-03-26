Aqui está o Release Notes técnico para a versão **v26.13.002**, consolidado com base nos commits analisados.

---

# 📝 Release Notes - v26.13.002

## Resumo
Esta versão foca na correção de cálculos críticos de jornada e tempo no serviço de pontos, garantindo que ajustes de horas customizadas e unidades de tempo sejam processados corretamente.

---

## 🐛 Fixes
*   **Cálculo de Horas em Feriados:** Ajustada a lógica de `holiday_time` para considerar corretamente os ajustes de horas customizadas (`custom hours adjustments`).
*   **Correção de Unidade de Tempo:** Corrigido o multiplicador de unidade de tempo incorreto que afetava os cálculos de `expected_time` e `holiday_time` no serviço de pontos.
*   **Integridade de Dados:** Sincronização das fórmulas de cálculo no `PointService.py` para evitar discrepâncias em relatórios de horas.

## 🔧 Chore
*   **Build Automation:** Atualização de metadados de versão (`version.txt`) e logs de histórico.
*   **Documentação:** Atualização do arquivo `RELEASE_NOTES.md` refletindo as mudanças das builds intermediárias.

---

### 🛠 Detalhes Técnicos (Diff Insights)
As alterações concentraram-se no arquivo `service/PointService.py`, onde foram identificados erros de precisão aritmética na conversão de unidades de tempo, impactando diretamente a folha de ponto dos colaboradores em dias de exceção (feriados e horários customizados).

**Commits incluídos:**
- `d77a7c1`: Fix holiday_time calculation.
- `1eb65eb`: Fix incorrect time unit multiplier.
- `fa517a9` & `69c8f82`: Build triggers e versionamento.