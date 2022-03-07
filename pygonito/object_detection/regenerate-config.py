#!/usr/bin/env python3

import sys
import re

in_dir = sys.argv[1]

labels = set()

with open(f'{in_dir}/train/expected.tsv') as expected_file:
    for line in expected_file:
        for match in re.finditer(r'(^|\s)(\S+):', line):
            label = match.group(2)
            labels.add(label)

extra_metrics = ''

if len(labels) > 0 and len(labels) < 50:
    labs = ','.join(f't<{lab}:>N<{lab}>' for lab in labels)
    extra_metrics = ' --metric Probabilistic-Soft2D-{F1:N<F1>P<2>,F0:N<P>P<3>,F999999:N<R>P<3>}{' + labs + '}'

with open(f'{in_dir}/config.txt', 'w') as config_file:
    print('--metric Probabilistic-Soft2D-F1:N<F1> --metric Probabilistic-Soft2D-F0:N<P>P<2> --metric Probabilistic-Soft2D-F999999:N<R>P<2> --precision 4 -%' + extra_metrics,
          file=config_file)
