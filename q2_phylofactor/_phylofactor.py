import os
import subprocess
import tempfile
import biom
import skbio

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
                 metadata,
                 family,
                 formula,
                 choice,
                 nfactors,
                 ncores):

    with tempfile.TemporaryDirectory() as temp_dir_name:
        input_table = os.path.join(temp_dir_name, 'table.tsv')
        input_metadata = os.path.join(temp_dir_name, 'metadata.tsv')
        with open(input_table, 'w') as fh:
            fh.write(table.to_tsv())
        metadata.save(input_metadata)

        biom_output = os.path.join(temp_dir_name, 'out_table.tsv')
        tree_output = os.path.join(temp_dir_name, 'tree.nwk')

        cmd = ['run_phylofactor.R',
               input_table,
               str(phylogeny),
               input_metadata,
               str(family),
               str(formula),
               str(choice),
               str(nfactors),
               str(ncores),
               str(biom_output),
               str(tree_output)]
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
        tree = skbio.tree.TreeNode.read(tree_output)
    return biom_table, tree


def phylofactor(table: biom.Table,
                phylogeny: NewickFormat,
                metadata: Metadata,
                family: str,
                formula: str = 'Data ~ X',
                choice: str = 'F',
                nfactors: int = 10,
                ncores: int = 1
                ) -> (biom.Table, skbio.tree.TreeNode):
    return _phylofactor(table,
                        phylogeny,
                        metadata,
                        family,
                        formula,
                        choice,
                        nfactors,
                        ncores,
                        )
