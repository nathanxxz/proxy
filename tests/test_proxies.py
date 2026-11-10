"""Suíte de testes automatizados com pytest para o Padrão de Projeto Proxy.

Cobre todos os 7 módulos práticos e a comparação com padrões vizinhos:
1. Estrutura Básica (Subject, RealSubject, Proxy, Client).
2. Proxy Virtual (Lazy Initialization e reutilização de instâncias).
3. Proxy de Proteção (Controle de acesso por papel e bloqueio não autorizado).
4. Proxy Remoto (Encaminhamento de chamadas e desempacotamento RPC).
5. Proxy de Log (Auditoria de parâmetros, resultados e captura de erros).
6. Proxy de Cache (Biblioteca do YouTube, cache hits, misses e economia de chamadas).
7. Referência Inteligente (Contador de referências e desalocação automática).
8. Comparação com outros padrões (Adapter, Decorator e Facade).
"""

import pytest

from proxy.clients.client import ClientApp
from proxy.clients.youtube_manager import YouTubeManager
from proxy.patterns_comparison.comparison_models import (
    LegacySmsVendor,
    NotificationFacade,
    NotificationProxy,
    RealNotificationService,
    SmsAdapter,
    TimestampEncryptionDecorator,
)
from proxy.proxies.basic_proxy import BasicProxy
from proxy.proxies.cache_proxy import CachedYouTubeClass
from proxy.proxies.logging_proxy import LoggingDocumentProxy
from proxy.proxies.protection_proxy import ProtectionAdminProxy, UserRole
from proxy.proxies.remote_proxy import RemoteServiceProxy
from proxy.proxies.smart_reference_proxy import SmartReferenceProxy
from proxy.proxies.virtual_proxy import VirtualDatabaseProxy
from proxy.services.admin_service import RealAdminService
from proxy.services.document_service import RealDocumentService
from proxy.services.real_subject import RealSubject
from proxy.services.remote_service import RealRemoteServer
from proxy.services.resource_service import SharedResourceService
from proxy.services.youtube_service import ThirdPartyYouTubeClass


# ==============================================================================
# 1. TESTES DA ESTRUTURA BÁSICA
# ==============================================================================

def test_basic_proxy_transparency_to_client() -> None:
    """Verifica se o Cliente consome RealSubject e BasicProxy com a mesma interface."""
    real_subject = RealSubject()
    proxy = BasicProxy(real_subject)

    # Cliente consumindo serviço real diretamente
    client_direct = ClientApp(real_subject)
    result_direct = client_direct.run_business_operation()
    assert "RealSubject" in result_direct
    assert real_subject.execution_count == 1

    # Cliente consumindo através do Proxy sem alterar nenhuma linha
    client_via_proxy = ClientApp(proxy)
    result_proxy = client_via_proxy.run_business_operation()
    assert "Proxy interceptou" in result_proxy
    assert "RealSubject" in result_proxy
    assert real_subject.execution_count == 2
    assert len(proxy.pre_processing_logs) == 1
    assert len(proxy.post_processing_logs) == 1


# ==============================================================================
# 2. TESTES DO PROXY VIRTUAL (LAZY INITIALIZATION)
# ==============================================================================

def test_virtual_proxy_lazy_initialization() -> None:
    """Garante que o banco pesado NÃO seja criado na instanciação do proxy, apenas na 1ª query."""
    proxy = VirtualDatabaseProxy()
    # Verifica que o serviço real ainda não foi instanciado
    assert not proxy.is_service_instantiated
    assert proxy.get_status()["is_instantiated"] is False

    # Primeira consulta: deve instanciar o serviço sob demanda (Lazy Loading)
    records = proxy.query("SELECT * FROM alunos")
    assert len(records) > 0
    assert proxy.is_service_instantiated
    assert proxy.get_status()["is_instantiated"] is True
    assert proxy.total_calls == 1


def test_virtual_proxy_instance_reuse() -> None:
    """Verifica se as consultas subsequentes reutilizam a mesma instância sem recriar conexão."""
    proxy = VirtualDatabaseProxy()

    # 1ª Consulta: Cria
    proxy.query("SELECT 1")
    instance_first = proxy._real_database
    assert instance_first is not None

    # 2ª Consulta: Reutiliza
    proxy.query("SELECT 2")
    instance_second = proxy._real_database

    # Confirma que é rigorosamente o mesmo objeto na memória
    assert instance_first is instance_second
    assert proxy.total_calls == 2
    assert instance_second.query_count == 2


# ==============================================================================
# 3. TESTES DO PROXY DE PROTEÇÃO
# ==============================================================================

