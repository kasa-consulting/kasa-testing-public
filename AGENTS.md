# Public results repository

KASA agents follow `kasa-consulting/kasa-platform` `workers/base-worker.md`,
including "Find skills without loading them". Reference that contract rather
than copying its rules or skill content here.

This repository holds reviewed results and evidence cleared for public release. Every
branch, pull request, attachment, and commit is public. Private draft preparation belongs
in the source repository.

Read README.md and CONTRIBUTING.md before adding a result. New reports belong in
`reports/<YYYY-MM-DD>-<subject>/`. Preserve the earlier `hardware/` investigations and
their evidence checksums. Do not import private Git history or copy an entire campaign.

State measurement dates, verdict, environment, exact versions and flags, reproduction
steps, failures, and limits. Separate measured values from predictions. Distinguish VM
and bare-metal measurements. Use public relative links for the evidence behind a claim.

Never add client data, credentials, gateway request or response bodies, private inventory,
unreviewed logs, model weights, or checkpoints. Review every selected file before pushing.
Automated checks do not establish permission to release content.

Run `python3 scripts/validate.py` before committing. CI uses GitHub-hosted runners with
read-only permissions and the required check name `KASA Validation`. Do not point public
pull requests at an internal runner or give them deployment credentials.
