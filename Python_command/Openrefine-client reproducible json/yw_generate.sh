#!/usr/bin/env bash
alias yw='java -jar ~/yesworkflow-0.2.2.0-SNAPSHOT-jar-with-dependencies.jar'

cat yw/XLinearParseYW.txt | yw graph -c extract.comment='#' > gv/XLinear.gv

cat yw/2X_SPParseYW.txt | yw graph -c extract.comment='#' > gv/XSerial-Parallel.gv

dot -Tpdf gv/XLinear.gv -o pdf/XLinear.pdf

dot -Tpdf gv/XSerial-Parallel.gv -o pdf/XSerial-Parallel.pdf


dot -Tpng gv/XLinear.gv -o png/XLinear.png

dot -Tpng gv/XSerial-Parallel.gv -o png/XSerial-Parallel.png