def test_protection_proxy_authorized_admin() -> None:
    """Verifica que o usuário ADMIN possui permissão para todas as operações sensíveis."""
    real_admin = RealAdminService()
    proxy = ProtectionAdminProxy(real_admin)

    # Alterar configuração como ADMIN
    res_cfg = proxy.alterar_configuracao("NIVEL_LOG", "DEBUG", "admin_joao", UserRole.ADMIN)
    assert res_cfg["status"] == "SUCESSO"
    assert real_admin.configuracoes["NIVEL_LOG"] == "DEBUG"

    # Excluir usuário como ADMIN
    res_del = proxy.excluir_usuario(104, "admin_joao", UserRole.ADMIN)
    assert res_del["status"] == "SUCESSO"
    assert 104 not in real_admin.usuarios_ativos

    # Reiniciar servidor como ADMIN
    res_boot = proxy.reiniciar_servidor("Atualização de Kernel", "admin_joao", UserRole.ADMIN)
    assert res_boot["status"] == "REINICIALIZACAO_AGENDADA"


def test_protection_proxy_blocked_access_raises_permission_error() -> None:
    """Verifica que usuários sem privilégio são bloqueados com PermissionError e logados."""
    real_admin = RealAdminService()
    proxy = ProtectionAdminProxy(real_admin)

    # CONVIDADO tentando alterar configuração
    with pytest.raises(PermissionError) as exc_info:
        proxy.alterar_configuracao("NIVEL_LOG", "DEBUG", "visitante", UserRole.CONVIDADO)
    assert "Acesso bloqueado" in str(exc_info.value)

    # OPERADOR tentando excluir usuário (restrito a ADMIN)
    with pytest.raises(PermissionError) as exc_info_del:
        proxy.excluir_usuario(101, "operador_lucas", UserRole.OPERADOR)
    assert "apenas usuários com perfil 'ADMIN'" in str(exc_info_del.value)

    # Verifica se os bloqueios foram arquivados nos logs de segurança
    failed_logs = [log for log in proxy.security_logs if not log["autorizada"]]
    assert len(failed_logs) == 2


# ==============================================================================
# 4. TESTES DO PROXY REMOTO
# ==============================================================================

def test_remote_proxy_call_forwarding() -> None:
    """Verifica se o proxy remoto serializa, transmite e desempacota dados transparentemente."""
    server = RealRemoteServer()
    proxy = RemoteServiceProxy(server)

    # Relatório de servidor remoto
    report = proxy.obter_relatorio_servidor("SRV-NODE-01")
    assert report["status"] == 200
    assert report["server_id"] == "SRV-NODE-01"
    assert report["hostname"] == "cloud-node-pb-01.local"

    # Cálculo distribuído remoto
    calc = proxy.executar_calculo_distribuido([10.0, 20.0, 30.0], "media")
    assert calc["status"] == 200
    assert calc["resultado"] == 20.0

    # Confirma que o servidor físico recebeu as mensagens
    assert server.total_packets_received == 2
    assert len(proxy.network_transmission_logs) == 2


def test_remote_proxy_unsupported_operation() -> None:
    """Verifica o tratamento de erro quando uma operação remota falha."""
    proxy = RemoteServiceProxy()
    with pytest.raises(ConnectionError):
        proxy.executar_calculo_distribuido([1.0, 2.0], "operacao_inexistente")


# ==============================================================================
# 5. TESTES DO PROXY DE LOG (AUDITORIA)
# ==============================================================================

def test_logging_proxy_audit_trail_and_error_capture() -> None:
    """Verifica se todas as operações são registradas com parâmetros, timestamps e erros."""
    real_doc = RealDocumentService()
    proxy = LoggingDocumentProxy(real_doc)

    # Emissão com sucesso
    doc = proxy.emitir_declaracao("2024.2060063", "Sistemas de Informação", "Vínculo Regular")
    assert doc["status"] == "VALIDO"

    # Assinatura com sucesso
    sign = proxy.assinar_documento(doc["documento_id"], "CHAVE-MESTRA-2026")
    assert sign["status_assinatura"] == "ASSINADO_DIGITALMENTE"

    # Tentativa com erro intencional
    with pytest.raises(ValueError):
        proxy.emitir_declaracao("INVALIDA", "Qualquer", "Vínculo")

    # Verifica histórico de auditoria
    assert len(proxy.call_history) == 3
    assert proxy.call_history[0]["sucesso"] is True
    assert proxy.call_history[0]["operacao"] == "emitir_declaracao"
    assert proxy.call_history[1]["sucesso"] is True
    assert proxy.call_history[1]["operacao"] == "assinar_documento"
    assert proxy.call_history[2]["sucesso"] is False
    assert "inválida no sistema" in proxy.call_history[2]["erro"]


# ==============================================================================
# 6. TESTES DO PROXY DE CACHE (BIBLIOTECA DO YOUTUBE)
# ==============================================================================

