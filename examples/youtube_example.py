"""Exemplo executável do Proxy de Cache da Biblioteca do YouTube (Módulo 6).

Demonstra no terminal como o CachedYouTubeClass poupa tráfego de rede e tempo
ao interceptar as consultas da classe cliente YouTubeManager.

Como executar:
    python3 proxy/examples/youtube_example.py
"""

import os
import sys
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
PARENT_DIR = os.path.dirname(BASE_DIR)
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

from proxy.clients.youtube_manager import YouTubeManager
from proxy.proxies.cache_proxy import CachedYouTubeClass
from proxy.services.youtube_service import ThirdPartyYouTubeClass


def main() -> None:
    print("=" * 75)
    print("DEMONSTRAÇÃO DE CONSOLE: PROXY DE CACHE (BIBLIOTECA DO YOUTUBE)")
    print("Fiel ao Trabalho Acadêmico de Engenharia de Software II (Seção 4)")
    print("=" * 75)

    real_service = ThirdPartyYouTubeClass()
    cache_proxy = CachedYouTubeClass(real_service)
    manager = YouTubeManager(cache_proxy)

    print("\n--- 1ª RODADA: CACHE VAZIO (CACHE MISSES) ---")
    start = time.perf_counter()
    videos = manager.render_list_panel()
    dur_1 = (time.perf_counter() - start) * 1000
    print(f"[Listagem 1] {len(videos)} vídeos obtidos em {dur_1:.1f} ms (Bateu na API real)")

    start = time.perf_counter()
    info = manager.render_video_page("v101")
    dur_2 = (time.perf_counter() - start) * 1000
    print(f"[Detalhes 1] Vídeo '{info['title']}' obtido em {dur_2:.1f} ms (Bateu na API real)")

    start = time.perf_counter()
    down = manager.trigger_download("v101")
    dur_3 = (time.perf_counter() - start) * 1000
    print(f"[Download 1] {down['downloaded_mb']} MB baixados em {dur_3:.1f} ms ({down['source']})")

    print("\n--- 2ª RODADA: MESMAS SOLICITAÇÕES REPETIDAS (CACHE HITS) ---")
    start = time.perf_counter()
    videos_hit = manager.render_list_panel()
    dur_hit_1 = (time.perf_counter() - start) * 1000
    print(f"[Listagem 2] {len(videos_hit)} vídeos obtidos em {dur_hit_1:.1f} ms (INSTANTÂNEO DO CACHE!)")

    start = time.perf_counter()
    info_hit = manager.render_video_page("v101")
    dur_hit_2 = (time.perf_counter() - start) * 1000
    print(f"[Detalhes 2] Vídeo '{info_hit['title']}' obtido em {dur_hit_2:.1f} ms (INSTANTÂNEO DO CACHE!)")

    start = time.perf_counter()
    down_hit = manager.trigger_download("v101")
    dur_hit_3 = (time.perf_counter() - start) * 1000
    print(f"[Download 2] Baixado em {dur_hit_3:.1f} ms ({down_hit['source']})")

    print("\n" + "=" * 75)
    print("MÉTRICAS FINAIS DE EFICIÊNCIA:")
    metrics = cache_proxy.get_metrics()
    print(f" • Total de requisições do cliente : {metrics['total_requests']}")
    print(f" • Chamadas reais à API do YouTube : {real_service.network_call_count}")
    print(f" • Chamadas atendidas pelo Cache   : {metrics['cache_hits']} ({metrics['hit_ratio_pct']}%)")
    print(f" • Tempo total de rede economizado : {metrics['saved_latency_seconds']} segundos")
    print("=" * 75)


if __name__ == "__main__":
    main()
