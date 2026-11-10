"""Implementação do RealSubject (Serviço Real) para o Módulo 1 — Estrutura Básica.

Participante: Serviço Real (RealSubject).
Contém a lógica de negócio principal. O cliente pode utilizá-lo diretamente
ou através do Proxy, sem notar diferença no contrato de interface.
"""

from proxy.interfaces.subject import Subject


class RealSubject(Subject):
    """Classe de negócio que implementa a operação real."""

    def __init__(self) -> None:
        self.execution_count: int = 0

    def request(self) -> str:
        """Executa a lógica de negócio real."""
        self.execution_count += 1
        return f"RealSubject: Processando requisição de negócio com sucesso (Execução #{self.execution_count})."
