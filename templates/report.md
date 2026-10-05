# Replace with the test subject

Date: Replace with the measurement date or date range.

Verdict: Replace with one sentence stating the measured result and its main limit.

## Environment

Record host hardware, GPU and memory, bare-metal or VM execution, OS and kernel, driver,
software and model revisions, quantization, and every flag that could change the result.
List the differences between compared configurations.

## Measurements

State the workload, repetitions, units, aggregation, variation, and measurement boundary.
Link each table to its reviewed evidence. Record failures and quality-screen outcomes.
Label estimates and predictions explicitly.

## Reproduction

Give commands, pinned dependencies, harness revision and hashes, synthetic inputs, and
chart-generation steps. Identify commands that change host state. Explain how to verify
the bundle with `sha256sum -c SHA256SUMS`.

## Limitations

State what the tests did not establish and which configuration changes require retesting.
Distinguish performance, correctness, and quality claims.

## Evidence

Link to the public data, figures, and procedure using paths relative to this report.
Record any omissions or redactions and their effect on reproduction.
