"""Script auxiliar para gerar e testar banners ASCII."""
import argparse
import pyfiglet
from rich.console import Console
from rich.align import Align
from rich.text import Text

console = Console()


def show_banner():
    linha1 = pyfiglet.figlet_format("Global Solution", font="ansi_shadow")
    linha2 = pyfiglet.figlet_format("Mission Control AI", font="ansi_shadow")
    console.print(Align.center(Text(linha1, style="bold #A855F7")))
    console.print(Align.center(Text(linha2, style="bold #06B6D4")))
    console.print(Align.center(
        Text("-- 2026.1 · Prompt Engineering and AI · FIAP --", style="italic #8484A0")
    ))


def list_fonts():
    for f in sorted(pyfiglet.FigletFont.getFonts()):
        console.print(f)


def demo_fonts():
    fontes = ["ansi_shadow", "slant", "banner3", "big", "block", "doom", "epic", "larry3d"]
    for fonte in fontes:
        try:
            texto = pyfiglet.figlet_format("Mission Control", font=fonte)
            console.rule(fonte)
            console.print(Text(texto, style="bold #06B6D4"))
        except Exception:
            pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gerador de banner ASCII")
    parser.add_argument("-fonts", action="store_true", help="Lista todas as fontes")
    parser.add_argument("-font", type=str, help="Testa uma fonte especifica")
    parser.add_argument("-text", type=str, default="Mission Control AI", help="Texto do banner")
    parser.add_argument("-demo", action="store_true", help="Demonstra 8 fontes")
    args = parser.parse_args()

    if args.fonts:
        list_fonts()
    elif args.demo:
        demo_fonts()
    elif args.font:
        console.print(Text(pyfiglet.figlet_format(args.text, font=args.font), style="bold #06B6D4"))
    else:
        show_banner()
