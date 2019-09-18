Performance
============

Speed
------
FusionVet is very efficient. It took about **1 second** to examine 1 fusion in a typical 
TCGA BAM file (7.1 Gb, 184 million reads)

Comparison to other tools
-------------------------
We used FusionVet to detect ERG-TMPRSS2 fusion from the `333 TCGA prostate cancer
samples <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4695400/>`_. A sample is called
ERG-TMPRSS2 fusion positive if it has two or more supporting fragments. 

We then compare FusionVet result to:

 * FusionSeq-HighSens (`Sboner et al., Genome Biology, 2010 <https://www.ncbi.nlm.nih.gov/pubmed/20964841>`_)
 * MapSplice (`Wang et al., Nucleic Acids Res. 2010 <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2952873/>`_)
 * DEEPEST (`Dehghannasiri et al., PNAS 2019 <https://www.pnas.org/content/116/31/15524>`_)
 * PRADA (tumorfusions.org) (`Hu et al., Nucleic Acids Res. 2018 <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5753333/>`_)

We chose **FusionSeq-HighSens** and **MapSplice** because they were used in the original TCGA `Cell paper <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4695400>`_.
We chose **DEEPEST** and **PRADA** because they were newly developed and have demonstrated superior performance to other tools. 

.. image:: ./_static/Venn_5circles.png
   :height: 500 px
   :width: 500 px
   :scale: 80 %

It has been found that ERG expression is significantly increased in fusion positive samples through 
the TMPRSS2 (an androgen responsive gene) mediated over expression (`Tomlins et al., Science, 2005 <https://www.ncbi.nlm.nih.gov/pubmed/16254181>`_).
Therefore, we used ERG expression as an **indirect** measurement of the authenticity of ERG-TMPRSS2 fusions.

**FusionVet vs FusionSeq/MapSplice**

.. image:: ./_static/Figure_1AB.png
   :height: 500 px
   :width: 800 px
   :scale: 80 %     
   
**FusionVet vs DEEPEST**

.. image:: ./_static/Figure_1CD.png
   :height: 500 px
   :width: 800 px
   :scale: 80 %        

**FusionVet vs PRADA(TumorFusions.org)**

.. image:: ./_static/Figure_1EF.png
   :height: 500 px
   :width: 800 px
   :scale: 80 %           