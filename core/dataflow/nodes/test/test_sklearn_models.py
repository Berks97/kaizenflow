import logging

import pandas as pd
import sklearn.linear_model as slmode

import core.artificial_signal_generators as casgen
import core.config_builders as cfgb
import helpers.unit_test as hut
from core.dataflow.nodes.sklearn_models import ContinuousSkLearnModel

_LOG = logging.getLogger(__name__)


class TestContinuousSkLearnModel(hut.TestCase):
    def test1(self) -> None:
        # Load test data.
        data = self._get_data(1)
        # Generate node config.
        config = cfgb.get_config_from_nested_dict(
            {
                "x_vars": ["x"],
                "y_vars": ["y"],
                "steps_ahead": 1,
                "model_kwargs": {
                    "alpha": 0.5,
                },
                "col_mode": "merge_all",
            }
        )
        # Load sklearn config and create modeling node.
        node = ContinuousSkLearnModel(
            "sklearn",
            model_func=slmode.Ridge,
            **config.to_dict(),
        )
        #
        df_out = node.fit(data)["df_out"]
        df_str = hut.convert_df_to_string(df_out, index=True, decimals=3)
        self.check_string(df_str)

    def test2(self) -> None:
        data = self._get_data(2)
        config = cfgb.get_config_from_nested_dict(
            {
                "x_vars": ["x"],
                "y_vars": ["y"],
                "steps_ahead": 2,
                "model_kwargs": {
                    "alpha": 0.5,
                },
                "col_mode": "merge_all",
            }
        )
        node = ContinuousSkLearnModel(
            "sklearn",
            model_func=slmode.Ridge,
            **config.to_dict(),
        )
        df_out = node.fit(data)["df_out"]
        df_str = hut.convert_df_to_string(df_out, index=True, decimals=3)
        self.check_string(df_str)

    def test3(self) -> None:
        """
        Test `slmode.Lasso` model.

        `Lasso` returns a one-dimensional array for a two-dimensional
        input.
        """
        data = self._get_data(1)
        config = cfgb.get_config_from_nested_dict(
            {
                "x_vars": ["x"],
                "y_vars": ["y"],
                "steps_ahead": 1,
                "model_kwargs": {
                    "alpha": 0.5,
                },
            }
        )
        node = ContinuousSkLearnModel(
            "sklearn",
            model_func=slmode.Lasso,
            **config.to_dict(),
        )
        df_out = node.fit(data)["df_out"]
        df_str = hut.convert_df_to_string(df_out, index=True, decimals=3)
        self.check_string(df_str)

    def test4(self) -> None:
        data = self._get_data(1)
        data_fit = data.loc[:"2010-01-01 00:29:00"]
        data_predict = data.loc["2010-01-01 00:30:00":]
        config = cfgb.get_config_from_nested_dict(
            {
                "x_vars": ["x"],
                "y_vars": ["y"],
                "steps_ahead": 1,
                "model_kwargs": {
                    "alpha": 0.5,
                },
                "col_mode": "merge_all",
            }
        )
        node = ContinuousSkLearnModel(
            "sklearn",
            model_func=slmode.Ridge,
            **config.to_dict(),
        )
        node.fit(data_fit)
        df_out = node.predict(data_predict)["df_out"]
        df_str = hut.convert_df_to_string(df_out, index=True, decimals=3)
        self.check_string(df_str)

    def test5(self) -> None:
        data = self._get_data(2)
        data_fit = data.loc[:"2010-01-01 00:29:00"]
        data_predict = data.loc["2010-01-01 00:30:00":]
        config = cfgb.get_config_from_nested_dict(
            {
                "x_vars": ["x"],
                "y_vars": ["y"],
                "steps_ahead": 2,
                "model_kwargs": {
                    "alpha": 0.5,
                },
            }
        )
        node = ContinuousSkLearnModel(
            "sklearn",
            model_func=slmode.Ridge,
            **config.to_dict(),
        )
        node.fit(data_fit)
        df_out = node.predict(data_predict)["df_out"]
        df_str = hut.convert_df_to_string(df_out, index=True, decimals=3)
        self.check_string(df_str)

    def _get_data(self, lag: int) -> pd.DataFrame:
        """
        Generate "random returns".

        Use lag + noise as predictor.
        """
        num_periods = 50
        total_steps = num_periods + lag + 1
        rets = casgen.get_gaussian_walk(0, 0.2, total_steps, seed=10).diff()
        noise = casgen.get_gaussian_walk(0, 0.02, total_steps, seed=1).diff()
        pred = rets.shift(-lag).loc[1:num_periods] + noise.loc[1:num_periods]
        resp = rets.loc[1:num_periods]
        idx = pd.date_range("2010-01-01", periods=num_periods, freq="T")
        df = pd.DataFrame.from_dict({"x": pred, "y": resp}).set_index(idx)
        return df