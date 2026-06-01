"""Interface CLI estilo Claude Code — usa Rich + prompt-toolkit."""
import pyfiglet
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
from datetime import datetime

console = Console()
session = PromptSession(style=Style.from_dict({"prompt": "#06B6D4 bold"}))


def show_banner():
    banner = pyfiglet.figlet_format("Mission Control", font="ansi_shadow")
    console.print(Text(banner, style="bold #06B6D4"))
    console.print(Panel.fit(
        "Trilha: EnviroSat — Observacao Ambiental\n"
        "Sistema de monitoramento e analise por IA generativa.\n"
        "Use /help para ver os comandos · /exit para sair.\n"
        "Modelo: gpt-oss:120b via Ollama Cloud",
        title="MISSION CONTROL AI",
        border_style="#06B6D4"
    ))


def show_response(text: str):
    now = datetime.now().strftime("%H:%M")
    console.print(Panel(text, title="Mission Control", subtitle=now, border_style="#06B6D4"))


def run_cli(engine):
    show_banner()

    if not engine.is_ready():
        console.print("Engine status: AGUARDANDO IMPLEMENTACAO\n", style="yellow")

    while True:
        try:
            user_input = session.prompt(">> ").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\nEncerrando Mission Control AI...")
            break

        if not user_input:
            continue

        if user_input == "/exit":
            console.print("Encerrando Mission Control AI...")
            break

        if user_input == "/help":
            console.print(Panel(
                "/help    → mostra este painel\n"
                "/status  → snapshot da telemetria atual\n"
                "/about   → informacoes sobre a missao\n"
                "/clear   → limpa o terminal\n"
                "/exit    → encerra o sistema\n\n"
                "Qualquer outro texto e enviado a IA para analise.",
                title="Comandos",
                border_style="#8484A0"
            ))
            continue

        if user_input == "/status":
            show_response(engine.status_snapshot())
            continue

        if user_input == "/about":
            console.print(Panel(
                "Mission Control AI — Trilha EnviroSat\n\n"
                "Satelite simulado: EnviroSat-1\n"
                "Tipo: Observacao ambiental (sensor termico + optico)\n"
                "Referencia: Amazonia-1 / Landsat\n\n"
                "Parametros monitorados:\n"
                "  sensor_termico, sensor_optico_ndvi,\n"
                "  buffer_imagens_pct, precisao_geo_metros, energia_disponivel_pct\n\n"
                "FIAP · Ciencia da Computacao · Global Solution 2026.1",
                title="Sobre a missao",
                border_style="#8484A0"
            ))
            continue

        if user_input == "/clear":
            console.clear()
            show_banner()
            continue

        with console.status("Analisando telemetria...", spinner="dots"):
            resposta = engine.analyze(user_input)
        show_response(resposta)
