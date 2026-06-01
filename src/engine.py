"""Motor de analise da Mission Control AI — Trilha EnviroSat."""
import os
from ollama import Client
from dotenv import load_dotenv
from pathlib import Path
from src import telemetria, alertas

load_dotenv()

TRILHA = "envirosat"

client = Client(
    host="https://ollama.com",
    headers={"Authorization": "Bearer " + os.environ.get("OLLAMA_API_KEY", "")}
)


def llm(prompt: str, system: str = None, max_tokens: int = 800, temperature: float = 0.3) -> str:
    """Envia prompt ao gpt-oss:120b via Ollama Cloud."""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    try:
        return client.chat(
            model="gpt-oss:120b",
            messages=messages,
            options={"num_predict": max_tokens, "temperature": temperature},
            stream=False
        )["message"]["content"].strip()
    except Exception as e:
        return f"Erro ao consultar IA: {e}"


def load_system_prompt() -> str:
    """Le o system prompt do arquivo prompts/system_prompt.md."""
    path = Path("prompts/system_prompt.md")
    if path.exists():
        return path.read_text(encoding="utf-8")
    return "Voce e um assistente de missao espacial."


class MissionEngine:
    """Motor de analise da missao EnviroSat."""

    def __init__(self):
        self.trilha = TRILHA
        self.system_prompt = load_system_prompt()

    def is_ready(self) -> bool:
        return True

    def status_snapshot(self) -> str:
        """Retorna snapshot textual do estado atual da telemetria com alertas."""
        dados = telemetria.coletar()
        lista_alertas = alertas.avaliar(dados)
        resumo = alertas.resumo_alertas(lista_alertas)

        linhas = [
            f"EnviroSat-1 · {self.trilha.upper()} · {dados['timestamp']}",
            "",
            "Telemetria atual:",
            f"  sensor_termico      : {dados['sensor_termico']}C",
            f"  sensor_optico_ndvi  : {dados['sensor_optico_ndvi']}",
            f"  buffer_imagens_pct  : {dados['buffer_imagens_pct']}%",
            f"  precisao_geo        : {dados['precisao_geo_metros']}m de desvio",
            f"  energia_disponivel  : {dados['energia_disponivel_pct']}%",
            "",
            "Alertas:",
            resumo,
        ]
        return "\n".join(linhas)

    def analyze(self, pergunta_usuario: str) -> str:
        """
        Coleta telemetria, avalia alertas e consulta a IA com o contexto completo.
        """
        dados = telemetria.coletar()
        lista_alertas = alertas.avaliar(dados)
        resumo = alertas.resumo_alertas(lista_alertas)

        contexto = f"""
TELEMETRIA ATUAL DO ENVIROSAT-1 ({dados['timestamp']}):
- sensor_termico: {dados['sensor_termico']}C
- sensor_optico_ndvi: {dados['sensor_optico_ndvi']}
- buffer_imagens_pct: {dados['buffer_imagens_pct']}%
- precisao_geo_metros: {dados['precisao_geo_metros']}m de desvio
- energia_disponivel_pct: {dados['energia_disponivel_pct']}%

ALERTAS DETECTADOS PELO SISTEMA:
{resumo}

PERGUNTA DO OPERADOR:
{pergunta_usuario}
"""
        return llm(contexto, system=self.system_prompt)
