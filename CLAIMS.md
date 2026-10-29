# Claims and evidence

Every line in the "receipts" terminal on my profile, and where to check it.

The terminal image is a rendered summary, not a CI run. This file is the part you can verify.

## Public: check it yourself

| Claim | Evidence |
|---|---|
| agent-triage ships on PyPI | [pypi.org/project/agent-triage](https://pypi.org/project/agent-triage/) · [repo](https://github.com/thebharathkumar/agent-triage) (220+ tests, 93%+ coverage per its README) |
| faramesh PR #33 merged | [faramesh/faramesh-core#33](https://github.com/faramesh/faramesh-core/pull/33): wires delegation tokens into runtime policy evaluation |
| 0 of 4 MCP OpenTelemetry libraries ship the spec's MCP histograms | [mcp-otel-audit](https://github.com/thebharathkumar/mcp-otel-audit): reproducible audit and [writeup](https://github.com/thebharathkumar/mcp-otel-audit/blob/main/docs/blog/auditing-mcp-otel.md) |
| Springer Nature 2023 | [ICACECS 2023 proceedings, Atlantis Press (a Springer Nature imprint)](https://www.atlantis-press.com/proceedings/icacecs-23/125995742). Corresponding author |

## Private: production work, not public

These come from the multi-agent platform I built and operated as a Graduate Assistant at Pace University (LangGraph + Claude on Amazon Bedrock). It answers students' questions and helps them choose courses, grounded in their own records. The code and dashboards are not public. My supervisor can confirm them as a reference on request.

| Claim | Context |
|---|---|
| 10K+ daily users | Production traffic on the Pace platform |
| 99.5% uptime | Same system, monitored with OpenTelemetry and Grafana |
| 12 zero-regression releases | Release evaluations gated every deploy |
| 0.92 MRR@5 over 50K+ documents | Retrieval quality on the platform's RAG pipeline |
| 4 silent regressions caught before users | Caught by the release eval harness (200+ tests per release) |

## The rule behind "no fabricated metrics"

- A public number links to the repo file that produced it.
- A private number is labeled private, with the context it came from.
- A weak result is published as weak. [loopcheck](https://github.com/thebharathkumar/loopcheck) reports recall 0.33 on a 15-file seed set, and says 15 files is too small to estimate it reliably.

If you find a number on this profile that does not trace back to one of these, tell me: [bharath.kr702@gmail.com](mailto:bharath.kr702@gmail.com).
