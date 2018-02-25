#!/bin/bash

set -o verbose

FC=ifort

$FC -c getoptions.f90
$FC main.f90 getoptions.o -o idos-map

