"""Laboratório Interativo do Padrão de Projeto Proxy.

Disciplina: Engenharia de Software II (Cajazeiras-PB, 2026)
Equipe:
- João Pedro Cruz
- Pedro Henrique
- Pedro Arlyx
- Fabricio Nathan
- Lucas Gonçalves

Aplicação gráfica desenvolvida com Streamlit para demonstração visual, prática e
didática de todos os conceitos, tipos e comparações do padrão estrutural Proxy.
"""

import os
import sys
import time
from typing import Any

import streamlit as st

# Garante que o diretório raiz do projeto esteja no sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
PARENT_DIR = os.path.dirname(BASE_DIR)
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

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
from proxy.services.database_service import HeavyDatabaseService
from proxy.services.document_service import RealDocumentService
from proxy.services.real_subject import RealSubject
from proxy.services.remote_service import RealRemoteServer
from proxy.services.resource_service import SharedResourceService
from proxy.services.youtube_service import ThirdPartyYouTubeClass

# ==============================================================================
# CONFIGURAÇÃO DE PÁGINA E ESTILO VISUAL
# ==============================================================================

st.set_page_config(
    page_title="Laboratório do Padrão Proxy | ES II FAFIC",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .main-header {
        background: linear-gradient(135deg, #1E2B5B 0%, #0F172A 100%);
        padding: 24px;
        border-radius: 12px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .main-header h1 {
        color: #FFFFFF;
        margin: 0;
        font-size: 2.2rem;
        font-weight: 700;
    }
    .main-header p {
        color: #94A3B8;
        margin: 6px 0 0 0;
        font-size: 1.05rem;
    }
    .badge-authors {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.85rem;
        display: inline-block;
        margin-top: 12px;
        color: #E2E8F0;
    }
    .concept-card {
        background-color: #F8FAFC;
        border-left: 5px solid #1E2B5B;
        padding: 16px 20px;
        border-radius: 0 8px 8px 0;
        margin-bottom: 16px;
        color: #1E293B;
    }
    .metric-box {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 14px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==============================================================================
# INICIALIZAÇÃO DE ESTADO GLOBAL (SESSION STATE)
# ==============================================================================

if "virtual_proxy" not in st.session_state:
    st.session_state.virtual_proxy = VirtualDatabaseProxy()

if "protection_proxy" not in st.session_state:
    st.session_state.protection_proxy = ProtectionAdminProxy()

if "remote_proxy" not in st.session_state:
    st.session_state.remote_server = RealRemoteServer()
    st.session_state.remote_proxy = RemoteServiceProxy(st.session_state.remote_server)

if "logging_proxy" not in st.session_state:
    st.session_state.logging_proxy = LoggingDocumentProxy()

if "cached_youtube" not in st.session_state:
    st.session_state.real_youtube = ThirdPartyYouTubeClass()
    st.session_state.cached_youtube = CachedYouTubeClass(st.session_state.real_youtube)
    st.session_state.youtube_manager = YouTubeManager(st.session_state.cached_youtube)

if "smart_proxy" not in st.session_state:
    st.session_state.shared_resource = SharedResourceService("Pool-Memoria-Compartilhada-X1")
    st.session_state.smart_proxy = SmartReferenceProxy(st.session_state.shared_resource)

# ==============================================================================
# CABEÇALHO ACADÊMICO
# ==============================================================================

st.markdown(
    """
    <div class="main-header">
        <h1>🛡️ Laboratório do Padrão de Projeto Proxy</h1>
        <p>Demonstração Prática e Visual dos Conceitos de Engenharia de Software II — FAFIC (Cajazeiras-PB, 2026)</p>
        <div class="badge-authors">
            👥 <strong>Grupo:</strong> João Pedro Cruz • Pedro Henrique • Pedro Arlyx • Fabricio Nathan • Lucas Gonçalves
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ==============================================================================
# BARRA LATERAL COM NAVEGAÇÃO E SUMÁRIO ACADÊMICO
# ==============================================================================

with st.sidebar:
    st.image(
        "https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/shield-check.svg",
        width=50,
    )
    st.title("Navegação do Laboratório")
    st.markdown("Selecione o módulo para demonstração:")

    modulo_selecionado = st.radio(
        "Módulos Acadêmicos:",
        [
            "📖 Visão Geral & Teoria",
            "🧩 1. Estrutura Básica",
            "⏳ 2. Proxy Virtual (Lazy Loading)",
            "🛡️ 3. Proxy de Proteção",
            "🌐 4. Proxy Remoto",
            "📝 5. Proxy de Log (Auditoria)",
            "📺 6. Proxy de Cache (YouTube Lib)",
            "🧠 7. Referência Inteligente",
            "⚖️ 8. Comparação com Outros Padrões",
        ],
        index=0,
    )

    st.divider()
    st.markdown("### 📚 Ficha Técnica")
    st.markdown("**Padrão:** Estrutural (GoF)")
    st.markdown("**Referência:** Refactoring Guru")
    st.markdown("**Ambiente:** Python 3.14 + Streamlit")
    st.markdown("**Disciplina:** Engenharia de Software II")


# ==============================================================================
# MÓDULO 0 — VISÃO GERAL & TEORIA ACADÊMICA
# ==============================================================================

if modulo_selecionado == "📖 Visão Geral & Teoria":
    st.subheader("📖 Visão Geral do Padrão de Projeto Proxy")

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown(
            """
            <div class="concept-card">
                <h4>1. Introdução</h4>
                O <strong>Proxy</strong> é um padrão de projeto estrutural cuja ideia central é colocar um objeto intermediário
                — o <em>proxy</em> — no lugar de outro objeto, chamado de <em>serviço real</em>. Esse intermediário expõe
                <strong>exatamente a mesma interface</strong> do objeto original, de modo que o cliente não percebe a troca.
            </div>
            <div class="concept-card">
                <h4>2. O Problema</h4>
                Considere um objeto pesado que consome muitos recursos (como uma conexão com banco de dados ou um arquivo gigante),
                mas que só é necessário de vez em quando. Criá-lo logo na inicialização desperdiça memória e atrasa o sistema.
                Além disso, se a classe pertencer a uma biblioteca de terceiros, <strong>não podemos alterar seu código</strong>
                para adicionar verificações ou cache.
            </div>
            <div class="concept-card">
                <h4>3. A Solução</h4>
                Criar uma classe Proxy que implementa a mesma interface do serviço e mantém uma referência interna para ele.
                O cliente recebe o Proxy no lugar do serviço real. Quando uma chamada chega, o Proxy executa tarefas
                como controle de permissões, cache ou inicialização sob demanda, delegando a operação ao serviço real.
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.info("💳 **Analogia do Mundo Real (Apresentada no Artigo)**")
        st.markdown(
            """
            * **O Dinheiro Físico:** É o recurso real no cofre do banco central.
            * **A Conta Bancária:** É o serviço que gerencia o saldo.
            * **O Cartão de Crédito (Proxy):** É o substituto intermediário do dinheiro.
            
            Tanto o dinheiro vivo quanto o cartão atendem à mesma necessidade — pagar uma compra —,
            mas o cartão evita carregar notas pesadas e protege o lojista e o cliente contra riscos!
            """
        )

        st.success("✅ **Vantagens Principais (Seção 7)**")
        st.markdown(
            """
            1. **Transparência:** O cliente não sabe que está usando um intermediário.
            2. **Gerenciamento de Ciclo de Vida:** Cria o objeto pesado apenas quando estritamente necessário.
            3. **Princípio Aberto/Fechado (OCP):** Permite adicionar novos proxies sem modificar o serviço ou o cliente.
            4. **Resiliência:** Funciona mesmo se o serviço real estiver temporariamente indisponível.
            """
        )

        st.warning("⚠️ **Desvantagens a Ponderar**")
        st.markdown(
            """
            * Aumenta a quantidade de classes na arquitetura.
            * Pode introduzir uma pequena latência adicional devido à camada de indireção.
            """
        )


# ==============================================================================
# MÓDULO 1 — ESTRUTURA BÁSICA
# ==============================================================================

elif modulo_selecionado == "🧩 1. Estrutura Básica":
    st.subheader("🧩 Módulo 1 — Estrutura Básica do Padrão Proxy")
    st.markdown(
        """
        Este módulo demonstra os **quatro participantes clássicos** do padrão:
        1. **`Subject` (Interface do Serviço):** Define o contrato abstrato comum (`request()`).
        2. **`RealSubject` (Serviço Real):** Contém a lógica de negócio verdadeira.
        3. **`Proxy`:** Mantém a referência ao `RealSubject`, intercepta a requisição e delega a operação.
        4. **`Client`:** Consome o serviço dependendo estritamente da interface `Subject`.
        """
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 1. Chamada Direta ao Serviço Real (`RealSubject`)")
        st.caption("O cliente recebe diretamente a instância de `RealSubject`.")
        if st.button("Executar via Serviço Real", key="btn_real_subject"):
            real_subject = RealSubject()
            client_real = ClientApp(real_subject)
            with st.spinner("Processando..."):
                resp = client_real.run_business_operation()
            st.success(f"**Retorno:** {resp}")
            st.code(
                f"""# Código do Cliente:
client = ClientApp(real_subject)
resultado = client.run_business_operation()
# {resp}""",
                language="python",
            )

    with col2:
        st.markdown("### 2. Chamada Intermediada pelo `Proxy`")
        st.caption("O cliente recebe o `BasicProxy`. O código do cliente permanece 100% idêntico!")
        if st.button("Executar via Proxy Intermediário", key="btn_basic_proxy"):
            real_subject = RealSubject()
            proxy = BasicProxy(real_subject)
            client_proxy = ClientApp(proxy)
            with st.spinner("Interceptando e delegando..."):
                resp = client_proxy.run_business_operation()
            st.info(f"**Retorno:** {resp}")
            st.code(
                f"""# Código do Cliente (Inalterado):
client = ClientApp(basic_proxy)
resultado = client.run_business_operation()
# {resp}""",
                language="python",
            )
            st.markdown("**Logs de Interceptação do Proxy:**")
            st.write(proxy.pre_processing_logs)
            st.write(proxy.post_processing_logs)


# ==============================================================================
# MÓDULO 2 — PROXY VIRTUAL (LAZY INITIALIZATION)
# ==============================================================================

elif modulo_selecionado == "⏳ 2. Proxy Virtual (Lazy Loading)":
    st.subheader("⏳ Módulo 2 — Proxy Virtual (Lazy Initialization / Inicialização Preguiçosa)")
    st.markdown(
        """
        **Cenário Real do Artigo:** Conexão com banco de dados pesada (`HeavyDatabaseService`)
        que consome memória, buffers e tempo de handshake TLS.
        
        O **`VirtualDatabaseProxy`** é instanciado em **0 milissegundos**, adiando a conexão real
        até a primeira execução de `query()`, e **reutiliza a mesma instância** nas chamadas seguintes.
        """
    )

    v_proxy: VirtualDatabaseProxy = st.session_state.virtual_proxy
    status = v_proxy.get_status()

    # Métricas visuais
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Instanciado no Banco?", "Sim (Conectado)" if status.get("is_instantiated") else "Não (Leve)")
    with m2:
        st.metric("Total de Chamadas Recebidas", v_proxy.total_calls)
    with m3:
        st.metric(
            "Tempo de Conexão Inicial",
            f"{status.get('initialization_duration_ms', 0)} ms" if status.get("is_instantiated") else "0.0 ms (Adiado)",
        )

    st.divider()

    c1, c2, c3 = st.columns([1, 1, 1])

    with c1:
        if st.button("1. Criar / Resetar Proxy Virtual", use_container_width=True):
            st.session_state.virtual_proxy = VirtualDatabaseProxy()
            st.rerun()

    with c2:
        if st.button("2. Executar 1ª Consulta (Dispara Conexão)", use_container_width=True):
            start = time.perf_counter()
            with st.spinner("Primeira consulta detectada: Estabelecendo conexão pesada sob demanda..."):
                records = v_proxy.query("SELECT * FROM alunos")
            elapsed = round((time.perf_counter() - start) * 1000, 2)
            st.success(f"Consulta executada com sucesso! Tempo total: {elapsed} ms.")
            st.rerun()

    with c3:
        if st.button("3. Executar Consulta Subsequente (Reúso)", use_container_width=True):
            if not v_proxy.is_service_instantiated:
                st.warning("Aviso: O serviço ainda não foi instanciado. Esta chamada será a primeira!")
            start = time.perf_counter()
            records = v_proxy.query("SELECT * FROM turmas")
            elapsed = round((time.perf_counter() - start) * 1000, 2)
            st.info(f"Consulta executada reutilizando a conexão ativa! Tempo total: {elapsed} ms.")
            st.rerun()

    st.markdown("### 📋 Linha do Tempo e Ciclo de Vida do Proxy Virtual")
    for event in v_proxy.lifecycle_events:
        st.code(event, language="text")


# ==============================================================================
# MÓDULO 3 — PROXY DE PROTEÇÃO
# ==============================================================================

elif modulo_selecionado == "🛡️ 3. Proxy de Proteção":
    st.subheader("🛡️ Módulo 3 — Proxy de Proteção (Controle de Acesso / RBAC)")
    st.markdown(
        """
        **Cenário do Artigo:** Operações administrativas críticas no sistema (`RealAdminService`).
        
        O **`ProtectionAdminProxy`** verifica ativamente o papel do usuário (*Role-Based Access Control*)
        antes de repassar a chamada ao serviço real. Usuários não autorizados são bloqueados com `PermissionError`.
        """
    )

    prot_proxy: ProtectionAdminProxy = st.session_state.protection_proxy

    col_user, col_role = st.columns(2)
    with col_user:
        usuario_atual = st.text_input("Identificador do Usuário:", value="joao.pedro@fafic.edu.br")
    with col_role:
        papel_selecionado = st.selectbox(
            "Perfil / Papel de Acesso:",
            options=[UserRole.ADMIN, UserRole.OPERADOR, UserRole.CONVIDADO],
            format_func=lambda x: f"🔑 {x.value} " + ("(Acesso Total)" if x == UserRole.ADMIN else "(Parcial)" if x == UserRole.OPERADOR else "(Somente Leitura)"),
        )

    st.markdown("#### Selecione uma Operação Administrativa para Testar:")
    op1, op2, op3 = st.columns(3)

    with op1:
        st.markdown("**Alterar Parâmetro do Sistema**")
        st.caption("Permitido para: `ADMIN` e `OPERADOR`")
        if st.button("Executar Alteração", key="btn_cfg"):
            try:
                res = prot_proxy.alterar_configuracao("NIVEL_LOG", "DEBUG", usuario_atual, papel_selecionado)
                st.success(f"✅ Operação Autorizada!\n\n`{res['chave']}` alterado para `{res['novo_valor']}`.")
            except PermissionError as err:
                st.error(f"❌ {err}")

    with op2:
        st.markdown("**Excluir Usuário do Banco**")
        st.caption("Restrito exclusivamente a: `ADMIN`")
        if st.button("Excluir Usuário #104", key="btn_del"):
            try:
                res = prot_proxy.excluir_usuario(104, usuario_atual, papel_selecionado)
                st.success(f"✅ Usuário excluído com sucesso: `{res['email_removido']}`.")
            except (PermissionError, ValueError) as err:
                st.error(f"❌ {err}")

    with op3:
        st.markdown("**Reiniciar Nó do Servidor**")
        st.caption("Restrito exclusivamente a: `ADMIN`")
        if st.button("Reboot do Servidor", key="btn_boot"):
            try:
                res = prot_proxy.reiniciar_servidor("Rotina de Manutenção", usuario_atual, papel_selecionado)
                st.success(f"✅ Reinicialização agendada com sucesso!")
            except PermissionError as err:
                st.error(f"❌ {err}")

    st.divider()
    st.markdown("### 📋 Histórico de Auditoria do Proxy de Proteção")
    if prot_proxy.security_logs:
        st.dataframe(prot_proxy.security_logs, use_container_width=True)
    else:
        st.caption("Nenhuma operação registrada ainda nesta sessão.")


# ==============================================================================
# MÓDULO 4 — PROXY REMOTO
# ==============================================================================

elif modulo_selecionado == "🌐 4. Proxy Remoto":
    st.subheader("🌐 Módulo 4 — Proxy Remoto (Comunicação Transparente com Servidor Remoto)")
    st.markdown(
        """
        **Cenário do Artigo:** O serviço real está fisicamente hospedado em outro servidor (`RealRemoteServer`).
        
        O **`RemoteServiceProxy`** funciona como um *Stub Local*. O cliente chama métodos Python normais
        como se o serviço estivesse na mesma memória. O Proxy cuida de empacotar a mensagem em JSON (marshalling),
        transmitir pela rede simulada com latência, aguardar e desempacotar a resposta (unmarshalling).
        """
    )

    remote_proxy: RemoteServiceProxy = st.session_state.remote_proxy
    server = st.session_state.remote_server

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"**Servidor Remoto Alvo:** `{server.hostname}` (`{server.ip_address}`)")
        st.caption("Total de pacotes binários recebidos pelo servidor: " + str(server.total_packets_received))

        if st.button("1. Consultar Telemetria do Servidor Remoto", key="btn_rem_rep"):
            with st.spinner("Transmitindo pacote RPC pelo socket remoto..."):
                report = remote_proxy.obter_relatorio_servidor("SRV-NODE-PB01")
            st.success(f"Dados remotos recebidos com sucesso!")
            st.json(report)

    with c2:
        st.markdown("**Executar Cálculo Numérico Distribuído**")
        operacao = st.selectbox("Operação Matemática Remota:", ["media", "soma", "variancia"])
        if st.button("2. Enviar Dataset para Processamento em Nuvem", key="btn_rem_calc"):
            dataset_teste = [12.5, 45.2, 98.7, 33.1, 78.4, 99.0]
            with st.spinner("Empacotando dataset e transmitindo ao nó remoto..."):
                calc_res = remote_proxy.executar_calculo_distribuido(dataset_teste, operacao)
            st.info(f"Resultado computado remotamente: **{calc_res.get('resultado')}**")
            st.json(calc_res)

    st.markdown("### 📡 Logs de Transmissão de Pacotes de Rede (RPC Telemetry)")
    if remote_proxy.network_transmission_logs:
        st.dataframe(remote_proxy.network_transmission_logs, use_container_width=True)


# ==============================================================================
# MÓDULO 5 — PROXY DE LOG
# ==============================================================================

elif modulo_selecionado == "📝 5. Proxy de Log (Auditoria)":
    st.subheader("📝 Módulo 5 — Proxy de Log (Registro e Auditoria)")
    st.markdown(
        """
        **Cenário do Artigo:** Sistema de emissão de declarações e certificados acadêmicos (`RealDocumentService`).
        
        O **`LoggingDocumentProxy`** intercepta cada chamada ao serviço real e registra:
        * Nome da operação executada
        * Data e horário exatos
        * Parâmetros recebidos (com ofuscação de segredos)
        * Resultado gerado ou exceção capturada
        * Duração da chamada em milissegundos
        """
    )

    log_proxy: LoggingDocumentProxy = st.session_state.logging_proxy

    col_input1, col_input2, col_input3 = st.columns(3)
    with col_input1:
        mat_in = st.text_input("Matrícula:", value="2024.2060063")
    with col_input2:
        curso_in = st.selectbox("Curso:", ["Sistemas de Informação", "Engenharia de Software", "Direito"])
    with col_input3:
        tipo_in = st.selectbox("Tipo de Declaração:", ["Vínculo Acadêmico", "Conclusão de Curso", "Quitação"])

    col_act1, col_act2 = st.columns(2)
    with col_act1:
        if st.button("Emitir Declaração Institucional", use_container_width=True):
            try:
                doc = log_proxy.emitir_declaracao(mat_in, curso_in, tipo_in)
                st.success(f"Declaração `{doc['documento_id']}` emitida com autenticidade `{doc['codigo_autenticidade']}`!")
            except Exception as e:
                st.error(f"Erro capturado e registrado pelo Proxy: {e}")

    with col_act2:
        if st.button("Simular Erro (Matrícula Inválida)", use_container_width=True):
            try:
                log_proxy.emitir_declaracao("INVALIDA", curso_in, tipo_in)
            except Exception as e:
                st.warning(f"Erro intencional capturado com sucesso pelo Proxy: {e}")

    st.divider()
    st.markdown("### 📋 Livro de Registro de Auditoria do Proxy")
    if log_proxy.call_history:
        st.dataframe(log_proxy.call_history, use_container_width=True)
    else:
        st.caption("Nenhuma operação registrada ainda.")


# ==============================================================================
# MÓDULO 6 — PROXY DE CACHE (BIBLIOTECA DO YOUTUBE)
# ==============================================================================

elif modulo_selecionado == "📺 6. Proxy de Cache (YouTube Lib)":
    st.subheader("📺 Módulo 6 — Proxy de Cache (Exemplo da Biblioteca do YouTube)")
    st.markdown(
        """
        **Exemplo Central do Trabalho Acadêmico (Seção 4):**
        * **Interface:** `ThirdPartyYouTubeLib`
        * **Serviço Real (Biblioteca de Terceiros):** `ThirdPartyYouTubeClass` (simula requisições lentas de rede)
        * **Proxy de Cache:** `CachedYouTubeClass` (armazena resultados e evita chamadas redundantes)
        * **Cliente:** `YouTubeManager` (consome apenas a interface, operando com ou sem cache)
        """
    )

    cached_yt: CachedYouTubeClass = st.session_state.cached_youtube
    real_yt: ThirdPartyYouTubeClass = st.session_state.real_youtube
    yt_manager: YouTubeManager = st.session_state.youtube_manager

    # Métricas de economia
    metrics = cached_yt.get_metrics()
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total de Requisições do Cliente", metrics["total_requests"])
    with c2:
        st.metric("Cache Hits (Na Memória)", metrics["cache_hits"])
    with c3:
        st.metric("Chamadas Reais à Rede (YouTube)", real_yt.network_call_count)
    with c4:
        st.metric("Tempo Economizado", f"{metrics['saved_latency_seconds']} s", delta=f"{metrics['hit_ratio_pct']}% economia")

    st.divider()

    st.markdown("#### Ações do Cliente (`YouTubeManager`):")
    a1, a2, a3, a4 = st.columns([1, 1, 1, 1])

    with a1:
        if st.button("1. Listar Vídeos Populares", use_container_width=True):
            start = time.perf_counter()
            with st.spinner("Buscando lista de vídeos..."):
                videos = yt_manager.render_list_panel()
            dur = round((time.perf_counter() - start) * 1000, 1)
            st.success(f"{len(videos)} vídeos listados em {dur} ms.")
            st.rerun()

    with a2:
        if st.button("2. Detalhes do Vídeo #v101", use_container_width=True):
            start = time.perf_counter()
            with st.spinner("Consultando metadados do vídeo..."):
                info = yt_manager.render_video_page("v101")
            dur = round((time.perf_counter() - start) * 1000, 1)
            st.info(f"Vídeo '{info['title']}' obtido em {dur} ms.")
            st.rerun()

    with a3:
        if st.button("3. Baixar Vídeo #v102", use_container_width=True):
            start = time.perf_counter()
            with st.spinner("Solicitando stream de download..."):
                down = yt_manager.trigger_download("v102")
            dur = round((time.perf_counter() - start) * 1000, 1)
            origem = down.get("source", "REDE")
            st.success(f"Download ({down['downloaded_mb']} MB) concluído em {dur} ms! [Origem: {origem}]")
            st.rerun()

    with a4:
        if st.button("🔄 Resetar Cache em Memória", use_container_width=True):
            cached_yt.reset_cache()
            st.warning("Cache esvaziado! A próxima chamada consultará a rede novamente.")
            st.rerun()

    st.markdown("### 💡 Demonstração Didática: O que acabou de acontecer?")
    st.info(
        f"""
        1. O cliente **`YouTubeManager`** não foi modificado em nada: ele apenas chama `list_videos()`, `get_video_info()` e `download_video()`.
        2. Na **1ª vez** que você clica em um botão, ocorre um **Cache Miss**: o Proxy repassa a chamada à biblioteca real de terceiros (levando ~400ms a ~700ms de latência simulada).
        3. Na **2ª vez** em diante, ocorre um **Cache Hit**: o Proxy entrega os dados instantaneamente da memória (**0 ms** de chamada de rede).
        4. O sistema economizou até agora **{metrics['saved_latency_seconds']} segundos** de transferência e processamento!
        """
    )


# ==============================================================================
# MÓDULO 7 — REFERÊNCIA INTELIGENTE (SMART REFERENCE)
# ==============================================================================

elif modulo_selecionado == "🧠 7. Referência Inteligente":
    st.subheader("🧠 Módulo 7 — Referência Inteligente (Smart Reference Proxy)")
    st.markdown(
        """
        **Cenário do Artigo (Seção 5):** Controle de ciclo de vida de um recurso compartilhado caro (`SharedResourceService`).
        
        O **`SmartReferenceProxy`** acompanha a quantidade de clientes que estão referenciando ativamente
        o recurso. Quando o último cliente libera sua referência (`reference_count == 0`), o Proxy
        **desaloca automaticamente o recurso da memória**.
        """
    )

    smart_proxy: SmartReferenceProxy = st.session_state.smart_proxy
    status_smart = smart_proxy.get_lifecycle_status()

    r1, r2, r3 = st.columns(3)
    with r1:
        st.metric("Clientes Ativos Usando o Recurso", status_smart["reference_count"])
    with r2:
        st.metric(
            "Estado da Memória",
            "Alocado e Ativo" if status_smart["is_allocated"] else "Desalocado da Memória",
            delta="Pronto para uso" if status_smart["is_allocated"] else "Recurso liberado",
        )
    with r3:
        st.metric("Desalocação Automática Disparada?", "Sim (Auto-Released)" if status_smart["auto_released"] else "Não")

    st.divider()

    st.markdown("#### Simulação de Clientes Conectando e Desconectando:")
    c_btn1, c_btn2, c_btn3, c_btn4 = st.columns(4)

    with c_btn1:
        if st.button("➕ Conectar Cliente A (Matrículas)", use_container_width=True):
            smart_proxy.acquire_reference("ModuloMatricula")
            st.rerun()

    with c_btn2:
        if st.button("➕ Conectar Cliente B (Financeiro)", use_container_width=True):
            smart_proxy.acquire_reference("ModuloFinanceiro")
            st.rerun()

    with c_btn3:
        if st.button("➖ Liberar Cliente A", use_container_width=True):
            smart_proxy.release_reference("ModuloMatricula")
            st.rerun()

    with c_btn4:
        if st.button("➖ Liberar Cliente B", use_container_width=True):
            smart_proxy.release_reference("ModuloFinanceiro")
            st.rerun()

    if st.button("🔄 Reiniciar Simulação de Recurso Compartilhado"):
        st.session_state.shared_resource = SharedResourceService("Pool-Memoria-Compartilhada-X1")
        st.session_state.smart_proxy = SmartReferenceProxy(st.session_state.shared_resource)
        st.rerun()

    st.markdown("### 📋 Log de Acompanhamento do Ciclo de Vida (Smart Reference)")
    for entry in smart_proxy.usage_log[-8:]:
        st.code(entry, language="text")


# ==============================================================================
# MÓDULO 8 — COMPARAÇÃO COM OUTROS PADRÕES
# ==============================================================================

elif modulo_selecionado == "⚖️ 8. Comparação com Outros Padrões":
    st.subheader("⚖️ Módulo 8 — Comparação Arquitetural com Outros Padrões (Seção 8)")
    st.markdown(
        """
        O padrão **Proxy** é frequentemente confundido com padrões vizinhos do GoF.
        Esta seção demonstra as diferenças conceituais e estruturais rigorosas descritas no artigo:
        """
    )

    t1, t2, t3, t4 = st.tabs(["🛡️ Proxy", "🔌 Adapter", "🎀 Decorator", "🏛️ Facade"])

    with t1:
        st.markdown("### 🛡️ Padrão Proxy")
        st.markdown(
            """
            * **Interface:** Mantém **exatamente a mesma interface** do serviço real.
            * **Propósito:** Controla o acesso, gerencia o ciclo de vida (lazy init), faz cache ou validações de segurança.
            * **Ciclo de Vida:** Geralmente o próprio Proxy gerencia a criação e destruição do serviço real.
            """
        )
        proxy_demo = NotificationProxy()
        st.code(
            """# Proxy: Mesma interface 'send(recipient, message)'
proxy = NotificationProxy()
res1 = proxy.send('aluno@fafic.br', 'Aviso de Prova')     # Repassa ao serviço real
res2 = proxy.send('spammer@hack.org', 'Spam detectado')   # Bloqueia antes de repassar""",
            language="python",
        )
        if st.button("Testar Proxy Demo", key="btn_cmp_proxy"):
            st.write(proxy_demo.send("aluno@fafic.br", "Aviso de Prova"))
            st.write(proxy_demo.send("spammer@hack.org", "Spam detectado"))

    with t2:
        st.markdown("### 🔌 Padrão Adapter")
        st.markdown(
            """
            * **Interface:** Oferece uma **interface diferente ou adaptada** para viabilizar compatibilidade entre classes incompatíveis.
            * **Propósito:** Faz objetos com contratos incompatíveis trabalharem juntos (ex: adaptar API legada para a nova interface).
            * **Intercambiabilidade:** Não é intercambiável com a classe original sem adaptação.
            """
        )
        legacy_sms = LegacySmsVendor()
        adapter_demo = SmsAdapter(legacy_sms)
        st.code(
            """# Adapter: Converte 'send(recipient, message)' para 'disparar_torpedo_celular(ddd, num, msg)'
legacy_vendor = LegacySmsVendor()
adapter = SmsAdapter(legacy_vendor)
resultado = adapter.send('83999998888', 'Código de confirmação FAFIC')""",
            language="python",
        )
        if st.button("Testar Adapter Demo", key="btn_cmp_adapter"):
            st.write(adapter_demo.send("83999998888", "Código de confirmação FAFIC"))

    with t3:
        st.markdown("### 🎀 Padrão Decorator")
        st.markdown(
            """
            * **Interface:** Mantém a mesma interface base, mas adiciona **novas responsabilidades em camadas**.
            * **Propósito:** Adiciona comportamentos em tempo de execução através de composição em cascata.
            * **Ciclo de Vida:** A composição dos decoradores fica a cargo do **cliente**, enquanto no Proxy é ele quem gerencia o serviço.
            """
        )
        base_service = RealNotificationService()
        decorator_demo = TimestampEncryptionDecorator(base_service)
        st.code(
            """# Decorator: Envolve o serviço adicionando criptografia e assinatura digital em cascata
base = RealNotificationService()
decorator = TimestampEncryptionDecorator(base)
resultado = decorator.send('aluno@fafic.br', 'Documento confidencial')""",
            language="python",
        )
        if st.button("Testar Decorator Demo", key="btn_cmp_decorator"):
            st.write(decorator_demo.send("aluno@fafic.br", "Documento confidencial"))

    with t4:
        st.markdown("### 🏛️ Padrão Facade")
        st.markdown(
            """
            * **Interface:** Cria uma **nova interface simplificada** para esconder um subsistema complexo.
            * **Propósito:** Reduz a complexidade de múltiplos módulos interdependentes em uma única porta de entrada fácil.
            * **Intercambiabilidade:** Não possui a mesma interface dos subsistemas que encapsula.
            """
        )
        facade_demo = NotificationFacade()
        st.code(
            """# Facade: Esconde SMTP, TemplateEngine e DeliveryAuditor em um único método simples
facade = NotificationFacade()
resultado = facade.enviar_comunicado_oficial('Pedro Henrique', '2024.101', 'Bolsa Deferida')""",
            language="python",
        )
        if st.button("Testar Facade Demo", key="btn_cmp_facade"):
            steps = facade_demo.enviar_comunicado_oficial("Pedro Henrique", "2024.101", "Bolsa Deferida")
            for s in steps:
                st.write(f"• {s}")

    st.divider()
    st.markdown("### 📊 Tabela Comparativa Resumida")
    st.table(
        [
            {"Padrão": "🛡️ Proxy", "Interface com o Cliente": "Rigidamente a mesma", "Controle de Ciclo de Vida?": "Sim, pelo Proxy", "Objetivo Central": "Controlar acesso e adicionar serviços transversais"},
            {"Padrão": "🔌 Adapter", "Interface com o Cliente": "Diferente / Convertida", "Controle de Ciclo de Vida?": "Não", "Objetivo Central": "Resolver incompatibilidade de interfaces"},
            {"Padrão": "🎀 Decorator", "Interface com o Cliente": "Mesma interface base", "Controle de Ciclo de Vida?": "Pelo Cliente (Composição)", "Objetivo Central": "Adicionar responsabilidades dinâmicas em camadas"},
            {"Padrão": "🏛️ Facade", "Interface com o Cliente": "Nova interface simplificada", "Controle de Ciclo de Vida?": "Parcial", "Objetivo Central": "Esconder a complexidade de múltiplos subsistemas"},
        ]
    )

# ==============================================================================
# RODAPÉ INSTITUCIONAL
# ==============================================================================

st.divider()
st.markdown(
    """
    <div style="text-align: center; color: #64748B; font-size: 0.85rem; padding: 12px 0;">
        Faculdade Católica da Paraíba (FAFIC) • Engenharia de Software II • Cajazeiras-PB, 2026<br>
        Projeto Acadêmico: Demonstração e Laboratório do Padrão de Projeto Estrutural Proxy
    </div>
    """,
    unsafe_allow_html=True,
)
