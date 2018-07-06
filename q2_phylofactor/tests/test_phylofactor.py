import unittest

from qiime2.plugin.testing import TestPluginBase
from q2_phylofactor import phylofactor
from q2_types.tree import NewickFormat
from skbio.tree import TreeNode
import qiime2
import biom
import pandas as pd
from pandas.util.testing import assert_frame_equal


class TestPhylofactor(TestPluginBase):
    package = 'q2_phylofactor.tests'

    def setUp(self):
        super().setUp()
        with open(self.get_data_path('asv_table.tsv')) as fh:
            self.table = biom.Table.from_tsv(fh, None, None, None)
        self.phylogeny = NewickFormat(self.get_data_path('tree.nwk'),
                                      mode='r')
        self.metadata = (qiime2.Metadata
                         .load(self.get_data_path('metadata.tsv')))

    def test_defaults(self):

        exp_basis = pd.read_csv(
            self.get_data_path('expected/categorical_basis.tsv'), sep='\t')
        exp_groups = pd.read_csv(
            self.get_data_path('expected/categorical_groups.tsv'), sep='\t')
        exp_factors = pd.read_csv(
            self.get_data_path('expected/categorical_factors.tsv'), sep='\t')
        exp_tree = TreeNode.read(self
        .get_data_path('expected/categorical_tree.nwk'))

        pf = phylofactor(self.table,
                         self.phylogeny,
                         self.metadata,
                         formula='Categorical~Data',
                         nfactors=3,
                         family='binomial')

        basis, out_tree, groups, factors = pf

        assert_frame_equal(basis, exp_basis)
        assert_frame_equal(groups, exp_groups)
        assert_frame_equal(factors, exp_factors)
        self.assertEqual(TreeNode.compare_rfd(exp_tree, out_tree), 0)


    def test_continous(self):
        exp_basis = pd.read_csv(
            self.get_data_path('expected/numeric_basis.tsv'), sep='\t')
        exp_groups = pd.read_csv(
            self.get_data_path('expected/numeric_groups.tsv'), sep='\t')
        exp_factors = pd.read_csv(
            self.get_data_path('expected/numeric_factors.tsv'), sep='\t')
        exp_tree = (TreeNode.read(self
        .get_data_path('expected/numeric_tree.nwk')))

        pf = phylofactor(self.table,
                         self.phylogeny,
                         self.metadata,
                         formula='Continuous~Data',
                         nfactors=3,
                         family='poisson')

        basis, out_tree, groups, factors = pf

        assert_frame_equal(basis, exp_basis)
        assert_frame_equal(groups, exp_groups)
        assert_frame_equal(factors, exp_factors)
        self.assertEqual(TreeNode.compare_rfd(exp_tree, out_tree), 0)


    # def test_non_matching_tips(self):
    #     pass
    # def test_missing_columns(self):
    #     pass
    # def test_choice_var(self):
    #     pass


if __name__ == '__main__':
    unittest.main()
