import qiime2
import pandas as pd

from q2_phylofactor import FactorsFormat
from q2_phylofactor.plugin_setup import plugin


@plugin.register_transformer
def _1(ff: FactorsFormat) -> pd.DataFrame:
    return pd.read_csv((str(ff)), sep='\t', index_col=0)


@plugin.register_transformer
def _2(df: pd.DataFrame) -> FactorsFormat:
    ff = FactorsFormat()
    df.to_csv(str(ff), sep='\t', header=True, index=True)
    return ff



# These do not currently work
# @plugin.register_transformer
# def _3(ff: FactorsFormat) -> qiime2.Metadata:
#     return qiime2.Metadata.load(str(ff))
#
#
# @plugin.register_transformer
# def _4(obj: qiime2.Metadata) -> FactorsFormat:
#     ff = FactorsFormat()
#     obj.save(str(ff))
#     return ff
