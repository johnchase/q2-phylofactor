import qiime2
import pandas as pd

from q2_phylofactor import FactorGroupsFormat
from q2_phylofactor.plugin_setup import plugin


@plugin.register_transformer
def _1(ff: FactorGroupsFormat) -> pd.DataFrame:
    return pd.read_csv((str(ff)), sep='\t', index_col=0)


@plugin.register_transformer
def _2(df: pd.DataFrame) -> FactorGroupsFormat:
    ff = FactorGroupsFormat()
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
