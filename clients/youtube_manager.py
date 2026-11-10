"""Implementação do Cliente YouTubeManager (Módulo 6 — Exemplo do YouTube).

Fiel ao trabalho acadêmico (Seção 4):
A classe YouTubeManager simula a camada de interface e apresentação da aplicação.
Ela depende exclusivamente da interface ThirdPartyYouTubeLib, podendo ser
injetada com o serviço direto (ThirdPartyYouTubeClass) ou com o Proxy de Cache
(CachedYouTubeClass) sem que uma única linha do seu código precise ser alterada.
"""

from typing import Any

from proxy.interfaces.youtube_interface import ThirdPartyYouTubeLib


class YouTubeManager:
    """Gerenciador e Renderizador de Vídeos (Client)."""

    def __init__(self, service: ThirdPartyYouTubeLib) -> None:
        """Injeta a biblioteca via interface comum."""
        self._service: ThirdPartyYouTubeLib = service
        self.last_rendered_content: str = ""

    def render_list_panel(self) -> list[dict[str, Any]]:
        """Solicita a lista de vídeos para montar a grade de exibição."""
        videos = self._service.list_videos()
        self.last_rendered_content = f"Lista de {len(videos)} vídeos renderizada na tela."
        return videos

    def render_video_page(self, video_id: str) -> dict[str, Any]:
        """Solicita os metadados do vídeo para renderizar a página do player."""
        info = self._service.get_video_info(video_id)
        self.last_rendered_content = f"Página do vídeo '{info.get('title')}' renderizada."
        return info

    def trigger_download(self, video_id: str) -> dict[str, Any]:
        """Dispara a ação do usuário de baixar o arquivo para reprodução offline."""
        download_info = self._service.download_video(video_id)
        self.last_rendered_content = f"Download concluído: {download_info.get('title')} ({download_info.get('downloaded_mb')} MB)."
        return download_info
