"""Implementação do Proxy Básico para o Módulo 1 — Estrutura Básica do Padrão Proxy.

Participante: Proxy.
Mantém uma referência ao Serviço Real (RealSubject), implementa a mesma interface
(Subject) e controla o acesso, podendo executar ações antes e depois de repassar a chamada.
"""

from proxy.interfaces.subject import Subject
from proxy.services.real_subject import RealSubject


class BasicProxy(Subject):
    """Proxy da estrutura clássica do padrão."""

    def __init__(self, real_subject: RealSubject | None = None) -> None:
        """Inicializa o Proxy com uma referência opcional ao serviço real.

        Args:
            real_subject: Instância do serviço real. Se omitido, pode ser criado sob demanda.
        """
        self._real_subject: RealSubject | None = real_subject
        self.pre_processing_logs: list[str] = []
        self.post_processing_logs: list[str] = []

    def _check_access(self) -> bool:
        """Lógica executada ANTES de delegar ao serviço real."""
        log = "Proxy: [Pré-processamento] Verificando acesso e estado antes de delegar a chamada."
        self.pre_processing_logs.append(log)
        return True

    def _log_access(self) -> None:
        """Lógica executada DEPOIS de receber o resultado do serviço real."""
        log = "Proxy: [Pós-processamento] Chamada registrada no histórico de auditoria."
        self.post_processing_logs.append(log)

    def request(self) -> str:
        """Implementa o método da interface Subject delegando ao serviço real."""
        # Ação pré-delegação
        if self._check_access():
            # Lazy creation se o serviço real ainda não foi fornecido
            if self._real_subject is None:
                self._real_subject = RealSubject()

            # Delegação da chamada para o objeto real
            resultado_real = self._real_subject.request()

            # Ação pós-delegação
            self._log_access()

            return f"Proxy interceptou -> {resultado_real} -> Proxy finalizou."

        return "Proxy: Acesso negado."
