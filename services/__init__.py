"""Módulo de serviços reais (RealSubjects) do projeto acadêmico Padrão Proxy."""

from proxy.services.admin_service import RealAdminService
from proxy.services.database_service import HeavyDatabaseService
from proxy.services.document_service import RealDocumentService
from proxy.services.real_subject import RealSubject
from proxy.services.remote_service import RealRemoteServer
from proxy.services.resource_service import SharedResourceService
from proxy.services.youtube_service import ThirdPartyYouTubeClass

__all__ = [
    "RealSubject",
    "HeavyDatabaseService",
    "RealAdminService",
    "RealRemoteServer",
    "RealDocumentService",
    "ThirdPartyYouTubeClass",
    "SharedResourceService",
]
