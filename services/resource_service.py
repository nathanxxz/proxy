"""Implementação do Recurso Compartilhado para o Módulo 7 (Referência Inteligente).

Representa um recurso de alto custo (memória compartilhada, handle de arquivo
ou descritor de dispositivo) que deve ser desalocado quando ninguém mais o utilizar.
"""

from datetime import datetime
from typing import Any

from proxy.interfaces.resource_interface import SharedResourceInterface


class SharedResourceService(SharedResourceInterface):
    """Serviço Real do Recurso Compartilhado (RealSubject)."""

    def __init__(self, resource_name: str = "Pool-Memoria-Compartilhada-X1") -> None:
        self.resource_name: str = resource_name
        self.allocated_at: datetime = datetime.now()
        self.is_allocated: bool = True
        self.read_operations: int = 0
        self.write_operations: int = 0
        self.buffer_data: list[str] = [
            "Bloco Inicial: Configurações de Conexão do Sistema",
            "Bloco 02: Tabela de Sessões Ativas",
        ]

    def read_data(self, client_id: str) -> dict[str, Any]:
        """Lê os blocos de dados do buffer compartilhado."""
        if not self.is_allocated:
            raise RuntimeError(f"Erro de acesso: o recurso '{self.resource_name}' já foi desalocado da memória.")

        self.read_operations += 1
        return {
            "recurso": self.resource_name,
            "solicitante": client_id,
            "blocos": list(self.buffer_data),
            "total_blocos": len(self.buffer_data),
            "status": "LIDO_COM_SUCESSO",
        }

    def write_data(self, client_id: str, payload: str) -> dict[str, Any]:
        """Grava um novo bloco no recurso compartilhado."""
        if not self.is_allocated:
            raise RuntimeError(f"Erro de acesso: o recurso '{self.resource_name}' já foi desalocado da memória.")

        self.write_operations += 1
        self.buffer_data.append(f"[{datetime.now().strftime('%H:%M:%S')}] {client_id}: {payload}")
        return {
            "recurso": self.resource_name,
            "solicitante": client_id,
            "status": "GRAVADO_COM_SUCESSO",
            "total_blocos_atual": len(self.buffer_data),
        }

    def deallocate(self) -> str:
        """Libera fisicamente o recurso e buffers de memória."""
        self.is_allocated = False
        return f"Recurso '{self.resource_name}' foi desalocado com sucesso da memória operacional."
