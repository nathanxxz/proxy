"""Implementação do Proxy Virtual (Lazy Initialization) para o Módulo 2.

Fiel ao trabalho acadêmico:
Adia a criação de um serviço pesado até que ele seja estritamente necessário.
Instancia o serviço apenas na primeira utilização e reutiliza a mesma instância
nas chamadas seguintes, poupando memória e tempo de inicialização.
"""

import time
from datetime import datetime
from typing import Any

from proxy.interfaces.database_interface import DatabaseInterface
from proxy.services.database_service import HeavyDatabaseService


class VirtualDatabaseProxy(DatabaseInterface):
    """Proxy Virtual para Banco de Dados Pesado (Lazy Initialization)."""

    def __init__(self, connection_string: str = "postgresql://cluster-prod.catolicapb.edu.br:5432/academico") -> None:
        self.connection_string: str = connection_string
        # O serviço real começa NULO (não consome recursos nem executa conexão na criação do proxy)
        self._real_database: HeavyDatabaseService | None = None
        self.proxy_created_at: datetime = datetime.now()
        self.lifecycle_events: list[str] = [
            f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] Proxy Virtual criado levemente na memória. O banco de dados pesado AINDA NÃO foi instanciado."
        ]
        self.total_calls: int = 0

    @property
    def is_service_instantiated(self) -> bool:
        """Indica se o serviço pesado já foi instanciado."""
        return self._real_database is not None

    def _get_or_create_real_service(self) -> HeavyDatabaseService:
        """Método interno que aplica a Inicialização Preguiçosa (Lazy Initialization)."""
        if self._real_database is None:
            log_criacao = f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] PRIMEIRA CHAMADA DETECTADA: Instanciando HeavyDatabaseService sob demanda (Lazy Loading)..."
            self.lifecycle_events.append(log_criacao)

            start = time.perf_counter()
            self._real_database = HeavyDatabaseService(self.connection_string)
            elapsed_ms = round((time.perf_counter() - start) * 1000, 2)

            log_conclusao = f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] Conexão pesada estabelecida e armazenada no Proxy ({elapsed_ms} ms)."
            self.lifecycle_events.append(log_conclusao)
        else:
            log_reuso = f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] CHAMADA SUBSEQUENTE: Reutilizando a instância ativa do banco de dados (0 ms de overhead de conexão)."
            self.lifecycle_events.append(log_reuso)

        return self._real_database

    def query(self, sql: str) -> list[dict[str, Any]]:
        """Executa a consulta garantindo que o serviço exista apenas no momento da execução."""
        self.total_calls += 1
        service = self._get_or_create_real_service()
        return service.query(sql)

    def get_status(self) -> dict[str, Any]:
        """Inspeciona o estado do proxy e do serviço real (se existente)."""
        if self._real_database is None:
            return {
                "proxy_created_at": self.proxy_created_at.strftime("%H:%M:%S"),
                "is_instantiated": False,
                "message": "Serviço real não instanciado. Zero consumo de conexão.",
                "total_proxy_calls": self.total_calls,
                "events_count": len(self.lifecycle_events),
            }

        status_real = self._real_database.get_status()
        status_real["proxy_created_at"] = self.proxy_created_at.strftime("%H:%M:%S")
        status_real["is_instantiated"] = True
        status_real["total_proxy_calls"] = self.total_calls
        return status_real
