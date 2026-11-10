"""Implementação do Servidor Remoto para o Módulo 4 (Proxy Remoto).

Simula um servidor de nuvem fisicamente separado que recebe requisições
via mensagens serializadas, processa e devolve a resposta empacotada.
"""

import json
import statistics
import time
from datetime import UTC, datetime
from typing import Any


class RealRemoteServer:
    """Servidor Remoto Real (hospedado virtualmente em outra máquina).

    Não expõe diretamente a interface em Python para o cliente local;
    espera mensagens JSON encapsuladas em envelopes de rede.
    """

    def __init__(self, ip_address: str = "192.168.10.42", hostname: str = "cloud-node-pb-01.local") -> None:
        self.ip_address: str = ip_address
        self.hostname: str = hostname
        self.uptime_hours: int = 1420
        self.total_packets_received: int = 0

    def dispatch_raw_network_packet(self, raw_json_payload: str) -> str:
        """Ponto de entrada do protocolo de transporte remoto (RPC / Socket).

        Simula a recepção de um pacote binário/JSON através de um socket TCP,
        desempacotamento, roteamento interno e resposta.
        """
        self.total_packets_received += 1
        # Simula latência de transmissão na rede (200ms de RTT)
        time.sleep(0.2)

        packet: dict[str, Any] = json.loads(raw_json_payload)
        action = packet.get("action")
        params = packet.get("params", {})

        if action == "GET_SERVER_REPORT":
            servidor_id = params.get("servidor_id", "DESCONHECIDO")
            response = {
                "status": 200,
                "server_id": servidor_id,
                "hostname": self.hostname,
                "ip": self.ip_address,
                "uptime": f"{self.uptime_hours} horas",
                "cpu_usage_pct": 28.4,
                "memory_used_mb": 4096,
                "memory_total_mb": 16384,
                "timestamp_utc": datetime.now(UTC).isoformat(),
            }
        elif action == "EXECUTE_DISTRIBUTED_CALC":
            dataset: list[float] = params.get("dataset", [])
            operacao: str = params.get("operacao", "soma")

            if not dataset:
                response = {"status": 400, "erro": "Dataset vazio."}
            elif operacao == "soma":
                response = {"status": 200, "resultado": sum(dataset), "itens": len(dataset)}
            elif operacao == "media":
                response = {"status": 200, "resultado": statistics.mean(dataset), "itens": len(dataset)}
            elif operacao == "variancia":
                res = statistics.variance(dataset) if len(dataset) > 1 else 0.0
                response = {"status": 200, "resultado": res, "itens": len(dataset)}
            else:
                response = {"status": 400, "erro": f"Operação '{operacao}' não suportada."}
        else:
            response = {"status": 404, "erro": f"Ação remota '{action}' desconhecida."}

        # Devolve pacote serializado de volta pela rede
        return json.dumps(response)
