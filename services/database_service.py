"""Implementação do Serviço Real de Banco de Dados para o Módulo 2 (Proxy Virtual).

Representa um objeto pesado que consome muitos recursos e leva tempo para
estabelecer conexão, carregar pools e compilar esquemas relacionais.
"""

import time
from datetime import datetime
from typing import Any

from proxy.interfaces.database_interface import DatabaseInterface


class HeavyDatabaseService(DatabaseInterface):
    """Serviço de Banco de Dados Pesado (RealSubject).

    Simula uma conexão cara e pesada que aloca pools de memória e sockets de rede.
    """

    def __init__(self, connection_string: str = "postgresql://cluster-prod.catolicapb.edu.br:5432/academico") -> None:
        self.connection_string: str = connection_string
        self.created_at: datetime = datetime.now()
        self.initialization_duration_ms: float = 0.0
        self.query_count: int = 0
        self.is_connected: bool = False
        self._simulate_heavy_connection()

    def _simulate_heavy_connection(self) -> None:
        """Simula o custo computacional e de I/O de uma inicialização pesada."""
        start_time = time.perf_counter()
        # Simula latência de handshake TLS, alocação de buffer e carga de esquemas (800ms)
        time.sleep(0.8)
        self.is_connected = True
        self.initialization_duration_ms = round((time.perf_counter() - start_time) * 1000, 2)

    def query(self, sql: str) -> list[dict[str, Any]]:
        """Executa a consulta sobre a conexão pesada ativa."""
        if not self.is_connected:
            raise RuntimeError("Falha de conexão: o banco de dados não está conectado.")

        self.query_count += 1
        # Registros simulados correspondentes à consulta
        return [
            {"id": 1, "matricula": "2024.2060063", "aluno": "Samuel Dantas de Albuquerque", "curso": "Sistemas de Informação", "status": "Ativo"},
            {"id": 2, "matricula": "2024.1050012", "aluno": "Maria Clara Vasconcelos", "curso": "Engenharia de Software", "status": "Ativo"},
            {"id": 3, "matricula": "2023.2040089", "aluno": "Lucas Gonçalves Dias", "curso": "Ciência da Computação", "status": "Ativo"},
        ]

    def get_status(self) -> dict[str, Any]:
        """Retorna telemetria da conexão pesada."""
        return {
            "is_connected": self.is_connected,
            "connection_string": self.connection_string,
            "created_at": self.created_at.strftime("%H:%M:%S.%f")[:-3],
            "initialization_duration_ms": self.initialization_duration_ms,
            "total_queries_executed": self.query_count,
        }
