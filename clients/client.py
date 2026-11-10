"""Implementação do Cliente para o Módulo 1 — Estrutura Básica.

Participante: Cliente (Client).
O cliente depende estritamente da interface Subject.
Ele pode receber tanto o RealSubject quanto o Proxy, sem qualquer alteração
em seu código de consumo.
"""

from proxy.interfaces.subject import Subject


class ClientApp:
    """Aplicação cliente que consome serviços através da interface Subject."""

    def __init__(self, service: Subject) -> None:
        """Recebe qualquer objeto que satisfaça o contrato Subject.

        Args:
            service: Instância de RealSubject ou BasicProxy.
        """
        self._service: Subject = service

    def run_business_operation(self) -> str:
        """Dispara a operação de negócio dependendo apenas da abstração."""
        return self._service.request()
