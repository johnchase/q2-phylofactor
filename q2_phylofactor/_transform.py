import qiime2

from q2_phylofactor.import FactorsFormat
from q2_phylofactor.plugin_setup import plugin


@plugin.register_transformer
def _1(ff: FactorsFormat) -> qiime2.Metadata:
    return qiime2.Metadata.load(str(ff))


@plugin.register_transformer
def _2(obj: qiime2.Metadata) -> FactorsFormat:
    ff = FactorsFormat()
    obj.save(str(ff))
    return ff
