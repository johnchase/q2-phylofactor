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
        biom_fp = os.path.join(temp_dir_name, 'output.tsv.biom')
        cmd = ['_phylofactor.R',
               str(table),
               biom_fp,
               str(phylogeny),
               str(taxonomy),
               str(metadata),
               str(formula),
               str(choice),
               str(nfactors),
               str(ncores)]
        try:
            run_commands([cmd])
        except subprocess.CalledProcessError as e:
            raise Exception("An error was encountered with PhyloFactor"
                            " in R (return code %d), please inspect stdout"
                            " and stderr to learn more." % e.returncode)
    with open(biom_fp) as fh:
        table = biom.Table.from_tsv(fh)
    return table


def phylofactor(table: BIOMV210Format,
                phylogeny: NewickFormat,
                taxonomy: TSVTaxonomyFormat,
                metadata: Metadata,
                formula: str,
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
