.. image:: http://b.dryicons.com/images/icon_sets/blue_extended_icons_set/png/128x128/chart.png
MIA Backtesting Engine (based on bt)
====================================

What is MIA-BT?
-----------

**MIA-BT** is a flexible backtesting framework that will be used for Project MIA. It currently offers vectorized backtesting, but event-driven backtesting is also planned. MIA-BT is based on bt by PMorissette.

What is bt?
-----------

**bt** is a flexible backtesting framework for Python used to test quantitative trading strategies. **Backtesting** is the process of testing a strategy over a given data set. This framework allows you to easily create strategies that mix and match different `Algos <http://pmorissette.github.io/bt/bt.html#bt.core.Algo>`_. It aims to foster the creation of easily testable, re-usable and flexible blocks of strategy logic to facilitate the rapid development of complex trading strategies. 

**bt** is coded in **Python** and joins a vibrant and rich ecosystem for data analysis. Numerous libraries exist for machine learning, signal processing and statistics and can be leveraged to avoid re-inventing the wheel - something that happens all too often when using other languages that don't have the same wealth of high-quality, open-source projects.

bt is built atop `ffn <https://github.com/pmorissette/ffn>`_ - a financial function library for Python.

Features
---------

* **Tree Structure**
    `The tree structure <http://pmorissette.github.io/bt/tree.html>`_ facilitates the construction and composition of complex algorithmic trading 
    strategies that are modular and re-usable. Furthermore, each tree `Node
    <http://pmorissette.github.io/bt/bt.html#bt.core.Node>`_
    has its own price index that can be
    used by Algos to determine a Node's allocation. 

* **Algorithm Stacks**
    `Algos <http://pmorissette.github.io/bt/bt.html#bt.core.Algo>`_ and `AlgoStacks <http://pmorissette.github.io/bt/bt.html#bt.core.AlgoStack>`_ are
    another core feature that facilitate the creation of modular and re-usable strategy
    logic. Due to their modularity, these logic blocks are also easier to test -
    an important step in building robust financial solutions.

* **Charting and Reporting**
    bt also provides many useful charting functions that help visualize backtest
    results. We also plan to add more charts, tables and report formats in the future, 
    such as automatically generated PDF reports.

* **Detailed Statistics**
    Furthermore, bt calculates a bunch of stats relating to a backtest and offers a quick way to compare
    these various statistics across many different backtests via `Results'
    <http://pmorissette.github.io/bt/bt.html#bt.backtest.Result>`_ display methods.


Roadmap
--------

Future development efforts will focus on extending the engine to meet MIA's requirments:

* **Vectorized backtesting**
    The main objective is to focus on improving on the vectorized backtesting.

* **Event-based backtesting**
    Event-based backtesting is planned by modifying the vectorized backtesting.

Installing bt
-------------

The easiest way to install ``bt`` is from the `Python Package Index <https://pypi.python.org/pypi/bt/>`_
using ``pip`` or ``easy_insatll``:

.. code-block:: bash

    $ pip install bt 

Since bt has many dependencies, we strongly recommend installing the `Anaconda Scientific Python
Distribution <https://store.continuum.io/cshop/anaconda/>`_, especially on Windows. This distribution 
comes with many of the required packages pre-installed, including pip. Once Anaconda is installed, the above 
command should complete the installation. 

MIA-BT should be compatible with Python 2.7.