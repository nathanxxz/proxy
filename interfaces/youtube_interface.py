"""Interface para o Módulo 6 — Proxy de Cache (Biblioteca do YouTube).

Fiel ao exemplo acadêmico:
Define a interface ThirdPartyYouTubeLib que tanto a classe real da biblioteca
de terceiros (ThirdPartyYouTubeClass) quanto o Proxy de cache (CachedYouTubeClass)
precisam implementar rigorosamente.
"""

from abc import ABC, abstractmethod
from typing import Any


class ThirdPartyYouTubeLib(ABC):
    """Contrato abstrato que define as operações da biblioteca do YouTube."""

    @abstractmethod
    def list_videos(self) -> list[dict[str, Any]]:
        """Lista os vídeos disponíveis na plataforma.

        Returns:
            list[dict[str, Any]]: Coleção de vídeos populares com metadados.
        """
        pass

    @abstractmethod
    def get_video_info(self, video_id: str) -> dict[str, Any]:
        """Consulta informações detalhadas e metadados de um vídeo específico.

        Args:
            video_id: Identificador único do vídeo (ex: 'v101').

        Returns:
            dict[str, Any]: Detalhes completos do vídeo (título, autor, duração, views).
        """
        pass

    @abstractmethod
    def download_video(self, video_id: str) -> dict[str, Any]:
        """Simula o download do stream de mídia do vídeo.

        Args:
            video_id: Identificador único do vídeo a ser baixado.

        Returns:
            dict[str, Any]: Informações do arquivo baixado (nome, tamanho_mb, bytes).
        """
        pass
