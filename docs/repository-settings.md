# Repository settings

Configured and verified on 2026-10-05. This repository already existed with a public
Thunderbolt investigation; configuration preserved that investigation and its checksums.

| Area | Configuration |
| --- | --- |
| Visibility and default branch | Public, `main` |
| Ownership | `platform-maintainers` team, maintain access and CODEOWNERS |
| Merge method | Squash only; delete head branches after merging |
| Default branch | Organization protection requires a pull request, resolved review threads, linear history, and an up-to-date `KASA Validation` check; deletion and force pushes are blocked |
| Features | Issues and projects enabled; wiki and discussions disabled |
| Actions | GitHub-hosted Ubuntu 24.04; checkout pinned to a commit; five-minute job timeout |
| Workflow permissions | Read-only; workflows cannot approve pull requests; checkout does not persist credentials |
| External pull requests | Workflow approval required for all external contributors |
| Security | Secret scanning, non-provider secret patterns, and push protection enabled; Dependabot security updates enabled |

The inherited default-branch rule requires no approving-review count. CODEOWNERS identifies
the responsible team; it does not enforce a separate code-owner approval. Public content
must be cleared before pushing, as described in [CONTRIBUTING.md](../CONTRIBUTING.md).

Repository setup publishes these instructions and checks. It does not export private
campaigns or approve a draft report for release. Each result needs its own reviewed bundle.
