"""Implementação do Serviço Real da Biblioteca do YouTube (Módulo 6 — Proxy de Cache).

Fiel ao trabalho acadêmico:
Representa a classe ThirdPartyYouTubeClass de uma biblioteca de terceiros.
Como não podemos modificar seu código-fonte, suas chamadas diretas são lentas
e repetem requisições de rede a cada solicitação.
"""

import time
from typing import Any

from proxy.interfaces.youtube_interface import ThirdPartyYouTubeLib


class ThirdPartyYouTubeClass(ThirdPartyYouTubeLib):
    """Serviço Real da Biblioteca do YouTube (RealSubject de Terceiros).

    Simula chamadas lentas de API e downloads repetidos através de rede.
    """

    def __init__(self) -> None:
        self.network_call_count: int = 0
        self.download_call_count: int = 0
        self.info_call_count: int = 0
        self.list_call_count: int = 0

        # Banco de dados simulado no YouTube
        self._videos_database: dict[str, dict[str, Any]] = {
            "v101": {
                "id": "v101",
                "title": "Padrão de Projeto Proxy — Teoria e Prática Completa",
                "channel": "Engenharia de Software FAFIC",
                "duration": "18:42",
                "size_mb": 145.0,
                "views": 15420,
            },
            "v102": {
                "id": "v102",
                "title": "Design Patterns: Gang of Four em Python 3.14",
                "channel": "Arquitetura de Software Pro",
                "duration": "24:15",
                "size_mb": 210.5,
                "views": 89200,
            },
            "v103": {
                "id": "v103",
                "title": "Lazy Initialization e Proxy Virtual no Mundo Real",
                "channel": "Refactoring Guru Fan Club",
                "duration": "12:08",
                "size_mb": 95.0,
                "views": 32100,
            },
        }

    def list_videos(self) -> list[dict[str, Any]]:
        """Simula requisição HTTP GET /videos para a API do YouTube (lenta)."""
        self.network_call_count += 1
        self.list_call_count += 1
        # Simula latência de rede de 400ms
        time.sleep(0.4)
        return list(self._videos_database.values())

    def get_video_info(self, video_id: str) -> dict[str, Any]:
        """Simula requisição HTTP GET /videos/{id} com metadados (lenta)."""
        self.network_call_count += 1
        self.info_call_count += 1
        # Simula latência de rede de 350ms
        time.sleep(0.35)

        video = self._videos_database.get(video_id)
        if not video:
            raise KeyError(f"Vídeo com ID '{video_id}' não encontrado no YouTube.")
        return dict(video)

    def download_video(self, video_id: str) -> dict[str, Any]:
        """Simula download pesado de stream de vídeo pela rede (muito lento)."""
        self.network_call_count += 1
        self.download_call_count += 1
        # Simula latência de download de stream binário (700ms)
        time.sleep(0.7)

        video = self.get_video_info(video_id)
        return {
            "video_id": video_id,
            "title": video["title"],
            "downloaded_mb": video["size_mb"],
            "format": "mp4 (1080p60)",
            "source": "REDE_YOUTUBE_DIRETA",
        }
