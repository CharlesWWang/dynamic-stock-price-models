# Dynamic stock price models

An __ongoing__ implementation of dynamic models of stock prices based on technical trading rules. 

A description of the models can be found in a [paper](https://arxiv.org/abs/1401.1888) published by [Li-Xin Wang](https://arxiv.org/find/q-fin/1/au:+Wang_L/0/1/0/all/0/1). For now, **the goal of this implementation is to reproduce the results obtained by Li-Xin Wang** for further study.

# Concept

1. Agents' (investor) reaction to the stock market depends on a qualitative (__large__, __medium__, __small__) measure of fluctuation in prices. Actions agents perform, such as __invest__ or __withdraw__ are also qualified by the same vague measures. As such, we first formalize the ideas of __large__, __medium__ and __small__ using [fuzzy sets](https://en.wikipedia.org/wiki/Fuzzy_set).

2. Todo...

# Usage

As of the most recent commit, fuzzy sets are implemented. Figures 1 and 2 in the paper, depicting the memberhsip domains of specific fuzzy sets can now be reproduced by running

```python
python generate_figures.py
```

