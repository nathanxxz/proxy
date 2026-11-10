"""Implementação do Proxy de Proteção para o Módulo 3.

Fiel ao trabalho acadêmico:
Intercepta requisições a um serviço administrativo e valida os papéis/permissões
do usuário solicitante. Somente repassa a chamada ao serviço real se houver autorização,
bloqueando acessos indevidos e registrando tentativas não autorizadas.
"""

from datetime import datetime
from enum import Enum
from typing import Any

from proxy.interfaces.admin_interface import AdminServiceInterface
from proxy.services.admin_service import RealAdminService


class UserRole(str, Enum):
    """Papéis de usuário reconhecidos pelo sistema."""

    ADMIN = "ADMIN"
    OPERADOR = "OPERADOR"
    CONVIDADO = "CONVIDADO"


class ProtectionAdminProxy(AdminServiceInterface):
    """Proxy de Proteção com controle de acesso baseado em papéis (RBAC)."""

    def __init__(self, real_service: RealAdminService | None = None) -> None:
        self._real_service: RealAdminService = real_service or RealAdminService()
        self.security_logs: list[dict[str, Any]] = []

    def _log_security_decision(self, operacao: str, usuario: str, papel: UserRole, autorizada: bool, motivo: str) -> None:
        """Registra a auditoria da decisão de segurança tomada pelo Proxy."""
        self.security_logs.append({
            "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "operacao": operacao,
            "usuario": usuario,
            "papel": papel.value,
            "autorizada": autorizada,
            "motivo": motivo,
        })

    def alterar_configuracao(self, chave: str, valor: str, usuario: str, papel: UserRole = UserRole.CONVIDADO) -> dict[str, Any]:
        """Protege a alteração de configurações (permitida apenas para ADMIN e OPERADOR)."""
        if papel not in (UserRole.ADMIN, UserRole.OPERADOR):
            motivo = f"Acesso bloqueado: o papel '{papel.value}' não tem permissão para alterar parâmetros do sistema."
            self._log_security_decision("ALTERAR_CONFIGURACAO", usuario, papel, False, motivo)
            raise PermissionError(motivo)

        self._log_security_decision("ALTERAR_CONFIGURACAO", usuario, papel, True, "Operação autorizada pelo Proxy.")
        return self._real_service.alterar_configuracao(chave, valor, usuario)

    def excluir_usuario(self, id_usuario_alvo: int, usuario_solicitante: str, papel: UserRole = UserRole.CONVIDADO) -> dict[str, Any]:
        """Protege a exclusão de contas (estritamente restrita a administradores)."""
        if papel != UserRole.ADMIN:
            motivo = f"Acesso bloqueado: apenas usuários com perfil '{UserRole.ADMIN.value}' podem excluir contas."
            self._log_security_decision("EXCLUIR_USUARIO", usuario_solicitante, papel, False, motivo)
            raise PermissionError(motivo)

        self._log_security_decision("EXCLUIR_USUARIO", usuario_solicitante, papel, True, "Operação autorizada com privilégio máximo.")
        return self._real_service.excluir_usuario(id_usuario_alvo, usuario_solicitante)

    def reiniciar_servidor(self, motivo: str, usuario_solicitante: str, papel: UserRole = UserRole.CONVIDADO) -> dict[str, Any]:
        """Protege o reinício da infraestrutura (estritamente restrito a ADMIN)."""
        if papel != UserRole.ADMIN:
            motivo = f"Acesso bloqueado: tentativa não autorizada de reiniciar o servidor pelo usuário '{usuario_solicitante}'."
            self._log_security_decision("REINICIAR_SERVIDOR", usuario_solicitante, papel, False, motivo)
            raise PermissionError(motivo)

        self._log_security_decision("REINICIAR_SERVIDOR", usuario_solicitante, papel, True, "Comando de reboot aprovado e delegado ao serviço real.")
        return self._real_service.reiniciar_servidor(motivo, usuario_solicitante)
