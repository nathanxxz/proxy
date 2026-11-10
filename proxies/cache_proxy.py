"""Implementação do Proxy de Cache para o Módulo 6 (Biblioteca do YouTube).

Fiel ao trabalho acadêmico (Seção 4):
Implementa a classe CachedYouTubeClass com a mesma interface ThirdPartyYouTubeLib.
Armazena em memória as listagens, metadados e downloads efetuados para evitar
requisições repetidas e lentas à biblioteca real de terceiros.
Calcula métricas didáticas de acertos de cache (cache hits) e economia de processamento/tempo.
"""

import time
from typing import Any

from proxy.interfaces.youtube_interface import ThirdPartyYouTubeLib
from proxy.services.youtube_service import ThirdPartyYouTubeClass


class CachedYouTubeClass(ThirdPartyYouTubeLib):
    """Proxy de Cache para a Biblioteca de Vídeos do YouTube (CachedYouTubeClass).

    Controla o acesso à biblioteca ThirdPartyYouTubeClass sem alterar sua estrutura.
    """

    def __init__(self, service: ThirdPartyYouTubeLib | None = None) -> None:
        self._service: ThirdPartyYouTubeLib = service or ThirdPartyYouTubeClass()
        self._list_cache: list[dict[str, Any]] | None = None
        self._video_info_cache: dict[str, dict[str, Any]] = {}
        self._download_cache: dict[str, dict[str, Any]] = {}

        # Métricas para acompanhamento didático
        self.cache_hits: int = 0
        self.cache_misses: int = 0
        self.total_requests: int = 0
        self.saved_latency_seconds: float = 0.0

    def list_videos(self) -> list[dict[str, Any]]:
        """Retorna a lista de vídeos, consultando o cache quando disponível."""
        self.total_requests += 1

        if self._list_cache is not None:
            self.cache_hits += 1
            # Economizou ~400ms de chamada de rede simulada
            self.saved_latency_seconds += 0.40
            return self._list_cache

        self.cache_misses += 1
        # Busca no serviço real e preenche o cache
        self._list_cache = self._service.list_videos()
        return self._list_cache

    def get_video_info(self, video_id: str) -> dict[str, Any]:
        """Retorna os metadados do vídeo consultando o cache em memória."""
        self.total_requests += 1

        if video_id in self._video_info_cache:
            self.cache_hits += 1
            # Economizou ~350ms de chamada de rede simulada
            self.saved_latency_seconds += 0.35
            return self._video_info_cache[video_id]

        self.cache_misses += 1
        video_data = self._service.get_video_info(video_id)
        self._video_info_cache[video_id] = video_data
        return video_data

    def download_video(self, video_id: str) -> dict[str, Any]:
        """Baixa o vídeo apenas se ele ainda não estiver no cache local."""
        self.total_requests += 1

        if video_id in self._download_cache:
            self.cache_hits += 1
            # Economizou ~700ms de download pesado
            self.saved_latency_seconds += 0.70
            cached_result = dict(self._download_cache[video_id])
            cached_result["source"] = "CACHE_LOCAL_MEMORIA (0ms)"
            return cached_result

        self.cache_misses += 1
        download_result = self._service.download_video(video_id)
        self._download_cache[video_id] = download_result
        return download_result

    def reset_cache(self) -> None:
        """Limpa todo o cache para demonstração de cache miss e renovação."""
        self._list_cache = None
        self._video_info_cache.clear()
        self._download_cache.clear()

    def get_metrics(self) -> dict[str, Any]:
        """Retorna o sumário de telemetria e eficiência do Proxy de Cache."""
        hit_ratio = round((self.cache_hits / self.total_requests) * 100, 1) if self.total_requests > 0 else 0.0
        return {
            "total_requests": self.total_requests,
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "hit_ratio_pct": hit_ratio,
            "saved_latency_seconds": round(self.saved_latency_seconds, 2),
            "cached_video_count": len(self._video_info_cache),
            "cached_downloads_count": len(self._download_cache),
        }
