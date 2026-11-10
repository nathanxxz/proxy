"""Interface para o Módulo 4 — Proxy Remoto.

Define o contrato para acesso a um serviço que reside em outro servidor,
escondendo do cliente os detalhes de serialização, rede e latência.
"""

from abc import ABC, abstractmethod
from typing import Any


class RemoteServiceInterface(ABC):
    """Contrato abstrato para serviço de computação e dados remotos."""

    @abstractmethod
    def obter_relatorio_servidor(self, servidor_id: str) -> dict[str, Any]:
        """Obtém métricas e telemetria de um servidor de nuvem remoto.

        Args:
            servidor_id: Identificador do nó remoto.

        Returns:
            dict[str, Any]: Dados de telemetria desempacotados.
        """
        pass

    @abstractmethod
    def executar_calculo_distribuido(self, dataset: list[float], operacao: str) -> dict[str, Any]:
        """Envia um lote de dados para processamento remoto pesado.

        Args:
            dataset: Lista de valores numéricos para análise.
            operacao: Tipo de agregação ('soma', 'media', 'variancia').

        Returns:
            dict[str, Any]: Resultado consolidado do cálculo remoto.
        """
        pass
