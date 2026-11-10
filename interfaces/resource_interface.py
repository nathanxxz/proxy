"""Interface para o Módulo 7 — Referência Inteligente (Smart Reference Proxy).

Define o contrato para gerenciar o ciclo de vida e a utilização de um
recurso compartilhado com alto consumo de memória ou conexão.
"""

from abc import ABC, abstractmethod
from typing import Any


class SharedResourceInterface(ABC):
    """Contrato abstrato para acesso a um recurso compartilhado no sistema."""

    @abstractmethod
    def read_data(self, client_id: str) -> dict[str, Any]:
        """Lê blocos de dados do recurso compartilhado.

        Args:
            client_id: Identificador do cliente solicitante.

        Returns:
            dict[str, Any]: Conteúdo lido e telemetria de acesso.
        """
        pass

    @abstractmethod
    def write_data(self, client_id: str, payload: str) -> dict[str, Any]:
        """Grava dados no recurso compartilhado.

        Args:
            client_id: Identificador do cliente solicitante.
            payload: Mensagem ou dados a serem gravados.

        Returns:
            dict[str, Any]: Confirmação de gravação e bytes persistidos.
        """
        pass
