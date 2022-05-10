
from typing import Dict, Tuple
import regex as re

key_val_pair_regexp = re.compile(r'([^\s=]+)=(\S+)')
val_prob_regexp = re.compile(r'(.*):(\d+(?:\.\d*)?)$')

def quote_value(val: str) -> str:
    return val.replace(' ', '_')

def unquote_value(val: str) -> str:
    return val.replace('_', ' ')


def parse_probs(val: str) -> Tuple[str, float]:
    m = val_prob_regexp.match(val)
    if m:
        return (m.group(1), float(m.group(2)))
    else:
        return (val, 1.0)


def clean_line(line: str) -> str:
    return line.rstrip('\n')


def parse_expected_line(line: str) -> Dict[str, str]:
    return {m.group(1): unquote_value(m.group(2))
            for m in key_val_pair_regexp.finditer(clean_line(line))}


def parse_output_line(line: str) -> Dict[str, Tuple[str, float]]:
    kvs = parse_expected_line(line)
    return {k: parse_probs(v) for (k, v) in kvs.items()}


def format_data_point(data_point: Tuple[str, Tuple[str, float]]) -> str:
    k, (v, p) = data_point
    prob_suffix = ':' + str(p) if p < 1.0 else ''
    return f'{k}={quote_value(v)}{prob_suffix}'
