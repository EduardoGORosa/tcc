import os
import git
import pandas as pd
from statsbombpy import sb
from tqdm import tqdm
import warnings
from pathlib import Path

# Configurações Globais
DATA_DIR = Path("data")
RAW_DIR = DATA_DIR / "raw"
EXTERNAL_DIR = DATA_DIR / "external"

# Cria diretórios se não existirem
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(EXTERNAL_DIR, exist_ok=True)

warnings.simplefilter(action="ignore", category=FutureWarning)


def download_statsbomb_360():
    """
    Baixa o catálogo da Euro 2020 e Copa 2022 (As minas de ouro do 360).
    """
    print("\n--- 1. STATSBOMB 360 (Tática de Elite) ---")
    comps = sb.competitions()

    # Filtra apenas competições que tem match_available_360
    comps_360 = comps[comps["match_available_360"].notna()]

    # Foca nas principais para o TCC (Euro e Copa)
    targets = comps_360[
        comps_360["competition_name"].isin(["UEFA Euro", "FIFA World Cup"])
    ]

    print(f"Competições encontradas: {len(targets)}")
    print(targets[["competition_name", "season_name"]].to_string(index=False))

    # Salva o catálogo para referência
    targets.to_csv(RAW_DIR / "statsbomb_360_catalog.csv", index=False)
    print(f"Catálogo salvo em {RAW_DIR}")


def download_metrica_sports():
    """
    Clona o repositório oficial da Metrica Sports.
    Referência: Pettersen et al. (2014) em papers de validação.
    """
    print("\n--- 2. METRICA SPORTS (Física / Tracking Contínuo) ---")
    repo_url = "https://github.com/metrica-sports/sample-data.git"
    target_path = EXTERNAL_DIR / "metrica_sports"

    if target_path.exists():
        print(f"Metrica Data já existe em: {target_path}")
    else:
        print(f"Clonando repositório Metrica para {target_path}...")
        try:
            git.Repo.clone_from(repo_url, target_path)
            print("Download concluído com sucesso.")
        except Exception as e:
            print(f"Erro ao clonar Metrica: {e}")


def download_skillcorner_opendata():
    """
    Clona o SkillCorner Open Data (9 partidas da Liga Australiana).
    Útil pois é tracking de 'Broadcast', mais sujo e real que o da Metrica.
    """
    print("\n--- 3. SKILLCORNER (Tracking Real de Broadcast) ---")
    repo_url = "https://github.com/SkillCorner/opendata.git"
    target_path = EXTERNAL_DIR / "skillcorner"

    if target_path.exists():
        print(f"SkillCorner Data já existe em: {target_path}")
    else:
        print(f"Clonando repositório SkillCorner para {target_path}...")
        try:
            git.Repo.clone_from(repo_url, target_path)
            print("Download concluído com sucesso.")
        except Exception as e:
            print(f"Erro ao clonar SkillCorner: {e}")


def info_soccernet():
    """
    Apenas imprime instruções sobre o SoccerNet, pois o download é massivo (Terabytes).
    """
    print("\n--- 4. SOCCERNET (Opcional - Hardcore) ---")
    print("O SoccerNet é o padrão acadêmico atual (CVPR/ICCV).")
    print("Para baixar o tracking deles (Challenge 2022), use no terminal:")
    print("  pip install SoccerNet")
    print(
        '  python -c \'from SoccerNet.Downloader import SoccerNetDownloader; myDL = SoccerNetDownloader(LocalDirectory="data/external/soccernet"); myDL.downloadDataTask(task="tracking", split=["train", "test", "challenge"])\''
    )
    print("Aviso: Isso pode baixar mais de 100GB de dados.")


def main():
    print("=== GHOST SCOUT DATA DOWNLOADER ===")
    print(f"Salvando dados em: {DATA_DIR.absolute()}\n")

    download_statsbomb_360()
    download_metrica_sports()
    download_skillcorner_opendata()
    info_soccernet()

    print("\n=== COLETA FINALIZADA ===")
    print("Seus dados brutos estão prontos para virar tensores na RTX 5070.")


if __name__ == "__main__":
    main()