def test_cached_youtube_hit_miss_and_call_economy() -> None:
    """Fiel ao exemplo do YouTube: testa cache misses na 1ª chamada e cache hits nas seguintes."""
    real_lib = ThirdPartyYouTubeClass()
    proxy = CachedYouTubeClass(real_lib)

    # 1. Listagem de vídeos
    # 1ª chamada: Cache Miss (busca no serviço real)
    videos_1 = proxy.list_videos()
    assert len(videos_1) == 3
    assert real_lib.list_call_count == 1
    assert proxy.cache_misses == 1
    assert proxy.cache_hits == 0

    # 2ª chamada: Cache Hit (retorna da memória instantaneamente)
    videos_2 = proxy.list_videos()
    assert len(videos_2) == 3
    assert real_lib.list_call_count == 1  # Serviço real NÃO foi chamado de novo!
    assert proxy.cache_hits == 1

    # 2. Informações de vídeo específico
    info_1 = proxy.get_video_info("v101")
    assert real_lib.info_call_count == 1
    assert proxy.cache_misses == 2

    info_2 = proxy.get_video_info("v101")
    assert real_lib.info_call_count == 1  # Economizado!
    assert proxy.cache_hits == 2

    # 3. Download de vídeo
    down_1 = proxy.download_video("v102")
    assert real_lib.download_call_count == 1

    down_2 = proxy.download_video("v102")
    assert real_lib.download_call_count == 1  # Download economizado!
    assert "CACHE_LOCAL" in down_2["source"]

    # Métricas
    metrics = proxy.get_metrics()
    assert metrics["cache_hits"] >= 3
    assert metrics["saved_latency_seconds"] > 0.0


def test_youtube_manager_client_integration() -> None:
    """Verifica se a classe cliente YouTubeManager opera perfeitamente com o CachedYouTubeClass."""
    proxy = CachedYouTubeClass()
    manager = YouTubeManager(proxy)

    videos = manager.render_list_panel()
    assert len(videos) > 0
    assert "renderizada" in manager.last_rendered_content

    info = manager.render_video_page("v101")
    assert info["id"] == "v101"

    down = manager.trigger_download("v101")
    assert down["video_id"] == "v101"


# ==============================================================================
# 7. TESTES DA REFERÊNCIA INTELIGENTE (SMART REFERENCE)
# ==============================================================================

def test_smart_reference_counting_and_auto_deallocate() -> None:
    """Verifica contagem de clientes ativos e liberação automática quando referências zeram."""
    real_resource = SharedResourceService("Pool-Academico-Principal")
    proxy = SmartReferenceProxy(real_resource)

    # Estado inicial
    assert proxy.reference_count == 0
    assert real_resource.is_allocated is True
    assert proxy.auto_released is False

    # Cliente 1 conecta
    proxy.acquire_reference("ModuloMatricula")
    assert proxy.reference_count == 1

    # Cliente 2 conecta
    proxy.acquire_reference("ModuloFinanceiro")
    assert proxy.reference_count == 2

    # Operações de leitura/escrita com clientes ativos
    res_read = proxy.read_data("ModuloMatricula")
    assert res_read["status"] == "LIDO_COM_SUCESSO"

    # Cliente 1 libera sua referência
    proxy.release_reference("ModuloMatricula")
    assert proxy.reference_count == 1
    assert real_resource.is_allocated is True  # Ainda ativo pois restam clientes

    # Cliente 2 libera a última referência restante
    proxy.release_reference("ModuloFinanceiro")
    assert proxy.reference_count == 0

    # Regra da Referência Inteligente: o recurso deve ter sido liberado automaticamente!
    assert proxy.auto_released is True
    assert real_resource.is_allocated is False

    # Tentativa de acesso após desalocação deve lançar erro
    with pytest.raises(RuntimeError):
        proxy.read_data("ClienteAtrasado")


# ==============================================================================
# 8. TESTES DE COMPARAÇÃO COM OUTROS PADRÕES
# ==============================================================================

def test_patterns_comparison_behavior() -> None:
    """Testa as diferenças arquiteturais entre Proxy, Adapter, Decorator e Facade."""
    # 1. Proxy: Mesma interface + controle de acesso
    proxy = NotificationProxy()
    assert "[Proxy Interceptou]" in proxy.send("aluno@fafic.br", "Aviso de aula")
    assert "[Proxy Bloqueio]" in proxy.send("spammer@hack.org", "Spam")

    # 2. Adapter: Adapta classe incompatível (LegacySmsVendor) para a interface NotificationService
    legacy = LegacySmsVendor()
    adapter = SmsAdapter(legacy)
    res_adapter = adapter.send("83999991111", "Seu boleto venceu")
    assert "[SMS Antigo Legado]" in res_adapter

    # 3. Decorator: Composição de novas responsabilidades em camadas
    real_notif = RealNotificationService()
    decorator = TimestampEncryptionDecorator(real_notif)
    res_dec = decorator.send("aluno@fafic.br", "Segredo")
    assert "[CRIPTO-AES256" in res_dec
    assert "[Assinatura Digital Anexada]" in res_dec

    # 4. Facade: Nova interface simplificada para orquestrar 3 subsistemas
    facade = NotificationFacade()
    steps = facade.enviar_comunicado_oficial("Fabricio Nathan", "2024.2060063", "Aprovado em ES II")
    assert len(steps) == 5
    assert "SMTP Conectado." in steps[0]
