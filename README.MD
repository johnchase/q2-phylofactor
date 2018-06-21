### Base Phylofactor q2-plugin
This package is being actively developed and not in a state that will be
consistently useable. If you are looking for the Phylofactor R package that may
be found here: https://github.com/reptalex/phylofactor


Phylofactor API call:
```python
pf = phylofactor.methods.phylofactor(s1_data, 
                                     unrooted_tree, 
                                     s1_metadata, 
                                     family='binomial', 
                                     formula='BodySite~Data',
                                     choice='F',
                                     nfactors=2,
                                     ncores=10)
```

Cross validate map API call:

```python
cvm = phylofactor.methods.cross_validate_map(table=s2_data,
                                             groups=pf.groups,
                                             phylogeny=pf.tree,
                                             full_phylogeny=unrooted_tree)
```





