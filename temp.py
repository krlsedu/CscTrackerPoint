import requests
import time
from datetime import datetime, timedelta

dados = [
  { "dia": "2026-02-25", "primeiro_horario": "10:31", "inicio_pausa": "15:49", "fim_pausa": "15:34", "ultimo_horario": "17:20" },
  { "dia": "2026-02-24", "primeiro_horario": "10:50", "inicio_pausa": "15:19", "fim_pausa": "15:57", "ultimo_horario": "19:40" },
  { "dia": "2026-02-23", "primeiro_horario": "10:38", "inicio_pausa": "15:10", "fim_pausa": "15:58", "ultimo_horario": "20:00" },
  { "dia": "2026-02-20", "primeiro_horario": "10:50", "inicio_pausa": "15:50", "fim_pausa": "15:44", "ultimo_horario": "19:44" },
  { "dia": "2026-02-19", "primeiro_horario": "10:48", "inicio_pausa": "15:14", "fim_pausa": "16:32", "ultimo_horario": "23:46" },
  { "dia": "2026-02-18", "primeiro_horario": "10:38", "inicio_pausa": "15:22", "fim_pausa": "16:29", "ultimo_horario": "20:01" },
  { "dia": "2026-02-13", "primeiro_horario": "10:21", "inicio_pausa": "15:50", "fim_pausa": "15:46", "ultimo_horario": "19:39" },
  { "dia": "2026-02-12", "primeiro_horario": "10:50", "inicio_pausa": "15:10", "fim_pausa": "16:07", "ultimo_horario": "20:05" },
  { "dia": "2026-02-11", "primeiro_horario": "10:49", "inicio_pausa": "15:26", "fim_pausa": "16:28", "ultimo_horario": "20:09" },
  { "dia": "2026-02-10", "primeiro_horario": "10:50", "inicio_pausa": "15:34", "fim_pausa": "15:30", "ultimo_horario": "23:19" },
  { "dia": "2026-02-09", "primeiro_horario": "10:33", "inicio_pausa": "15:05", "fim_pausa": "16:07", "ultimo_horario": "19:34" },
  { "dia": "2026-02-06", "primeiro_horario": "10:48", "inicio_pausa": "15:42", "fim_pausa": "15:30", "ultimo_horario": "20:11" },
  { "dia": "2026-02-05", "primeiro_horario": "10:20", "inicio_pausa": "15:05", "fim_pausa": "16:04", "ultimo_horario": "23:09" },
  { "dia": "2026-02-04", "primeiro_horario": "10:42", "inicio_pausa": "14:58", "fim_pausa": "16:09", "ultimo_horario": "20:04" },
  { "dia": "2026-02-03", "primeiro_horario": "10:41", "inicio_pausa": "15:14", "fim_pausa": "16:14", "ultimo_horario": "20:02" },
  { "dia": "2026-02-02", "primeiro_horario": "10:29", "inicio_pausa": "15:11", "fim_pausa": "16:15", "ultimo_horario": "19:18" }
]

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'authorization': 'Bearer 82bf3701-fc1e-4904-aaf7-4a57b36edee7',
    'content-type': 'application/json',
    'origin': 'https://csctracker.com',
    'priority': 'u=1, i',
    'referer': 'https://csctracker.com/',
    'sec-ch-ua': '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
    'x-correlation-id': 'CscTrackerFontend-Chrome-Windows-e39ca719-aba5-4857-a52b-8bebceca8c4d'
}

url = 'https://bff.csctracker.com/point/register'

# Ordena a lista de dicionários pela data
dados_ordenados = sorted(dados, key=lambda x: x['dia'])

for registro in dados_ordenados:
    dia = registro['dia']

    # Monta as strings e já ordena pra não perder a sequência lógica do dia
    horarios_do_dia = [
        f"{dia} {registro['primeiro_horario']}:00",
        f"{dia} {registro['inicio_pausa']}:00",
        f"{dia} {registro['fim_pausa']}:00",
        f"{dia} {registro['ultimo_horario']}:00"
    ]
    horarios_do_dia.sort()

    tipos_marcacao = ["E", "S", "E", "S"]

    print(f"\n--- Mandando os registros do dia {dia} ---")

    for horario_str, tipo in zip(horarios_do_dia, tipos_marcacao):
        # Converte a string pra um objeto datetime
        horario_dt = datetime.strptime(horario_str, "%Y-%m-%d %H:%M:%S")

        # Tira as 3 horas
        horario_ajustado = horario_dt - timedelta(hours=3)

        # Converte de volta pra string pro payload
        horario_final_str = horario_ajustado.strftime("%Y-%m-%d %H:%M:%S")

        payload = {
            "date_time": horario_final_str,
            "seq_mark": 0,
            "type": tipo
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            print(f"Horário original: {horario_str} | Ajustado: {horario_final_str} | Tipo: {tipo} | Status: {response.status_code}")
        except Exception as e:
            print(f"Deu ruim ao mandar o horário {horario_final_str}. Erro: {e}")

        time.sleep(1)

print("\nFeito! Tudo enviado com -3h.")