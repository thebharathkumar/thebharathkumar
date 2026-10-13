<p align="right">
  <img src="https://komarev.com/ghpvc/?username=thebharathkumar&label=profile%20views&style=flat-square&color=7C6CF2" alt="Profile views" />
</p>

<a href="./scripts/status_page.py">
  <img src="./assets/status.svg" width="100%" alt="Live status page for Bharath Kumar Rajesh: contributions over the last 12 months, CI state and last ship date for ten repos, regenerated daily from the GitHub API." />
</a>

<p align="center"><sub>☝️ This board is not a screenshot. A <a href="./.github/workflows/status.yml">GitHub Action</a> rebuilds it every day from the GitHub API. An observability engineer's profile should be observable.</sub></p>

<table>
<tr>
<td width="62%" valign="top">

**Looking for:** AI Engineer · Applied AI Engineer · Forward Deployed Engineer<br/>
**Based in:** New York City, open to relocation · F-1 OPT<br/>
**Education:** M.S. Computer Science, Pace University, GPA 3.87<br/>
**Reach me:** [bharath.kr702@gmail.com](mailto:bharath.kr702@gmail.com) · [thebharath.co](https://thebharath.co) · [LinkedIn](https://linkedin.com/in/thebharathkumar)

</td>
<td width="38%" valign="top">

**Shipped in production**<br/>
Multi-agent platform, LangGraph + Claude on Bedrock<br/>
**10K+** daily users · **99.5%** uptime<br/>
**0.92** MRR@5 over **50K+** docs<br/>
**4** silent regressions caught before users

</td>
</tr>
</table>

## ✅ The receipts

<p align="center">
  <img src="./assets/terminal.svg" width="100%" alt="pytest run over verified claims: 10K daily users, 99.5% uptime, 12 zero-regression releases, 0.92 MRR@5 over 50K docs, 4 silent regressions caught, agent-triage on PyPI, faramesh PR 33 merged, 0 of 4 MCP libraries ship the spec histograms, Springer Nature 2023, no fabricated metrics. 10 passed, 0 fabricated." />
</p>

## 🔦 Start here

<table>
<tr>
<td width="33%" valign="top">

### [agent-triage](https://github.com/thebharathkumar/agent-triage)
Ranks multi-agent failures by severity, frequency, and recovery from OpenTelemetry or NDJSON traces.

`pip install agent-triage`

**On PyPI · 220+ tests · 93%+ coverage**

</td>
<td width="33%" valign="top">

### [mcp-otel-audit](https://github.com/thebharathkumar/mcp-otel-audit)
A reproducible audit of 4 MCP OpenTelemetry libraries. **None of them ship the spec's MCP histograms.**

**A maintainer of Logfire and the MCP Python SDK responded publicly.**

</td>
<td width="33%" valign="top">

### [ForgeSync](https://github.com/thebharathkumar/ForgeSync)
Financial reconciliation infra with explainable matching and human-approved write-back.

**125 unit + 75 integration tests on real Postgres and Redis. Scoring runs ~25x faster than ingestion.**

</td>
</tr>
</table>

## 🧪 House rules

1. **Every number comes from a file the code wrote.** [ForgeSync](https://github.com/thebharathkumar/ForgeSync) commits the report behind every benchmark.
2. **Thresholds are fixed before the results.** [downgrade](https://github.com/thebharathkumar/downgrade) refuses to load runs whose settings were edited afterwards.
3. **Weak results are published as weak.** [loopcheck](https://github.com/thebharathkumar/loopcheck) reports recall 0.33. [gcf-virome](https://github.com/thebharathkumar/gcf-virome) reports a null result as null.
4. **Demos run offline in seconds, no API key.** `loopcheck demo` · `claimtrace demo` · `python3 -m estimate_check demo`
5. **Say what I don't know.** [estimate-check](https://github.com/thebharathkumar/estimate-check) has a section called "What I do not know".

<details>
<summary><b>🧭 The full reliability stack</b> (how the repos fit together)</summary>
<br/>

```mermaid
flowchart LR
    subgraph B["① Build"]
        LC["loopcheck<br/>verifier-first agent loop"]
        CT["claimtrace<br/>every claim traced to a char span"]
        OD["obindoc<br/>cited, verified RAG"]
    end
    subgraph R["② Route"]
        CF["costfloor<br/>cheapest model, no regression"]
        DG["downgrade<br/>catches router quality loss"]
    end
    subgraph O["③ Observe"]
        AT["agent-triage<br/>ranks failures from traces"]
        FR["agent-flight-recorder<br/>audit + tracing skills"]
        SM["super-mcp-eval<br/>evals for MCP servers"]
        MO["mcp-otel-audit<br/>OTel semconv audit"]
    end
    subgraph F["④ Fix"]
        RX["agent-rx<br/>proposes and A/B-tests fixes"]
    end
    B --> R --> O --> F
    F -. lessons .-> B

    classDef build fill:#1e1b4b,stroke:#7C6CF2,color:#e6edf3
    classDef route fill:#1c1917,stroke:#F59E0B,color:#e6edf3
    classDef observe fill:#052e2b,stroke:#10B981,color:#e6edf3
    classDef fix fill:#3b0a24,stroke:#EC4899,color:#e6edf3
    class LC,CT,OD build
    class CF,DG route
    class AT,FR,SM,MO observe
    class RX fix
```

| Project | What it does | Proof |
|---|---|---|
| [**loopcheck**](https://github.com/thebharathkumar/loopcheck) | Should you trust that the agent actually finished? Mutation-tested verification, calibrated confidence, HMAC-chained audit log. | 86 tests · precision 1.00 / recall 0.33 on a 15-file seed set |
| [**claimtrace**](https://github.com/thebharathkumar/Claimtrace) | Five-node LangGraph pipeline. Every claim points to an exact source chunk and character span, and contradicting sources get flagged. | Byte-flip tamper test on the audit chain |
| [**downgrade**](https://github.com/thebharathkumar/downgrade) | Measures silent quality loss when a model router downgrades a request. | Sequential tests, SPRT, Benjamini-Hochberg, Kupiec and Christoffersen backtests |
| [**costfloor**](https://github.com/thebharathkumar/costfloor) | Finds the cheapest model that does not silently break your agent. | 47 tests · CI on Python 3.11 and 3.12 |
| [**agent-flight-recorder**](https://github.com/thebharathkumar/agent-flight-recorder) | Claude Code plugin: hash-chained audit logs, OTel tracing, eval scaffolds, trace triage. | 90% coverage gate in CI |
| [**agent-rx**](https://github.com/thebharathkumar/agent-rx) | Diagnoses agent failures, proposes fixes, A/B-tests them. | Python · MIT |
| [**super-mcp-eval**](https://github.com/thebharathkumar/super-mcp-eval) | Eval harness for MCP servers: schema compliance, tool-selection accuracy. | Wilson 95% CIs |
| [**obindoc**](https://github.com/thebharathkumar/obindoc) | Grounded RAG with span-level citations and a verifier loop. | Under 900 lines · 29 tests |

</details>

<details>
<summary><b>🔬 Same rigor, other domains</b> (bioinformatics, insurance, vision, wearables)</summary>
<br/>

| Project | What makes it worth a look |
|---|---|
| [**gcf-virome**](https://github.com/thebharathkumar/gcf-virome) | One-command Snakemake pipeline on public periodontal metagenomes. Reports its null result as null, then runs its own host-depletion follow-up. 40 tests on a REDCap / NCBI metadata validator. |
| [**estimate-check**](https://github.com/thebharathkumar/estimate-check) | Deterministic verifier for restoration estimates. Six detectors, zero runtime dependencies. Its optional LLM judge can annotate findings but never change them. |
| [**vehicle-damage-detection**](https://github.com/thebharathkumar/vehicle-damage-detection) | YOLO11s-seg on CarDD: 0.753 mask mAP50 held out, with ablation, error analysis, and a robustness suite. |
| [**streamsense**](https://github.com/thebharathkumar/streamsense) | CNN + transformer activity recognition on PAMAP2, ONNX export, int8 quantization. |

</details>

## 📚 Research publications

<table>
<tr>
<td width="50%" valign="top">

#### A Deep CNN Approach for Identifying Medicinal and Edible Plants in the Western Ghats
<a href="https://www.atlantis-press.com/proceedings/icacecs-23/125995742"><img src="https://img.shields.io/badge/Springer_Nature-ICACECS_2023-b31b1b?style=flat-square" alt="ICACECS 2023, Springer Nature" /></a>

Deep CNN that identifies medicinal and edible plant species from the Western Ghats, at **89% accuracy**. *Corresponding author.*

</td>
<td width="50%" valign="top">

#### Driver Drowsiness Detection using AI
<a href="https://www.ijaresm.com/sahasransu-mohanty"><img src="https://img.shields.io/badge/IJARESM-Vol_11_·_Nov_2023-43853D?style=flat-square" alt="IJARESM, Nov 2023" /></a>

Real-time fatigue detection from facial landmarks and eye aspect ratio, using Dlib plus a Keras CNN, shipped as an Android app.

</td>
</tr>
</table>

## 📜 Certifications

<p>
  <img src="https://img.shields.io/badge/Anthropic-Building_with_Claude_on_Amazon_Bedrock-D97757?style=for-the-badge&logo=anthropic&logoColor=white" alt="Anthropic: Building with Claude on Amazon Bedrock" />
  <img src="https://img.shields.io/badge/AWS-Solutions_Architect_Associate-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white" alt="AWS Solutions Architect Associate" />
  <img src="https://img.shields.io/badge/Red_Hat-RHCSA-EE0000?style=for-the-badge&logo=redhat&logoColor=white" alt="Red Hat Certified System Administrator" />
</p>

## 🔁 Open source

- [**faramesh/faramesh-core**](https://github.com/faramesh/faramesh-core) (Go, AI agent governance): authored 9 PRs. Merged [#33](https://github.com/faramesh/faramesh-core/pull/33), which wires delegation tokens into runtime policy evaluation.
- [**agent-triage**](https://pypi.org/project/agent-triage/): my own package, published on PyPI.

## 🛠️ Tech stack

<p>
  <img src="https://skillicons.dev/icons?i=py,ts,go,cpp,react,nodejs,fastapi,pytorch,tensorflow,postgres,mongodb,redis,elasticsearch,kafka,docker,kubernetes,aws,azure,gcp,terraform,linux&perline=11" alt="Python, TypeScript, Go, C++, React, Node.js, FastAPI, PyTorch, TensorFlow, Postgres, MongoDB, Redis, Elasticsearch, Kafka, Docker, Kubernetes, AWS, Azure, GCP, Terraform, Linux" />
</p>

| Area | Tools |
|---|---|
| **AI / LLM** | Claude, Amazon Bedrock, OpenAI, LangGraph, LangChain, MCP, OpenTelemetry (GenAI semconv), RAG, LLM evals, Hugging Face |
| **ML** | PyTorch, TensorFlow, Keras, scikit-learn, OpenCV, YOLO, ONNX |
| **Backend** | FastAPI, Fastify, Node.js, Prisma, Zod, BullMQ |
| **Data** | PostgreSQL, Redis, MongoDB, Elasticsearch, Kafka, DuckDB |
| **Cloud / Infra** | AWS (incl. CDK), Azure, GCP, Docker, Kubernetes, Terraform, Linux |
| **Testing** | pytest, Vitest, Playwright, mutation testing |
| **Science** | Snakemake, R (vegan), bowtie2, samtools |

## 🤝 Let's connect

<p align="center">
  <a href="https://thebharath.co"><img src="https://img.shields.io/badge/Portfolio-7C6CF2?style=for-the-badge&logo=safari&logoColor=white" alt="Portfolio" /></a>
  <a href="https://linkedin.com/in/thebharathkumar"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" /></a>
  <a href="mailto:bharath.kr702@gmail.com"><img src="https://img.shields.io/badge/Email-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Email" /></a>
  <a href="https://medium.com/@thebharathkumar"><img src="https://img.shields.io/badge/Medium-000000?style=for-the-badge&logo=medium&logoColor=white" alt="Medium" /></a>
  <a href="https://twitter.com/passdweed"><img src="https://img.shields.io/badge/X-000000?style=for-the-badge&logo=x&logoColor=white" alt="X" /></a>
  <a href="https://open.spotify.com/show/4PDEqJu1u06pqcvBFF4BRA"><img src="https://img.shields.io/badge/Podcast-1DB954?style=for-the-badge&logo=spotify&logoColor=white" alt="Podcast" /></a>
  <a href="https://instagram.com/bharath.kr_10"><img src="https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white" alt="Instagram" /></a>
</p>

<p align="center"><sub>Writing: <a href="https://github.com/thebharathkumar/mcp-otel-audit/blob/main/docs/blog/auditing-mcp-otel.md">Auditing MCP OpenTelemetry instrumentations</a> · more on <a href="https://medium.com/@thebharathkumar">Medium</a><br/>Fun fact: I can solve a Rubik's cube in under 2 minutes.</sub></p>
