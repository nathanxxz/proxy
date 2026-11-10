"""Implementação do Proxy Remoto para o Módulo 4.

Fiel ao trabalho acadêmico:
Representa localmente um objeto hospedado em outro servidor.
Esconde do cliente todos os detalhes de empacotamento (marshalling),
serialização de rede, transporte via sockets e desempacotamento (unmarshalling).
O cliente interage com o Proxy como se o serviço estivesse executando na mesma máquina.
"""

import json
import time
from typing import Any

from proxy.interfaces.remote_interface import RemoteServiceInterface
from proxy.services.remote_service import RealRemoteServer


class RemoteServiceProxy(RemoteServiceInterface):
    """Proxy Remoto (Stub local do cliente).

    Implementa RemoteServiceInterface e simula a camada de comunicação RPC/Remota.
    """

    def __init__(self, remote_server: RealRemoteServer | None = None) -> None:
        # Mantém a referência ou conexão lógica com o servidor remoto
        self._server: RealRemoteServer = remote_server or RealRemoteServer()
        self.network_transmission_logs: list[dict[str, Any]] = []

    def _transmit_rpc_call(self, action: str, params: dict[str, Any]) -> dict[str, Any]:
        """Cuida do protocolo de rede: serialização (marshalling), envio e retorno."""
        start = time.perf_counter()

        # 1. Empacotamento / Marshalling local
        envelope = {
            "protocol": "ACADEMIC_RPC_V1",
            "action": action,
            "params": params,
        }
        raw_json_payload = json.dumps(envelope)

        # 2. Transmissão transparente pelo canal de rede
        raw_response_payload = self._server.dispatch_raw_network_packet(raw_json_payload)

        # 3. Desempacotamento / Unmarshalling
        response_data: dict[str, Any] = json.loads(raw_response_payload)
        elapsed_ms = round((time.perf_counter() - start) * 1000, 2)

        # Registra a telemetria do tráfego para fins didáticos
        self.network_transmission_logs.append({
            "action": action,
            "payload_sent_bytes": len(raw_json_payload.encode()),
            "response_bytes": len(raw_response_payload.encode()),
            "rtt_latency_ms": elapsed_ms,
            "remote_host": self._server.hostname,
            "remote_ip": self._server.ip_address,
        })

        if response_data.get("status") not in (200, 201):
            raise ConnectionError(f"Erro remoto ({response_data.get('status')}): {response_data.get('erro')}")

        return response_data

    def obter_relatorio_servidor(self, servidor_id: str) -> dict[str, Any]:
        """Invoca a consulta remota transparente."""
        return self._transmit_rpc_call("GET_SERVER_REPORT", {"servidor_id": servidor_id})

    def executar_calculo_distribuido(self, dataset: list[float], operacao: str) -> dict[str, Any]:
        """Dispara o processamento distribuído na nuvem transparente."""
        return self._transmit_rpc_call("EXECUTE_DISTRIBUTED_CALC", {"dataset": dataset, "operacao": operacao})
