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
    """Lê o system prompt do arquivo prompts/system_prompt.md."""
    path = Path(__file__).resolve().parent.parent / "prompts" / "system_prompt.md"
    if path.exists():
        return path.read_text(encoding="utf-8")
    return "Você é um assistente de missão espacial."


class MissionEngine:
    """Motor de analise da missao EnviroSat."""

    def __init__(self):
        self.trilha = TRILHA
        self.system_prompt = load_system_prompt()
        # Estado da telemetria — gerado UMA vez e reaproveitado por
        # status_snapshot() e analyze(), garantindo que a IA analise
        # exatamente a mesma leitura que aparece no /status.
        self.dados = None
        self.lista_alertas = []
        self.resumo = ""
        self.nova_leitura()

    def is_ready(self) -> bool:
        return True

    def nova_leitura(self) -> dict:
        """Faz uma nova leitura da telemetria e recalcula os alertas."""
        self.dados = telemetria.coletar()
        self.lista_alertas = alertas.avaliar(self.dados)
        self.resumo = alertas.resumo_alertas(self.lista_alertas)
        return self.dados

    def status_snapshot(self) -> str:
        """Faz uma nova leitura e retorna o snapshot textual com alertas."""
        self.nova_leitura()

        linhas = [
            f"EnviroSat-1 · {self.trilha.upper()} · {self.dados['timestamp']}",
            "",
            "Telemetria atual:",
            f"  sensor_termico      : {self.dados['sensor_termico']}C",
            f"  sensor_optico_ndvi  : {self.dados['sensor_optico_ndvi']}",
            f"  buffer_imagens_pct  : {self.dados['buffer_imagens_pct']}%",
            f"  precisao_geo        : {self.dados['precisao_geo_metros']}m de desvio",
            f"  energia_disponivel  : {self.dados['energia_disponivel_pct']}%",
            "",
            "Alertas:",
            self.resumo,
        ]
        return "\n".join(linhas)

    def analyze(self, pergunta_usuario: str) -> str:
        """
        Usa a leitura ATUAL da telemetria (NAO gera uma nova) e consulta a IA
        com o contexto completo — assim a analise sempre bate com o ultimo /status.
        """
        if self.dados is None:
            self.nova_leitura()

        contexto = f"""
TELEMETRIA ATUAL DO ENVIROSAT-1 ({self.dados['timestamp']}):
- sensor_termico: {self.dados['sensor_termico']}C
- sensor_optico_ndvi: {self.dados['sensor_optico_ndvi']}
- buffer_imagens_pct: {self.dados['buffer_imagens_pct']}%
- precisao_geo_metros: {self.dados['precisao_geo_metros']}m de desvio
- energia_disponivel_pct: {self.dados['energia_disponivel_pct']}%

ALERTAS DETECTADOS PELO SISTEMA:
{self.resumo}

PERGUNTA DO OPERADOR:
{pergunta_usuario}
"""
        return llm(contexto, system=self.system_prompt)
