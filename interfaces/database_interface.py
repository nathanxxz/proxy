"""Interface para o Módulo 2 — Proxy Virtual (Lazy Initialization).

Define o contrato de um serviço de banco de dados pesado.
"""

from abc import ABC, abstractmethod
from typing import Any


class DatabaseInterface(ABC):
    """Contrato abstrato para serviços de acesso a dados."""

    @abstractmethod
    def query(self, sql: str) -> list[dict[str, Any]]:
        """Executa uma consulta no banco de dados.

        Args:
            sql: Comando SQL ou identificador da consulta.

        Returns:
            list[dict[str, Any]]: Registros resultantes da consulta.
        """
        pass

    @abstractmethod
    def get_status(self) -> dict[str, Any]:
        """Retorna o estado operacional da conexão e métricas de inicialização.

        Returns:
            dict[str, Any]: Informações de status, tempo de conexão e estado.
        """
        pass
