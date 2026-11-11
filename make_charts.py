"""Génère les graphiques du README à partir des CSV de results/ (lancer run_query.py avant)."""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap

RACINE = Path(__file__).resolve().parent
RESULTATS = RACINE / "results"
GRAPHIQUES = RACINE / "charts"

FOND = "#fcfcfb"
TEXTE = "#0b0b0b"
TEXTE_SECONDAIRE = "#52514e"
TEXTE_DISCRET = "#898781"
GRILLE = "#e1e0d9"
AXE = "#c3c2b7"
BLEU = "#2a78d6"
RAMPE_BLEUE = ["#cde2fb", "#86b6ef", "#3987e5", "#1c5cab", "#0d366b"]

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "figure.facecolor": FOND,
    "axes.facecolor": FOND,
    "savefig.facecolor": FOND,
    "text.color": TEXTE,
    "axes.labelcolor": TEXTE_SECONDAIRE,
    "xtick.color": TEXTE_DISCRET,
    "ytick.color": TEXTE_DISCRET,
    "xtick.labelcolor": TEXTE_SECONDAIRE,
    "ytick.labelcolor": TEXTE_SECONDAIRE,
    "axes.edgecolor": AXE,
})


def titrer(fig, titre, sous_titre):
    hauteur = fig.get_figheight()
    fig.text(0.02, 1 - 0.18 / hauteur, titre, fontsize=13, fontweight="bold", va="top")
    fig.text(0.02, 1 - 0.48 / hauteur, sous_titre, fontsize=9.5, color=TEXTE_SECONDAIRE, va="top")


def epurer(ax, grille="y"):
    for cote in ("top", "right", "left"):
        ax.spines[cote].set_visible(False)
    ax.tick_params(length=0)
    if grille:
        ax.grid(axis=grille, color=GRILLE, linewidth=0.8)
        ax.set_axisbelow(True)


def ventes_mensuelles():
    df = pd.read_csv(RESULTATS / "01_ventes_mensuelles.csv")
    ca = df["chiffre_affaires"] / 1e6
    fig, ax = plt.subplots(figsize=(9, 4.4))
    fig.subplots_adjust(top=0.80, left=0.07, right=0.97, bottom=0.12)
    ax.plot(range(len(df)), ca, color=BLEU, linewidth=2)
    pic = ca.idxmax()
    ax.scatter([pic], [ca[pic]], s=45, color=BLEU, edgecolor=FOND, linewidth=2, zorder=3)
    ax.annotate(
        f"Novembre 2017 (Black Friday)\n{ca[pic]:.2f} M R$".replace(".", ","),
        (pic, ca[pic]), xytext=(-12, 0), textcoords="offset points",
        ha="right", va="center", fontsize=9, color=TEXTE_SECONDAIRE,
    )
    ax.set_xticks(range(0, len(df), 2))
    ax.set_xticklabels(df["mois"][::2], fontsize=8.5)
    ax.set_ylim(0, 1.3)
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0, 1.25])
    ax.yaxis.set_major_formatter(lambda v, _: f"{v:.2f}".replace(".", ","))
    epurer(ax)
    titrer(fig, "Chiffre d'affaires mensuel",
           "Commandes livrées, en millions de R$, janvier 2017 à août 2018")
    fig.savefig(GRAPHIQUES / "ca_mensuel.png", dpi=160)
    plt.close(fig)


def cohortes():
    df = pd.read_csv(RESULTATS / "03_cohortes_retention.csv")
    grille = df.pivot(index="cohorte", columns="mois_ecoules", values="taux_retention")
    grille = grille.reindex(columns=range(1, 13))
    # Un mois observable sans aucun réachat vaut 0 % (et non « pas de donnée »)
    dernier_mois = pd.Period(df["cohorte"].max(), freq="M") + 1
    for cohorte in grille.index:
        observables = (dernier_mois - pd.Period(cohorte, freq="M")).n
        colonnes = [m for m in grille.columns if m <= observables]
        grille.loc[cohorte, colonnes] = grille.loc[cohorte, colonnes].fillna(0)
    carte = LinearSegmentedColormap.from_list("bleu", RAMPE_BLEUE)
    carte.set_bad(FOND)
    fig, ax = plt.subplots(figsize=(9, 6.2))
    fig.subplots_adjust(top=0.84, left=0.10, right=0.99, bottom=0.09)
    image = ax.pcolormesh(grille.values, cmap=carte, vmin=0, vmax=0.75,
                          edgecolors=FOND, linewidth=2)
    ax.invert_yaxis()
    ax.set_xticks([i + 0.5 for i in range(12)])
    ax.set_xticklabels([f"M+{i}" for i in range(1, 13)], fontsize=8.5)
    ax.set_yticks([i + 0.5 for i in range(len(grille))])
    ax.set_yticklabels(grille.index, fontsize=8.5)
    ax.set_ylabel("Cohorte (mois du premier achat)")
    for cote in ax.spines.values():
        cote.set_visible(False)
    ax.tick_params(length=0)
    barre = fig.colorbar(image, ax=ax, pad=0.02, shrink=0.6)
    barre.outline.set_visible(False)
    barre.ax.tick_params(length=0, labelsize=8.5)
    barre.ax.yaxis.set_major_formatter(lambda v, _: f"{v:.2f} %".replace(".", ","))
    titrer(fig, "Rétention par cohorte d'acquisition",
           "Part des clients d'une cohorte qui recommandent N mois après leur premier achat "
           "(jamais plus de 0,75 %)")
    fig.savefig(GRAPHIQUES / "cohortes_retention.png", dpi=160)
    plt.close(fig)


def livraison():
    df = pd.read_csv(RESULTATS / "07_livraison_satisfaction.csv").iloc[::-1]
    fig, ax = plt.subplots(figsize=(9, 3.4))
    fig.subplots_adjust(top=0.76, left=0.26, right=0.97, bottom=0.12)
    barres = ax.barh(df["livraison"], df["note_moyenne"], color=BLEU, height=0.5)
    for barre, note, part in zip(barres, df["note_moyenne"], df["part_commandes"]):
        ax.text(barre.get_width() + 0.06, barre.get_y() + barre.get_height() / 2,
                f"{note:.2f}".replace(".", ",") + f"   ({part:.1f} % des commandes)".replace(".", ","),
                va="center", fontsize=9, color=TEXTE_SECONDAIRE)
    ax.set_xlim(0, 7.2)
    ax.set_xticks(range(0, 6))
    epurer(ax, grille="x")
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(True)
    titrer(fig, "Note client moyenne selon le respect du délai de livraison",
           "Note sur 5, commandes livrées, retard mesuré par rapport à la date estimée")
    fig.savefig(GRAPHIQUES / "livraison_satisfaction.png", dpi=160)
    plt.close(fig)


if __name__ == "__main__":
    GRAPHIQUES.mkdir(exist_ok=True)
    ventes_mensuelles()
    cohortes()
    livraison()
    print("Graphiques enregistrés dans charts/")
