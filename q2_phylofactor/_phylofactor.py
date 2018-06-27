import os
import subprocess
import tempfile
import biom
import skbio
import pandas as pd
import qiime2

from q2_types.tree import NewickFormat
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
        factor_ratio_output = os.path.join(temp_dir_name, 'factor_ratios.tsv')
        factor_output = os.path.join(temp_dir_name, 'factors.tsv')

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
               str(tree_output),
               str(factor_ratio_output),
               str(factor_output)]
        try:
            print('Running Commands')
            run_commands([cmd])
        except subprocess.CalledProcessError as e:
            raise Exception("An error was encountered with PhyloFactor"
                            " in R (return code %d), please inspect stdout"
                            " and stderr to learn more." % e.returncode)
        with open(biom_output) as fh:
            biom_table = biom.Table.from_tsv(fh, None, None, None)
        tree = skbio.tree.TreeNode.read(tree_output)
        # I think there is a way to remove the pandas call and just use Factors
        factor_ratios = pd.read_csv(factor_ratio_output, sep='\t')
        factors = pd.read_csv(factor_output, sep='\t')
    return biom_table, tree, factor_ratios, factors

# Does this really need to be it's own function?
def phylofactor(table: biom.Table,
                phylogeny: NewickFormat,
                metadata: Metadata,
                family: str,
                formula: str = 'Data ~ X',
                choice: str = 'F',
                nfactors: int = 10,
                ncores: int = 1
                ) -> (biom.Table,
                      skbio.tree.TreeNode,
                      pd.DataFrame,
                      pd.DataFrame):

    return _phylofactor(table,
                        phylogeny,
                        metadata,
                        family,
                        formula,
                        choice,
                        nfactors,
                        ncores,
                        )


def cross_validate_map(table: biom.Table,
                       groups: pd.DataFrame,
                       phylogeny: NewickFormat,
                       full_phylogeny: NewickFormat,
                       ) -> (biom.Table, pd.DataFrame):

    with tempfile.TemporaryDirectory() as temp_dir_name:
        input_table = os.path.join(temp_dir_name, 'table.tsv')
        with open(input_table, 'w') as fh:
            fh.write(table.to_tsv())

        input_groups = os.path.join(temp_dir_name, 'groups.tsv')
        groups.to_csv(input_groups, sep='\t')

        biom_output = os.path.join(temp_dir_name, 'out_table.tsv')
        group_output = os.path.join(temp_dir_name, 'groups_out.tsv')

        cmd = ['run_crossVmap.R',
               input_table,
               input_groups,
               str(phylogeny),
               str(full_phylogeny),
               str(biom_output),
               str(group_output)]

        try:
            print('Running Commands')
            run_commands([cmd])
        except subprocess.CalledProcessError as e:
            raise Exception("An error was encountered with PhyloFactor"
                            " in R (return code %d), please inspect stdout"
                            " and stderr to learn more." % e.returncode)

        with open(biom_output) as fh:
            biom_table = biom.Table.from_tsv(fh, None, None, None)
        group_output_df = pd.read_csv(group_output, sep='\t')

    return biom_table, group_output_df
