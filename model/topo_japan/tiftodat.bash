#!/bin/bash
ml gcc gdal/2.4.1
gdal_translate -of XYZ topo_japan.tiff topo_japan.dat
