#! /usr/bin/bash

tar czf my-genes.tar.gz *.nex
perl mb.pl my-genes.tar.gz -m bayes.txt -o my-genes-mb
bucky.pl my-genes-mb/my-genes.mb.tar -o mygenes-bucky
