"""Implementação da Referência Inteligente (Smart Reference Proxy) para o Módulo 7.

Fiel ao trabalho acadêmico (Seção 5):
Acompanha quais clientes ainda utilizam um objeto compartilhado caro, registrando
quem acessou o recurso e desalocando-o automaticamente da memória quando o contador
de referências ativas chega a zero.

NOTA DIDÁTICA:
Em linguagens como C++, este conceito se assemelha a um std::shared_ptr.
Em ambientes empresariais Python, é utilizado para gerenciar pools de conexões,
sessões ativas de banco de dados ou arquivos abertos compartilhados entre threads/corrotinas.
"""

from datetime import datetime
from typing import Any

from proxy.interfaces.resource_interface import SharedResourceInterface
from proxy.services.resource_service import SharedResourceService


class SmartReferenceProxy(SharedResourceInterface):
    """Proxy de Referência Inteligente (Smart Reference).

    Gerencia o ciclo de vida e a contagem de clientes ativos em um recurso compartilhado.
    """

    def __init__(self, resource_service: SharedResourceService | None = None) -> None:
        self._resource: SharedResourceService = resource_service or SharedResourceService()
        self.active_clients: set[str] = set()
        self.usage_log: list[str] = [
            f"[{datetime.now().strftime('%H:%M:%S')}] SmartReferenceProxy inicializado. Recurso monitorado: {self._resource.resource_name}."
        ]
        self.auto_released: bool = False

    @property
    def reference_count(self) -> int:
        """Retorna o número atual de clientes referenciando ativamente o objeto."""
        return len(self.active_clients)

    def acquire_reference(self, client_id: str) -> int:
        """Registra a entrada de um cliente que passa a utilizar o recurso compartilhado."""
        self.active_clients.add(client_id)
        msg = f"[{datetime.now().strftime('%H:%M:%S')}] Cliente '{client_id}' adquiriu referência. (Total de referências ativas: {self.reference_count})."
        self.usage_log.append(msg)
        return self.reference_count

    def release_reference(self, client_id: str) -> int:
        """Libera a referência do cliente.

        Se o contador zerar, o Proxy desaloca automaticamente o recurso subjacente.
        """
        if client_id in self.active_clients:
            self.active_clients.remove(client_id)
            msg = f"[{datetime.now().strftime('%H:%M:%S')}] Cliente '{client_id}' liberou referência. (Restam: {self.reference_count})."
            self.usage_log.append(msg)
        else:
            msg = f"[{datetime.now().strftime('%H:%M:%S')}] Aviso: Cliente '{client_id}' tentou liberar mas não possuía referência ativa."
            self.usage_log.append(msg)

        # Regra de Ouro da Referência Inteligente: Desalocação automática quando contagem == 0
        if self.reference_count == 0 and not self.auto_released:
            dealloc_msg = self._resource.deallocate()
            self.auto_released = True
            log_cleanup = f"[{datetime.now().strftime('%H:%M:%S')}] [AUTO-CLEANUP] Referências zeradas! {dealloc_msg}"
            self.usage_log.append(log_cleanup)

        return self.reference_count

    def read_data(self, client_id: str) -> dict[str, Any]:
        """Delega a leitura registrando a telemetria do cliente."""
        # Se o cliente ler sem ter registrado explicitamente, o proxy vincula-o
        if client_id not in self.active_clients:
            self.acquire_reference(client_id)

        self.usage_log.append(f"[{datetime.now().strftime('%H:%M:%S')}] Leitura executada pelo cliente '{client_id}'.")
        return self._resource.read_data(client_id)

    def write_data(self, client_id: str, payload: str) -> dict[str, Any]:
        """Delega a escrita registrando a telemetria do cliente."""
        if client_id not in self.active_clients:
            self.acquire_reference(client_id)

        self.usage_log.append(f"[{datetime.now().strftime('%H:%M:%S')}] Escrita executada pelo cliente '{client_id}': {payload[:30]}...")
        return self._resource.write_data(client_id, payload)

    def get_lifecycle_status(self) -> dict[str, Any]:
        """Retorna o estado consolidado do recurso e das referências ativas."""
        return {
            "resource_name": self._resource.resource_name,
            "is_allocated": self._resource.is_allocated,
            "auto_released": self.auto_released,
            "reference_count": self.reference_count,
            "active_clients": list(self.active_clients),
            "total_logs": len(self.usage_log),
        }
