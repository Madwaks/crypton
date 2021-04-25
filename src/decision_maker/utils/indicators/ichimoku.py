from typing import Tuple, Any

from pandas import Series, DataFrame

from decision_maker.utils.indicators.abstract import AbstractIndicatorFactory


class IchimokuFactory(AbstractIndicatorFactory):
    def tenkan(self, window: int = 9) -> Series:
        data = (
            self.quotations.high.rolling(window=window).max()
            + self.quotations.low.rolling(window=window).min()
        ) / 2
        data.name = "tenkan"
        return data

    def kijun(self, window: int = 26) -> Series:
        data = (
            self.quotations.high.rolling(window=window).max()
            + self.quotations.low.rolling(window=window).min()
        ) / 2
        data.name = "kijun"
        return data

    def kumo(self) -> Tuple[Any, Any]:
        ssa = ((self.tenkan() + self.kijun()) / 2).shift(26)
        ssa.name = "ssa"
        ssb = self.kijun(window=52).shift(26)
        ssb.name = "ssb"
        return ssa, ssb

    def heiken_ashi(self):
        return self._ha(self.quotations.copy(deep=True))[
            ["HA_Close", "HA_Open", "HA_Low", "HA_High"]
        ]

    def chikou(self):
        return self.quotations.close.shift(-26)

    @staticmethod
    def _ha(df: DataFrame):
        df["HA_Close"] = (df["open"] + df["high"] + df["low"] + df["close"]) / 4

        idx = df.index.name
        df.reset_index(inplace=True)

        for i in range(0, len(df)):
            if i == 0:
                df.loc[i, "HA_Open"] = (df.loc[i, "open"] + df.loc[i, "close"]) / 2
            else:
                df.loc[i, "HA_Open"] = (
                    df.loc[i - 1, "HA_Open"] + df.loc[i - 1, "HA_Close"]
                ) / 2

        if idx:
            df.set_index(idx, inplace=True)

        df["HA_High"] = df[["HA_Open", "HA_Close", "high"]].max(axis=1)
        df["HA_Low"] = df[["HA_Open", "HA_Close", "low"]].min(axis=1)
        return df
