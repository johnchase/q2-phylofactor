import q2_phylofactor
import qiime2

from qiime2.plugin import (
    Plugin,
    Str,
    Int,
    Metadata)

from q2_types.feature_table import FeatureTable, Frequency
from q2_phylofactor._phylofactor import phylofactor
from q2_types.tree import Phylogeny, Unrooted
from q2_types.feature_data import FeatureData, Taxonomy


_CHOICE_OPT = {'F', 'var', 'none'}

plugin = Plugin(
    name='phylofactor',
    version=q2_phylofactor.__version__,
    website='https://github.com/johnchase/q2-phylofactor',
    package='q2_phylofactor',
    description='Plugin defining clades associated with given metadata '
                'category`',
    short_description='Plugin for running phylofactor',
    )

plugin.methods.register_function(
    function=phylofactor,
    inputs={'table': FeatureTable[Frequency],
            'phylogeny': Phylogeny[Unrooted],
            'taxonomy': FeatureData[Taxonomy]
            },
    parameters={
        'metadata': Metadata,
        'formula': Str,
        'family': Str,
        'choice': Str % qiime2.plugin.Choices(_CHOICE_OPT),
        'nfactors': Int,
        'ncores': Int
    },
    outputs=[
        ('featuretable', FeatureTable[Frequency])
    ],
    input_descriptions={
        },
    parameter_descriptions={
        },
    output_descriptions={
        },
    name='Run Phylofactor',
    description='Phylofactor defines clades that are associated with '
                'metadata columns of interest'
)
