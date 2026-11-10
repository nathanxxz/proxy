"""Implementação do Proxy de Log (Registro e Auditoria) para o Módulo 5.

Fiel ao trabalho acadêmico:
Intercepta e registra todas as operações executadas sobre o serviço real,
armazenando nome do método, data/horário, parâmetros de entrada, resultado,
duração da chamada e captura de eventuais exceções.
"""

import time
from datetime import datetime
from typing import Any

from proxy.interfaces.document_interface import DocumentServiceInterface
from proxy.services.document_service import RealDocumentService


class LoggingDocumentProxy(DocumentServiceInterface):
    """Proxy de Log / Auditoria para Serviços de Documentos."""

    def __init__(self, real_service: RealDocumentService | None = None) -> None:
        self._real_service: RealDocumentService = real_service or RealDocumentService()
        self.call_history: list[dict[str, Any]] = []

    def _record_audit_entry(
        self,
        operacao: str,
        parametros: dict[str, Any],
        resultado: Any | None,
        erro: str | None,
        duracao_ms: float,
    ) -> None:
        """Adiciona uma entrada estruturada no histórico de auditoria."""
        self.call_history.append({
            "id": len(self.call_history) + 1,
            "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "operacao": operacao,
            "parametros": parametros,
            "resultado": resultado,
            "erro": erro,
            "sucesso": erro is None,
            "duracao_ms": duracao_ms,
        })

    def emitir_declaracao(self, matricula: str, curso: str, tipo_declaracao: str) -> dict[str, Any]:
        """Intercepta, audita e delega a emissão de declaração."""
        params = {"matricula": matricula, "curso": curso, "tipo_declaracao": tipo_declaracao}
        start = time.perf_counter()
        resultado = None
        erro_msg = None

        try:
            resultado = self._real_service.emitir_declaracao(matricula, curso, tipo_declaracao)
            return resultado
        except Exception as exc:
            erro_msg = str(exc)
            raise exc
        finally:
            elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
            self._record_audit_entry("emitir_declaracao", params, resultado, erro_msg, elapsed_ms)

    def assinar_documento(self, documento_id: str, chave_assinante: str) -> dict[str, Any]:
        """Intercepta, audita e delega a assinatura digital de documento."""
        # Ofusca a chave por segurança nos parâmetros salvos em log
        chave_ofuscada = chave_assinante[:4] + "****" if len(chave_assinante) > 4 else "****"
        params = {"documento_id": documento_id, "chave_assinante": chave_ofuscada}
        start = time.perf_counter()
        resultado = None
        erro_msg = None

        try:
            resultado = self._real_service.assinar_documento(documento_id, chave_assinante)
            return resultado
        except Exception as exc:
            erro_msg = str(exc)
            raise exc
        finally:
            elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
            self._record_audit_entry("assinar_documento", params, resultado, erro_msg, elapsed_ms)
