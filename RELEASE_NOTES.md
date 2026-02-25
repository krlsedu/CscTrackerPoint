Aqui estão as Notas de Lançamento para a versão **v26.09.006**, focadas em estabilidade e correção de bugs no processamento de dados.

---

# 📝 Release Notes - v26.09.006

## 🐛 Fixes

*   **PointService:** Corrigida falha no cálculo de dias úteis (`working_days`) que ocorria ao processar um DataFrame vazio. 
    *   *Impacto:* Evita exceções de execução (Runtime Errors) quando o sistema tenta calcular métricas para períodos sem registros de ponto.
    *   *Arquivo afetado:* `service/PointService.py`

---

### 🚀 Features
*   *Nenhuma nova funcionalidade nesta versão.*

### 🔧 Chore
*   *Nenhuma alteração de infraestrutura ou manutenção nesta versão.*

---
**Tech Lead:** Carlos Eduardo Duarte Schwalm  
**Commit de referência:** `4e62a8d`