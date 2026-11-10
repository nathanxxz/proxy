"""Interface base para o Módulo 1 — Estrutura Básica do Padrão Proxy.

Participante: Interface do Serviço (Subject).
Define a interface comum para o RealSubject e o Proxy, de forma que o
Cliente possa trabalhar indistintamente com qualquer um deles.
"""

from abc import ABC, abstractmethod


class Subject(ABC):
    """Contrato abstrato que define a operação principal do serviço."""

    @abstractmethod
    def request(self) -> str:
        """Executa a requisição principal do serviço.

        Returns:
            str: Mensagem ou resultado do processamento da requisição.
        """
        pass
