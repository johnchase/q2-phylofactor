import qiime2
import pandas as pd

from q2_phylofactor.import FactorsFormat
from q2_phylofactor.plugin_setup import plugin


def _factor_group_to_dataframe(filepath):
    """Convert FactorFormat to pandas dataframe
    ----------
    filepath : str
        Filepath pointing to the FactorFormat to transform.
    Returns
    -------
    pd.DataFrame
        DataFrame containing the Factors data. The index will be
    """

    df = pd.read_csv(filepath, sep='\t')

    if len(set(['factor', 'featureid', 'group']) - set(df.columns)) != 0:
        raise ValueError(
            "Factor format requires a header with `factor`, `group' and "
            "`featureid`")

    if len(df.index) < 1:
        raise ValueError("Taxonomy format requires at least one row of data.")

    return df


def _dataframe_to_factor_group(df):
    if len(df.index) < 1:
        raise ValueError("Factor format requires at least one row of data.")

    if len(set(['factor', 'featureid', 'group']) - set(df.columns)) != 0:
        raise ValueError(
            "Factor format requires a header with `factor`, `group' and "
            "`featureid`")

    ff = FactorsFormat()
    df.to_csv(str(ff), sep='\t', header=True, index=True)
    return ff


@plugin.register_transformer
def _1(ff: FactorsFormat) -> pd.DataFrame:
    return _factor_group_to_dataframe(str(ff))


@plugin.register_transformer
def _2(df: pd.DataFrame) -> FactorsFormat:
    return _dataframe_to_factor_group(df))

@plugin.register_transformer
def _3(ff: FactorsFormat) -> qiime2.Metadata:
    return qiime2.Metadata.load(str(ff))


@plugin.register_transformer
def _4(obj: qiime2.Metadata) -> FactorsFormat:
    ff = FactorsFormat()
    obj.save(str(ff))
    return ff
