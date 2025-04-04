import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


class PlotHelper:

    @staticmethod
    def plot_with_rolling_average(df: pd.DataFrame, x: str, y: str, window: int = 10):
        """
        Affiche un graphique avec la courbe des données `y` en fonction de `x`, ainsi qu'une moyenne glissante.

        Parameters:
        - df: Le DataFrame contenant les données.
        - x: La colonne à utiliser pour l'axe des X.
        - y: La colonne à utiliser pour l'axe des Y.
        - window: Taille de la fenêtre pour la moyenne glissante (par défaut 10).
        """
        plt.figure(figsize=(12, 6))

        # Courbe avec une moyenne glissante (moving average)
        sns.lineplot(
            x=x,
            y=y,
            data=df.rolling(window=window, on=x).mean(),
            label=f"Moving average {y} (rolling {window})",
            color="blue"
        )

        # Courbe sans moyenne glissante
        sns.lineplot(
            x=x,
            y=y,
            data=df,
            label=f"{y}",
            color="red",
            linestyle='--'
        )

        plt.title(f"{y} en fonction de {x}")
        plt.xlabel(f"{x} value")
        plt.ylabel(f"{y}")
        plt.legend()
        plt.tight_layout()
        plt.show()

# Exemple d'utilisation
# df = pd.DataFrame({'initial': range(1, 101), 'flyTime': some_data})
# PlotHelper.plot_with_rolling_average(df, 'initial', 'flyTime')
