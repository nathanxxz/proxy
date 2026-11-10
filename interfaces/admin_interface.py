"""Interface para o Módulo 3 — Proxy de Proteção.

Define o contrato para operações administrativas sensíveis que exigem
controle rigoroso de autenticação e autorização.
"""

from abc import ABC, abstractmethod
from typing import Any


class AdminServiceInterface(ABC):
    """Contrato abstrato para operações administrativas do sistema."""

    @abstractmethod
    def alterar_configuracao(self, chave: str, valor: str, usuario: str) -> dict[str, Any]:
        """Altera um parâmetro crítico do sistema.

        Args:
            chave: Nome do parâmetro a ser modificado.
            valor: Novo valor do parâmetro.
            usuario: Identificador do usuário que solicita a alteração.

        Returns:
            dict[str, Any]: Confirmação com status e dados alterados.
        """
        pass

    @abstractmethod
    def excluir_usuario(self, id_usuario_alvo: int, usuario_solicitante: str) -> dict[str, Any]:
        """Exclui permanentemente um usuário da base de dados.

        Args:
            id_usuario_alvo: ID do usuário a ser removido.
            usuario_solicitante: Identificador do usuário que solicita a exclusão.

        Returns:
            dict[str, Any]: Confirmação com status e registro afetado.
        """
        pass

    @abstractmethod
    def reiniciar_servidor(self, motivo: str, usuario_solicitante: str) -> dict[str, Any]:
        """Dispara reinicialização segura do servidor institucional.

        Args:
            motivo: Justificativa para a reinicialização.
            usuario_solicitante: Identificador do usuário solicitante.

        Returns:
            dict[str, Any]: Status do comando executado.
        """
        pass
