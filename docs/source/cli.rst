.. _cli:

Command Line Interface
======================

* Link stream generation from weighted graph and timeserie.

Input Format
------------

The genbip package takes as input a weighted graph and a timeserie, both as
text files compressed using gzip.
The content of both file is separated by spaces:

      idx1 val1
      idx2 val2
      ...

In the timeserie, `idx` denotes the timestamps and `val` the value,
in the weighted graph `idx` denotes the edge (usually written as `u,v` where
u and v are the nodes) and `val` denotes the weight.

Simple Example
--------------

* Given a weighted graph `data_graph.txt.gz` and a timeserie 
  `data_serie.txt.gz`, the following will build a link stream using a
  Havel-Hakimi model and write it as `data_stream.txt.gz`:

.. code-block:: bash

   python cli.py --top data_graph.txt.gz --bot data_serie.txt.gz --gen havelhakimi --out data_stream.txt.gz
