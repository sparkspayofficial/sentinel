#!/bin/bash
set -evx

mkdir ~/.sparkscore

# safety check
if [ ! -f ~/.sparkscore/.sparks.conf ]; then
  cp share/sparks.conf.example ~/.sparkscore/sparks.conf
fi
