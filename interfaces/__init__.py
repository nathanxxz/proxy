"""Módulo de interfaces abstratas do projeto acadêmico Padrão Proxy."""

from proxy.interfaces.admin_interface import AdminServiceInterface
from proxy.interfaces.database_interface import DatabaseInterface
from proxy.interfaces.document_interface import DocumentServiceInterface
from proxy.interfaces.remote_interface import RemoteServiceInterface
from proxy.interfaces.resource_interface import SharedResourceInterface
from proxy.interfaces.subject import Subject
from proxy.interfaces.youtube_interface import ThirdPartyYouTubeLib

__all__ = [
    "Subject",
    "DatabaseInterface",
    "AdminServiceInterface",
    "RemoteServiceInterface",
    "DocumentServiceInterface",
    "ThirdPartyYouTubeLib",
    "SharedResourceInterface",
]
