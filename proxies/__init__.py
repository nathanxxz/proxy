"""Módulo de proxies do projeto acadêmico Padrão Proxy."""

from proxy.proxies.basic_proxy import BasicProxy
from proxy.proxies.cache_proxy import CachedYouTubeClass
from proxy.proxies.logging_proxy import LoggingDocumentProxy
from proxy.proxies.protection_proxy import ProtectionAdminProxy, UserRole
from proxy.proxies.remote_proxy import RemoteServiceProxy
from proxy.proxies.smart_reference_proxy import SmartReferenceProxy
from proxy.proxies.virtual_proxy import VirtualDatabaseProxy

__all__ = [
    "BasicProxy",
    "VirtualDatabaseProxy",
    "ProtectionAdminProxy",
    "UserRole",
    "RemoteServiceProxy",
    "LoggingDocumentProxy",
    "CachedYouTubeClass",
    "SmartReferenceProxy",
]
