enrich_code_template = '''
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import gseapy as gp
from gseapy.plot import barplot, dotplot

outputFile='bar.pdf'
gene_sets=[]
organism=''
gene_list=[]
color=''

# Enrichr analysis of upregulated DEGs
enr_up = gp.enrichr(gene_list=gene_list,
                         gene_sets=gene_sets,
                         organism=organism,
                         outdir='test/enr_DEGs_GOBP_up',
                         )

"""Visualize GSEApy Results.
When multiple datasets exist in the input dataframe, the `group` argument is your friend.

:param df: GSEApy DataFrame results.
:param column: column name in `df` to map the x-axis data. Default: Adjusted P-value
:param group: group by the variable in `df` that will produce bars with different colors.
:param title: figure title.
:param cutoff: terms with `column` value < cut-off are shown. Work only for
               ("Adjusted P-value", "P-value", "NOM p-val", "FDR q-val")
:param top_term: number of top enriched terms grouped by `hue` are shown.
:param figsize: tuple, matplotlib figsize.
:param color: color or list or dict of matplotlib.colors. Must be reconigzed by matplotlib.
              if dict input, dict keys must be found in the `group`
:param ofname: output file name. If None, don't save figure

:return: matplotlib.Axes. return None if given ofname.
         Only terms with `column` <= `cut-off` are plotted.
"""
barplot(df=enr_up.res2d,
        column="Adjusted P-value",
        group=None,
        title='',
        cutoff=0.05,
        top_term=10,
        figsize=(4, 6),
        ofname=outputFile,
        color=color)
'''


def get_function_parameter_template(require_type):
    function = ''
    parameters = []
    if True:
        function = f"""
            def enrich(gene_list=[],
                       outputFile = 'bar.pdf',
                       gene_sets = [''],
                       organism = 'human',
                       color = ''):
            """
        parameters = ['gene_list', 'outputFile', 'gene_sets', 'organism', 'color']

    return function, parameters


def get_code_template(function):
    if True:
        return enrich_code_template

    return ""
