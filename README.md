# TDMchopS
#### Collection of code that chops in time chunks of NTCAP (iq.tdms) data in order to perform high-precision analysis of Schottky signals for mass-and lifetime measurements of ringed ions.
[![documentation](https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat)](https://DFreireF.github.io/tdmchops)[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.8172226.svg)](https://doi.org/10.5281/zenodo.8172226)

At GSI, the NTCAP (DAQ) records iq and sc data continuously in time. However, in order to analyse the data for lifetime and mass measurements we are interested in analysing the different injections at the same time, therefore we need to know the injection time. For that, with this collection of code we can create a mapping between absolute injection time and in which recorded file they corresponds, to cut the data of any injection at any time from injection that we want and it is added everything into the same 2D power array obtained by using `iqtools` by @xaratustrah.
It is still in developement, in its final version it should cut the data in the wanted time until next injection and create new files with the cutted data.
