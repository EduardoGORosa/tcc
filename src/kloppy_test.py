from pathlib import Path
from kloppy import sportec

# Caminhos definidos na arquitetura do projeto
BASE_DIR = Path("data")
RAW_DIR = BASE_DIR / "raw"
EVENTS_FILE = RAW_DIR / "sportec_events.xml"
META_FILE = RAW_DIR / "sportec_metadata.xml"


def main():
    print(f"--- Carregando Sportec (Arquitetura Local) ---")

    # 1. Validação de Dependência (Fail Fast)
    if not EVENTS_FILE.exists() or not META_FILE.exists():
        print(f"ERRO: Arquivos XML não encontrados em {RAW_DIR}")
        print(
            "Por favor, faça o download manual dos links e salve com os nomes corretos."
        )
        return

    # 2. Carregamento (Provider Agnostic)
    # O sportec.load_event_data espera arquivos locais, não URLs.
    dataset = sportec.load_event_data(
        event_data=EVENTS_FILE,
        meta_data=META_FILE,
        coordinates="metric",  # Padroniza para Metros (Engenharia de Dados)
        pitch_length=105,
        pitch_width=68,
    )

    # 3. Inspeção dos Objetos de Domínio
    print(f"\n✅ Dataset Carregado na Memória!")
    print(f"Provider: {dataset.metadata.provider}")
    print(f"Orientação do Campo: {dataset.metadata.orientation}")
    print(f"Total de Eventos: {len(dataset.events)}")

    # Vamos ver a estrutura de um evento para modelar suas classes depois
    first_event = dataset.events[0]
    print(f"\nExemplo de Evento (Objeto Kloppy):")
    print(f" - Tipo: {first_event.event_name}")
    print(f" - Jogador: {first_event.player}")
    print(f" - Posição: {first_event.coordinates}")
    print(f" - Timestamp: {first_event.timestamp}")


if __name__ == "__main__":
    main()
