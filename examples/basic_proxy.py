"""Exemplo executável da Estrutura Básica do Padrão Proxy (Módulo 1).

Demonstra no terminal como o cliente interage com RealSubject e BasicProxy
através do mesmo contrato abstrato Subject.

Como executar:
    python3 proxy/examples/basic_proxy.py
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
PARENT_DIR = os.path.dirname(BASE_DIR)
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

from proxy.clients.client import ClientApp
from proxy.proxies.basic_proxy import BasicProxy
from proxy.services.real_subject import RealSubject


def main() -> None:
    print("=" * 70)
    print("DEMONSTRAÇÃO DE CONSOLE: ESTRUTURA BÁSICA DO PADRÃO PROXY")
    print("=" * 70)

    # 1. Cliente executando diretamente com o Serviço Real
    print("\n1. Cliente recebendo RealSubject diretamente:")
    real_subject = RealSubject()
    client_real = ClientApp(real_subject)
    res_real = client_real.run_business_operation()
    print(f"   -> Retorno: {res_real}")

    # 2. Cliente executando com o Proxy
    print("\n2. Cliente recebendo BasicProxy (mesma interface):")
    proxy = BasicProxy(real_subject)
    client_proxy = ClientApp(proxy)
    res_proxy = client_proxy.run_business_operation()
    print(f"   -> Retorno: {res_proxy}")

    print("\nLogs internos de pré/pós-processamento do Proxy:")
    for log in proxy.pre_processing_logs + proxy.post_processing_logs:
        print(f"   * {log}")

    print("\nConclusão: O cliente operou de maneira idêntica em ambos os casos.")
    print("=" * 70)


if __name__ == "__main__":
    main()
