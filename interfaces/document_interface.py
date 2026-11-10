"""Interface para o Módulo 5 — Proxy de Log (Registro e Auditoria).

Define o contrato para processamento e emissão de documentos acadêmicos/empresariais.
"""

from abc import ABC, abstractmethod
from typing import Any


class DocumentServiceInterface(ABC):
    """Contrato abstrato para emissão e assinatura de documentos digitais."""

    @abstractmethod
    def emitir_declaracao(self, matricula: str, curso: str, tipo_declaracao: str) -> dict[str, Any]:
        """Emite uma declaração institucional oficial.

        Args:
            matricula: Matrícula discente.
            curso: Nome do curso de graduação.
            tipo_declaracao: Tipo de documento (matrícula, conclusão, vínculo).

        Returns:
            dict[str, Any]: Dados do documento gerado e código de validação.
        """
        pass

    @abstractmethod
    def assinar_documento(self, documento_id: str, chave_assinante: str) -> dict[str, Any]:
        """Aplica assinatura digital criptográfica em um documento.

        Args:
            documento_id: Identificador único do documento.
            chave_assinante: Chave pública ou certificado do assinante.

        Returns:
            dict[str, Any]: Confirmação da assinatura e hash gerado.
        """
        pass
