## Deterministic script registry

These workspace files are canonical. Do not reimplement their logic in a
prompt. Do not use Kestrel for work that `linkedin_source.py` can do.

| Script                               | Run when                               | Required output                                                             | Exit status                                                                            |
| ------------------------------------ | -------------------------------------- | --------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| `scripts/linkedin_source.py`         | Hunt source phase                      | `events.jsonl`, live `preflight.jsonl`, evidence files, `run.complete.json` | `0` complete, `1` one or more portal workers failed, `2` invalid input or runner error |
| `scripts/cache_linkedin_identity.py` | Once in hunt assemble                  | One immutable hunt-level LinkedIn identity JSON                             | `0` cached, `2` auth, profile, input, or portal failure                                |
| `scripts/resume_gate.py`             | After Quill and before Sieve           | Deterministic gate JSON, reduced review packet, gate sentinel               | `0` PASS, `1` blocked by a deterministic check, `2` gate could not run                 |
| `scripts/worker_sentinel.py`         | At the end of each Quill or Sieve task | Atomic task sentinel that names non-empty artifacts                         | `0` valid, `2` absent, empty, mismatched, or invalid                                   |

Validate the source plan before every hunt:

```
cd ~/career
python3 scripts/linkedin_source.py \
  --config scripts/linkedin-source.example.json plan
```

Run the source phase with a new output directory:

```
python3 scripts/linkedin_source.py \
  --config scripts/linkedin-source.example.json run \
  --output-dir state/source-<hunt-id>
```

Cache identity once before the first application:

```
python3 scripts/cache_linkedin_identity.py \
  --portal "Profile Check" \
  --profile-url "https://www.linkedin.com/in/queiroz-lucas/" \
  --output state/<hunt-id>-linkedin-identity.json
```

Run the deterministic application gate before Sieve:

```
python3 scripts/resume_gate.py \
  --base resumes/base-<base-lang>.tex \
  --tailored resumes/hunts/<hunt-id>/<application>/Lucas-Queiroz-Resume-<lang>.tex \
  --pdf resumes/hunts/<hunt-id>/<application>/Lucas-Queiroz-Resume-<lang>.pdf \
  --posting jobs/<application>.md \
  --manifest state/<application>-manifest.json \
  --identity-cache state/<hunt-id>-linkedin-identity.json \
  --claim-allowlist claim-allowlist.json \
  --report state/<application>-deterministic-gate.json \
  --review-packet state/<application>-review-packet.md \
  --sentinel state/<application>-deterministic-gate.complete.json
```

Use `base-lang=en` when the posting language is Spanish. Use the posting
language for every tailored output name and for the application manifest.

Quill and Sieve create and the Maestro verifies their task sentinels:

```
python3 scripts/worker_sentinel.py write \
  --path state/<task>.complete.json \
  --task-id <task-id> --status complete \
  --artifact <required-artifact> [--artifact <required-artifact>]
python3 scripts/worker_sentinel.py verify \
  --path state/<task>.complete.json --task-id <task-id>
```

