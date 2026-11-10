"""Implementação do Serviço Real de Documentos para o Módulo 5 (Proxy de Log).

Executa a emissão e assinatura de documentos acadêmicos e corporativos.
"""

import hashlib
import uuid
from datetime import datetime
from typing import Any

from proxy.interfaces.document_interface import DocumentServiceInterface


class RealDocumentService(DocumentServiceInterface):
    """Serviço Real de Emissão de Documentos (RealSubject)."""

    def __init__(self) -> None:
        self.total_documentos_gerados: int = 0

    def emitir_declaracao(self, matricula: str, curso: str, tipo_declaracao: str) -> dict[str, Any]:
        """Gera a declaração institucional solicitada."""
        self.total_documentos_gerados += 1
        codigo_validacao = str(uuid.uuid4())[:8].upper()

        if matricula.strip() == "INVALIDA":
            raise ValueError(f"Matrícula '{matricula}' inválida no sistema acadêmico.")

        return {
            "documento_id": f"DOC-{self.total_documentos_gerados:04d}",
            "tipo": tipo_declaracao,
            "matricula": matricula,
            "curso": curso,
            "codigo_autenticidade": f"FAFIC-{codigo_validacao}",
            "emissao": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "status": "VALIDO",
        }

    def assinar_documento(self, documento_id: str, chave_assinante: str) -> dict[str, Any]:
        """Aplica a assinatura criptográfica SHA-256 no documento."""
        if not chave_assinante or len(chave_assinante) < 5:
            raise ValueError("Chave de assinatura criptográfica inválida ou expirada.")

        raw_signature = f"{documento_id}:{chave_assinante}:{datetime.now().isoformat()}"
        hash_assinatura = hashlib.sha256(raw_signature.encode()).hexdigest()

        return {
            "documento_id": documento_id,
            "status_assinatura": "ASSINADO_DIGITALMENTE",
            "algoritmo": "SHA-256",
            "hash_assinatura": hash_assinatura[:32] + "...",
            "data_assinatura": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        }
