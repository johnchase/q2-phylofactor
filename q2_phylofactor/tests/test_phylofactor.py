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
        with open(self.get_data_path('s1_data.tsv')) as fh:
            self.table = biom.Table.from_tsv(fh, None, None, None)
        self.phylogeny = NewickFormat(self.get_data_path('s1_tree.nwk'),
                                      mode='r')
        self.metadata = (qiime2.Metadata
                         .load(self.get_data_path('metadata.tsv')))

    def test_defaults(self):

        exp_factor_groups = pd.read_csv(
            self.get_data_path('expected/factor_groups.tsv'), sep='\t')
        exp_tree = TreeNode.read(self.get_data_path('expected/pf_tree.nwk'))

        pf = phylofactor(self.table,
                         self.phylogeny,
                         self.metadata,
                         formula='BodySite~Data',
                         nfactors=3,
                         family='binomial')

        factors, out_tree, factor_ratios, factor_groups = pf

        assert_frame_equal(factor_groups, exp_factor_groups)
        # self.assertEqual(out_tree
        #                  .compare_tip_distances(exp_tree, 0))


if __name__ == '__main__':
    unittest.main()
