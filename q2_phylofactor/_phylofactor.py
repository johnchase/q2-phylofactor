import os
import subprocess
import tempfile
import biom


from q2_types.feature_table import FeatureTable, Frequency, BIOMV210Format
from q2_types.tree import NewickFormat
from q2_types.feature_data import TSVTaxonomyFormat

from qiime2 import Metadata


def run_commands(cmds, verbose=True):
    if verbose:
        print("Running external command line application(s). This may print "
              "messages to stdout and/or stderr.")
        print("The command(s) being run are below. These commands cannot "
              "be manually re-run as they will depend on temporary files that "
              "no longer exist.")
    for cmd in cmds:
        if verbose:
            print("\nCommand:", end=' ')
            print(" ".join(cmd), end='\n\n')
        subprocess.run(cmd, check=True)


def _phylofactor(table,
                 phylogeny,
                 taxonomy,
                 metadata,
                 formula,
                 choice,
                 nfactors,
                 ncores):

    with tempfile.TemporaryDirectory() as temp_dir_name:
        input_table = os.path.join(temp_dir_name, 'table.tsv')
        input_metadata = os.path.join(temp_dir_name, 'metadata.tsv')
        with open(input_table, 'w') as fh:
            fh.write(table.to_tsv())
        foo = '/home/john/dev/q2-phylofactor/test_table_qiime.tsv'
        with open(foo, 'w') as fh:
            fh.write(table.to_tsv())
        metadata.save(input_metadata)
        biom_output = os.path.join(temp_dir_name, 'out_table.tsv')
        cmd = ['run_phylofactor.R',
               input_table,
               str(biom_output),
               str(phylogeny),
               str(taxonomy),
               input_metadata,
               str(formula),
               str(choice),
               str(nfactors),
               str(ncores)]
        try:
            print('Running Commands')
            run_commands([cmd])
        except subprocess.CalledProcessError as e:
            raise Exception("An error was encountered with PhyloFactor"
                            " in R (return code %d), please inspect stdout"
                            " and stderr to learn more." % e.returncode)
# I think I may be able to skip this step by writing directly to a format
# but I'm not excactly sure yet
        with open(biom_output) as fh:
            biom_table = biom.Table.from_tsv(fh, None, None, None)
    return biom_output

def phylofactor(table: biom.Table,
                phylogeny: NewickFormat,
                taxonomy: TSVTaxonomyFormat,
                metadata: Metadata,
                formula: str='Data ~ X',
                choice: str='F',
                nfactors: int=10,
                ncores: int=1
                ) -> (biom.Table):
    return _phylofactor(table,
                        phylogeny,
                        taxonomy,
                        metadata,
                        formula,
                        choice,
                        nfactors,
                        ncores,
                        )
