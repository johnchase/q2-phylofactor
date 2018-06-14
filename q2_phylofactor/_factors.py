from qiime2.plugin import SemanticType, model
from q2_types.feature_data import FeatureData


Factors = SemanticType('Factors', variant_of=FeatureData.field['type'])


class FactorsFormat(model.TextFileFormat):
    def validate(*args):
        pass


FactorsDirFmt = model.SingleFileDirectoryFormat(
    'FactorsDirFmt', 'factors.tsv', FactorsFormat)
