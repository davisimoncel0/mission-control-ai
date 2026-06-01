"""Thresholds e regras de decisao — Trilha EnviroSat."""

THRESHOLD_SENSOR_TERMICO_CRITICO = 70.0
THRESHOLD_SENSOR_TERMICO_ATENCAO = 50.0
THRESHOLD_BUFFER_CRITICO = 90.0
THRESHOLD_ENERGIA_CRITICA = 20.0
THRESHOLD_ENERGIA_ATENCAO = 35.0
THRESHOLD_GEO_CRITICO = 100.0
THRESHOLD_NDVI_BAIXO = 0.2


def avaliar(dados: dict) -> list:
    """
    Avalia os dados de telemetria e retorna lista de alertas.
    Cada alerta tem: nivel, parametro, valor, mensagem, acao.
    """
    alertas = []

    temp = dados["sensor_termico"]
    if temp >= THRESHOLD_SENSOR_TERMICO_CRITICO:
        alertas.append({
            "nivel": "CRITICO",
            "parametro": "sensor_termico",
            "valor": f"{temp}C",
            "mensagem": "Temperatura critica — possivel foco de incendio na area imageada.",
            "acao": "Priorizar downlink das imagens termicas e notificar brigada de incendio.",
        })
    elif temp >= THRESHOLD_SENSOR_TERMICO_ATENCAO:
        alertas.append({
            "nivel": "ATENCAO",
            "parametro": "sensor_termico",
            "valor": f"{temp}C",
            "mensagem": "Temperatura elevada — area quente em monitoramento.",
            "acao": "Agendar nova passagem na proxima janela orbital.",
        })

    buffer = dados["buffer_imagens_pct"]
    if buffer >= THRESHOLD_BUFFER_CRITICO:
        alertas.append({
            "nivel": "CRITICO",
            "parametro": "buffer_imagens_pct",
            "valor": f"{buffer}%",
            "mensagem": "Buffer quase cheio — risco de perda de dados nao transmitidos.",
            "acao": "Iniciar downlink de emergencia na proxima janela de contato.",
        })

    energia = dados["energia_disponivel_pct"]
    if energia <= THRESHOLD_ENERGIA_CRITICA:
        alertas.append({
            "nivel": "CRITICO",
            "parametro": "energia_disponivel_pct",
            "valor": f"{energia}%",
            "mensagem": "Energia critica — modo de economia ativado.",
            "acao": "MODO ECONOMIA: desligar sensor optico, manter apenas sensor termico e telemetria basica.",
        })
    elif energia <= THRESHOLD_ENERGIA_ATENCAO:
        alertas.append({
            "nivel": "ATENCAO",
            "parametro": "energia_disponivel_pct",
            "valor": f"{energia}%",
            "mensagem": "Energia em nivel de atencao.",
            "acao": "Reduzir frequencia de aquisicao e aguardar recarga solar.",
        })

    geo = dados["precisao_geo_metros"]
    if geo >= THRESHOLD_GEO_CRITICO:
        alertas.append({
            "nivel": "CRITICO",
            "parametro": "precisao_geo_metros",
            "valor": f"{geo}m de desvio",
            "mensagem": "Geolocalizacao imprecisa — imagens podem estar georeferenciadas incorretamente.",
            "acao": "Suspender alertas de desmatamento ate recalibracao do sistema de atitude.",
        })

    ndvi = dados["sensor_optico_ndvi"]
    if ndvi <= THRESHOLD_NDVI_BAIXO:
        alertas.append({
            "nivel": "ATENCAO",
            "parametro": "sensor_optico_ndvi",
            "valor": f"{ndvi}",
            "mensagem": "NDVI muito baixo — vegetacao em estado critico ou area desmatada detectada.",
            "acao": "Registrar coordenadas e acionar analise de conformidade ambiental.",
        })

    return alertas


def resumo_alertas(alertas: list) -> str:
    """Retorna string resumida dos alertas para exibicao no terminal."""
    if not alertas:
        return "Todos os parametros dentro do normal."

    linhas = []
    for a in alertas:
        prefixo = "CRITICO" if a["nivel"] == "CRITICO" else "ATENCAO"
        linhas.append(f"[{prefixo}] {a['parametro']}: {a['valor']} — {a['mensagem']}")

    return "\n".join(linhas)
