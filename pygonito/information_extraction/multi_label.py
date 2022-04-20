
from typing import Dict, Tuple
import regex as re

key_val_pair_regexp = re.compile(r'([^\s=]+)=(\S+)')
val_prob_regexp = re.compile(r'(.*):(\d+(?:\.\d*)?)$')


def unquote_value(val: str) -> str:
    return val.replace('_', ' ')


def parse_probs(val: str) -> Tuple[str, float]:
    m = val_prob_regexp.match(val)
    if m:
        return (m.group(1), float(m.group(2)))
    else:
        return (val, 1.0)


def parse_expected_line(line: str) -> Dict[str, str]:
    return {m.group(1): unquote_value(m.group(2))
            for m in key_val_pair_regexp.finditer(line)}


def parse_output_line(line: str) -> Dict[str, Tuple[str, float]]:
    kvs = parse_expected_line(line)
    return {k: parse_probs(v) for (k, v) in kvs.items()}
