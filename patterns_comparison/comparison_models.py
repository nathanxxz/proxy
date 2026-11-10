"""Módulo de Comparação com Outros Padrões de Projeto (Seção 8 do Documento).

Implementa exemplos concisos, didáticos e executáveis demonstrando as diferenças
arquiteturais entre:
1. Proxy: Mantém a MESMA interface e controla o acesso/ciclo de vida.
2. Adapter: Modifica / converte uma interface para torná-la compatível com o cliente.
3. Decorator: Mantém a mesma interface base mas adiciona novas responsabilidades compostas pelo cliente.
4. Facade: Cria uma NOVA interface simplificada para um subsistema complexo (não intercambiável).
"""

from abc import ABC, abstractmethod
from typing import Any

# ==============================================================================
# 1. SERVIÇO BASE COMUM (Notificação de Mensagens)
# ==============================================================================

class NotificationService(ABC):
    """Interface padrão de notificação esperada pelo sistema."""

    @abstractmethod
    def send(self, recipient: str, message: str) -> str:
        pass


class RealNotificationService(NotificationService):
    """Serviço real de envio de e-mails institucionais."""

    def send(self, recipient: str, message: str) -> str:
        return f"[E-mail Real] Enviado para '{recipient}': {message}"


# ==============================================================================
# 2. PROXY: Mesma Interface + Controle de Acesso e Taxa (Rate Limit)
# ==============================================================================

class NotificationProxy(NotificationService):
    """Proxy: Mantém a mesma interface e controla o acesso (filtra spam)."""

    def __init__(self, service: NotificationService | None = None) -> None:
        self._service: NotificationService = service or RealNotificationService()
        self.blocked_recipients: set[str] = {"spammer@hack.org", "blocked@test.com"}

    def send(self, recipient: str, message: str) -> str:
        if recipient in self.blocked_recipients:
            return f"[Proxy Bloqueio] Destinatário '{recipient}' bloqueado por segurança!"
        return f"[Proxy Interceptou] -> {self._service.send(recipient, message)}"


# ==============================================================================
# 3. ADAPTER: Adapta uma Interface Incompatível para a Interface Esperada
# ==============================================================================

class LegacySmsVendor:
    """Classe legada de terceiros com interface incompatível (método e parâmetros diferentes)."""

    def disparar_torpedo_celular(self, ddd: str, numero: str, texto_curto: str) -> str:
        return f"[SMS Antigo Legado] Torpedo para ({ddd}) {numero}: {texto_curto}"


class SmsAdapter(NotificationService):
    """Adapter: Converte a chamada send(recipient, message) para disparar_torpedo_celular()."""

    def __init__(self, legacy_sms: LegacySmsVendor) -> None:
        self._legacy = legacy_sms

    def send(self, recipient: str, message: str) -> str:
        # Extrai DDD e número do formato esperado (ex: '83999998888')
        ddd = recipient[:2] if len(recipient) >= 10 else "83"
        numero = recipient[2:] if len(recipient) >= 10 else recipient
        return self._legacy.disparar_torpedo_celular(ddd, numero, message)


# ==============================================================================
# 4. DECORATOR: Adiciona Responsabilidades em Cascata Compostas pelo Cliente
# ==============================================================================

class NotificationDecorator(NotificationService):
    """Base para Decorators que envolvem o serviço."""

    def __init__(self, wrappee: NotificationService) -> None:
        self._wrappee = wrappee

    def send(self, recipient: str, message: str) -> str:
        return self._wrappee.send(recipient, message)


class TimestampEncryptionDecorator(NotificationDecorator):
    """Decorator concreto: Adiciona carimbo de data e criptografia sem alterar a classe original."""

    def send(self, recipient: str, message: str) -> str:
        encrypted_msg = f"[CRIPTO-AES256: {message[::-1]}]"
        base_result = super().send(recipient, encrypted_msg)
        return f"{base_result} + [Assinatura Digital Anexada]"


# ==============================================================================
# 5. FACADE: Cria uma Interface Nova e Simplificada para um Subsistema Complexo
# ==============================================================================

class SmtpServer:
    def connect(self) -> str: return "SMTP Conectado."
    def authenticate(self, user: str) -> str: return f"Autenticado como {user}."

class TemplateEngine:
    def compile_template(self, tpl: str, data: dict[str, Any]) -> str:
        return f"HTML Renderizado: {tpl} com {data}"

class DeliveryAuditor:
    def record_dispatch(self, id_msg: str) -> str: return f"Despacho {id_msg} arquivado."


class NotificationFacade:
    """Facade: Não implementa NotificationService! Cria uma API única e simples para 3 subsistemas."""

    def __init__(self) -> None:
        self.smtp = SmtpServer()
        self.template = TemplateEngine()
        self.auditor = DeliveryAuditor()

    def enviar_comunicado_oficial(self, aluno: str, matricula: str, aviso: str) -> list[str]:
        """Método de fachada simples que esconde toda a dança de múltiplos subsistemas."""
        steps = [
            self.smtp.connect(),
            self.smtp.authenticate("secretaria@fafic.edu.br"),
            self.template.compile_template("boletim.html", {"aluno": aluno, "matricula": matricula, "aviso": aviso}),
            self.auditor.record_dispatch("DISP-9981"),
            f"Comunicado entregue com sucesso para {aluno}!",
        ]
        return steps
