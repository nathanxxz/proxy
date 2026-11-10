"""Módulo de comparação com padrões vizinhos (Adapter, Decorator, Facade)."""

from proxy.patterns_comparison.comparison_models import (
    LegacySmsVendor,
    NotificationDecorator,
    NotificationFacade,
    NotificationProxy,
    NotificationService,
    RealNotificationService,
    SmsAdapter,
    TimestampEncryptionDecorator,
)

__all__ = [
    "NotificationService",
    "RealNotificationService",
    "NotificationProxy",
    "LegacySmsVendor",
    "SmsAdapter",
    "NotificationDecorator",
    "TimestampEncryptionDecorator",
    "NotificationFacade",
]
