from qiime2.plugin import SemanticType, model
from q2_types.feature_data import FeatureData


FactorGroups = SemanticType('FactorGroups', variant_of=FeatureData.field['type'])


class FactorGroupsFormat(model.TextFileFormat):
    # Update with required formatting
    def validate(*args):
        pass


FactorGroupsDirFmt = model.SingleFileDirectoryFormat(
    'FactorGroupsDirFmt', 'factor_groups.tsv', FactorGroupsFormat)
