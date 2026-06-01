# Mission Control AI — EnviroSat

## Integrantes

| Nome | RM |
|------|----|
| Davi Simoncelo | RM: 571738 |
| João Pedro Sousa | RM: 573962 |
| Matheus Evangelista Silva | RM: 568593 |

## O que o projeto faz

Sistema de monitoramento do satélite EnviroSat-1 que simula telemetria de um satélite de observação ambiental, detecta anomalias via thresholds em Python e analisa o estado da missão em linguagem natural usando IA generativa (Ollama Cloud). Cada alerta traduz a anomalia técnica em impacto concreto para operadores, brigadas de incêndio e analistas ambientais.

## Persona atendida

Operador do Centro de Controle Ambiental (INPE / órgão estadual): precisa de diagnóstico rápido e ação clara diante de anomalias que podem indicar focos de incêndio ou desmatamento.

## Tecnologias utilizadas

- Python 3.10+
- Ollama Cloud API (modelo gpt-oss:120b)
- rich 13.9.4
- prompt-toolkit 3.0.52
- pyfiglet 1.0.4
- python-dotenv 1.2.1

## Como executar

```
git clone https://github.com/usuario/mission-control-ai
cd mission-control-ai
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# edite o arquivo .env e coloque sua chave Ollama
python main.py
```

## Comandos da CLI

- `/status`  — snapshot da telemetria atual com alertas
- `/help`    — lista os comandos disponíveis
- `/about`   — informações sobre a missão
- `/clear`   — limpa o terminal
- `/exit`    — encerra o sistema
- qualquer texto — enviado à IA para análise contextualizada

## Demonstração


![Banner inicial](assets/screenshot_banner.png)
![Análise com alerta crítico](assets/screenshot_analise.png)

## System Prompt

Disponível em `prompts/system_prompt.md`. Instrui o modelo a sempre conectar diagnóstico técnico com impacto terrestre, usando formato estruturado com classificação de severidade.

## Cenários de teste

1. Operação normal — todos os parâmetros dentro do range
2. Foco de incêndio crítico — temperatura acima de 70°C + NDVI baixo
3. Energia crítica — abaixo de 20%, modo economia ativado pelo código Python
4. Múltiplos alertas — buffer cheio + energia baixa + temperatura elevada simultâneos

## Proposta de valor / modelo de negócio

**Problema terrestre:** O Brasil perde milhões de hectares de floresta anualmente para desmatamento e incêndios. O gargalo não é a falta de satélites, é o tempo entre detecção do dado bruto e a resposta em campo. Operadores precisam interpretar telemetria técnica e transformar isso em ação rápida, sem depender de especialistas disponíveis 24h.

**Quem paga:** Modelo híbrido — setor público (INPE, IBAMA, Secretarias Estaduais de Meio Ambiente) financia a infraestrutura de monitoramento; setor privado (seguradoras rurais, empresas com metas ESG, operadoras de crédito de carbono) paga por relatórios de compliance e certificação de áreas monitoradas.

**Métrica de impacto:** EnviroSat-1 operando 100% saudável por 1 ano cobre cerca de 2 milhões de hectares de áreas protegidas na Amazônia Legal, reduz o tempo médio de resposta de brigadas de 6h para 4h, e gera 12 relatórios mensais de conformidade ambiental para órgãos reguladores.

**Modelo de negócio:** Dado-como-serviço (DaaS). Órgãos ambientais assinam acesso à plataforma de alertas em tempo real. Analistas de compliance adquirem relatórios georreferenciados por área. Brigadas recebem notificações via API integrada ao sistema de despacho.

## Limitações conhecidas

- Telemetria é simulada aleatoriamente, não reflete dados reais de satélite
- Sem persistência de histórico entre sessões
- Interface apenas via terminal

## Vídeo


