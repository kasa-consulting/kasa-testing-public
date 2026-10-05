# Publishing a result

Prepare drafts and review source evidence in the private measurement repository. Push
only the selected files cleared for public release. A public pull request already exposes
its contents, even before it merges. Keep private repository history out of this repository.

## Report bundle

Use `reports/<YYYY-MM-DD>-<subject>/`, with the date of the first measurement in that
report. Keep an earlier report's date when adding a correction; record the revision and
the dates of new measurements in the report.

Each bundle contains:

- `report.md`, based on [the template](templates/report.md).
- `data/` for reviewed tables and machine-readable measurements used by the report.
- `figures/` for charts and their reproduction code, if needed.
- `scripts/` for the exact test procedure or links to a public, pinned revision.
- `SHA256SUMS`, covering every other file in the bundle.

Include only the folders the report needs. Use relative links so the report, charts, and
data remain readable in a checkout. Record source revisions and harness hashes for
provenance; evidence needed to check a claim must be available publicly. A private store
receipt alone does not give readers the evidence.

For each comparison, state the hardware, execution mode, software and model revisions,
flags, workload, repetitions, aggregation, and measurement boundary. Identify changes
between configurations. Include failed configurations and quality-screen failures. Label
predictions and estimates, and say what the tests did not establish.

## Release review

The person publishing the bundle checks its selected contents before pushing:

- Every number agrees with its cited evidence, and charts can be regenerated.
- The evidence contains synthetic test inputs and no client data, secrets, private
  inventory, gateway captures, or unreviewed logs. Remove internal links and paths.
- Reproduction steps name every dependency and warn when an experiment changes the host.
- The report includes its limitations and the conditions under which its result applies.
- The bundle's checksums cover every file, and the published-results index links to it.

To create a manifest, run `sha256sum` from inside the bundle with an explicit list of all
its files except `SHA256SUMS`, using paths relative to that directory. For example:

```sh
sha256sum report.md data/results.csv > SHA256SUMS
```

Then run `python3 scripts/validate.py` from the repository root and open a pull request.
Use squash merging after `KASA Validation` passes and review conversations are resolved.
CI checks file integrity and common accidental disclosures. A person still has to review
the content and authorize its release.

For a correction, explain which result changed and why. Preserve the earlier measurement
and identify a new run separately rather than silently replacing its configuration.

Maintainers can check [the repository settings record](docs/repository-settings.md) when
reviewing CI or access changes.
