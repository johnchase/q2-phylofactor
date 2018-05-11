from qiime2.plugin import (
    Plugin,
    Str,
    Numeric,
)

from q2_types.feature_table import FeatureTable, Frequency

import q2_phylofactor
from q2_phylofactor._phylofactor import phylofactor

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
    inputs={
    },
    parameters={
        'text': Str,
    },
    outputs=[
        ('featuretable', FeatureTable[Frequency])
    ],
    input_descriptions={
        },
    parameter_descriptions={
        'text': 'Number of CPU cores to use.',
    },
    output_descriptions={
        },
    name='Run Phylofactor',
    description='Phylofactor defines clades that are associated with '
                'metadata columns of interest'
)
