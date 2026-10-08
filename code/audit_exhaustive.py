#!/usr/bin/env python3
"""Exact weighted-support audit requested for the publication package."""

from datetime import datetime, timezone
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import platform
import sys
import time

from exact_checker import (normalise,classify,direct_gap,analytic_gap,
                           exact_failure_witness,serialise)
from finite_alphabet_audit import run_checks


def main():
    started = datetime.now(timezone.utc).isoformat()
    clock = time.perf_counter()
    root = Path(__file__).resolve().parent
    grid = (F(0),F(1,3),F(2,3),F(1))
    kernels = tuple(((a,1-a),(b,1-b)) for a,b in product(grid,repeat=2))
    table_count = orientation_count = accepted = rejected = kernel_comparisons = 0
    strong_count = degenerate_count = 0
    masks = set()
    overlap_counts = {0:0,1:0,2:0}
    witness_file = root/"exhaustive_witnesses.jsonl"
    with witness_file.open("w") as output:
        for counts in product(range(3),repeat=8):
            if not any(counts):
                continue
            p = normalise(counts)
            table_count += 1
            mask = sum(1<<i for i,v in enumerate(counts) if v)
            masks.add(mask)
            c = classify(p)
            strong_count += c["strong_substitutes"]
            for source in ("X","Y"):
                d = c["directions"][source]
                orientation_count += 1
                degenerate_count += d["degenerate_source"]
                if not d["degenerate_source"]:
                    overlap_counts[len(d["overlap"])] += 1
                if d["passes"]:
                    accepted += 1
                    for kernel in kernels:
                        direct = direct_gap(p,source,kernel)["gap"]
                        if not (direct==analytic_gap(p,source,kernel)):
                            raise AssertionError('Exact audit condition failed')
                        if not (direct>=0):
                            raise AssertionError((counts,source,kernel,direct))
                        kernel_comparisons += 1
                else:
                    rejected += 1
                    witness = exact_failure_witness(p,source)
                    if not (witness["gap"]<0):
                        raise AssertionError('Exact audit condition failed')
                    if not (witness["gap"]==analytic_gap(p,source,witness["kernel"])):
                        raise AssertionError('Exact audit condition failed')
                    record = {"counts":counts,"source":source,
                              "margins":d["margins"],
                              "kernel":witness["kernel"],"gap":witness["gap"]}
                    output.write(json.dumps(serialise(record),separators=(",",":"))+"\n")
            if table_count%1000==0:
                print(json.dumps({"tables_checked":table_count,"elapsed_seconds":round(time.perf_counter()-clock,3)}),flush=True)
    if not (table_count==6560):
        raise AssertionError('Exact audit condition failed')
    if not (len(masks)==255):
        raise AssertionError('Exact audit condition failed')
    if not (accepted+rejected==orientation_count==13120):
        raise AssertionError('Exact audit condition failed')
    extended = run_checks()
    files = ("exact_checker.py","finite_alphabet_audit.py","audit_exhaustive.py","exhaustive_witnesses.jsonl")
    report = {
        "status":"PASS","started_utc":started,
        "finished_utc":datetime.now(timezone.utc).isoformat(),
        "elapsed_seconds":round(time.perf_counter()-clock,3),
        "command":"python audit_exhaustive.py",
        "python_version":sys.version,
        "implementation":platform.python_implementation(),
        "arithmetic":"fractions.Fraction; no floating-point mathematical decisions",
        "corpus":"All eight-entry count tables in {0,1,2}^8 except the zero table, normalised by their sum",
        "tables_checked":table_count,"different_nonempty_supports":len(masks),
        "strong_substitute_tables":strong_count,"orientations_checked":orientation_count,
        "accepted_orientations":accepted,"rejected_orientations":rejected,
        "degenerate_source_orientations":degenerate_count,
        "nondegenerate_orientations_by_overlap_size":overlap_counts,
        "accepted_orientation_raw_kernel_comparisons":kernel_comparisons,
        "binary_kernel_grid":[str(x) for x in grid],
        "rejected_orientation_direct_negative_witnesses":rejected,
        "full_proof_claim":False,
        "scope_note":"Sanity checks of independently evaluated raw-score gaps; the universal result rests on the analytic proof",
        "finite_alphabet_extension":extended,
        "sha256":{filename:hashlib.sha256((root/filename).read_bytes()).hexdigest() for filename in files},
    }
    rendered = json.dumps(serialise(report),indent=2,sort_keys=True)+"\n"
    (root/"exhaustive_audit_results.json").write_text(rendered)
    (root/"exhaustive_audit.log").write_text(rendered)
    print(rendered,end="")


if __name__=="__main__":
    main()
