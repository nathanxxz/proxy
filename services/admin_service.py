"""Implementação do Serviço Real Administrativo para o Módulo 3 (Proxy de Proteção).

Representa operações protegidas de alto privilégio no sistema.
"""

from datetime import datetime
from typing import Any

from proxy.interfaces.admin_interface import AdminServiceInterface


class RealAdminService(AdminServiceInterface):
    """Serviço Real Administrativo (RealSubject).

    Executa comandos que alteram criticamente o estado do sistema.
    """

    def __init__(self) -> None:
        self.configuracoes: dict[str, str] = {
            "MODO_MANUTENCAO": "DESATIVADO",
            "LIMITE_SESSAO_MINUTOS": "30",
            "NIVEL_LOG": "INFO",
        }
        self.usuarios_ativos: dict[int, str] = {
            101: "joao.pedro@fafic.edu.br",
            102: "pedro.henrique@fafic.edu.br",
            103: "fabricio.nathan@fafic.edu.br",
            104: "aluno.temporario@fafic.edu.br",
        }
        self.historico_operacoes: list[dict[str, Any]] = []

    def alterar_configuracao(self, chave: str, valor: str, usuario: str) -> dict[str, Any]:
        """Aplica a alteração de parâmetro diretamente no sistema."""
        antigo = self.configuracoes.get(chave, "INEXISTENTE")
        self.configuracoes[chave] = valor
        registro = {
            "operacao": "ALTERAR_CONFIGURACAO",
            "chave": chave,
            "valor_anterior": antigo,
            "novo_valor": valor,
            "executado_por": usuario,
            "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "status": "SUCESSO",
        }
        self.historico_operacoes.append(registro)
        return registro

    def excluir_usuario(self, id_usuario_alvo: int, usuario_solicitante: str) -> dict[str, Any]:
        """Remove o registro de usuário."""
        if id_usuario_alvo not in self.usuarios_ativos:
            raise ValueError(f"Usuário com ID {id_usuario_alvo} não encontrado.")

        email_removido = self.usuarios_ativos.pop(id_usuario_alvo)
        registro = {
            "operacao": "EXCLUIR_USUARIO",
            "id_usuario": id_usuario_alvo,
            "email_removido": email_removido,
            "executado_por": usuario_solicitante,
            "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "status": "SUCESSO",
        }
        self.historico_operacoes.append(registro)
        return registro

    def reiniciar_servidor(self, motivo: str, usuario_solicitante: str) -> dict[str, Any]:
        """Dispara a rotina de reinicialização do nó."""
        registro = {
            "operacao": "REINICIAR_SERVIDOR",
            "motivo": motivo,
            "executado_por": usuario_solicitante,
            "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "status": "REINICIALIZACAO_AGENDADA",
        }
        self.historico_operacoes.append(registro)
        return registro
