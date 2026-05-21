# interrogating-agents

ECS 172 group project. A RAG-guided LLM "interrogator" that nudges another LLM's stance during multi-turn debate on non-partisan topics. Evaluation is LLM-vs-LLM (control vs treatment) with a blinded judge LLM scoring stance ∈ [−2, 2] per turn.

The project runs entirely against local Ollama models, so no API costs and unlimited eval trials.

## Install

### macOS

```bash
brew install ollama
ollama serve &              # or launch the Ollama app
git clone https://github.com/mawroblewski1/interrogating-agents.git
cd interrogating-agents
python -m venv .venv && source .venv/bin/activate
python scripts/setup.py
```

### Linux

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama serve &
git clone https://github.com/mawroblewski1/interrogating-agents.git
cd interrogating-agents
python -m venv .venv && source .venv/bin/activate
python scripts/setup.py
```

### Windows (PowerShell)

```powershell
# Install Ollama from https://ollama.com/download
Start-Process "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" -ArgumentList "serve" -WindowStyle Hidden
git clone https://github.com/mawroblewski1/interrogating-agents.git
cd interrogating-agents
python -m venv .venv
.venv\Scripts\Activate.ps1
python scripts/setup.py
```

`scripts/setup.py` installs the Python requirements, locates the Ollama binary on any OS, pulls `llama3.1:8b`, and runs the fast (no-LLM) test subset.

## Run a single trial

```bash
python -m src.trial --topic housing_prop_123 --direction -2 --condition control --n_turns 3
```

## Run a small experiment sweep

```bash
python -m src.experiment --topic housing_prop_123 --n_quads 1 --condition control
```

Outputs land under `output/` as `transcripts_<ts>.jsonl`, `trials_<ts>.csv`, `quads_<ts>.csv`.

## Run the test suite

```bash
python -m pytest -v                  # full suite (requires Ollama)
python -m pytest -m "not slow" -v    # fast subset (no Ollama, ~10 tests, <1s)
```

Slow tests are LLM-integration tests; they auto-skip when no Ollama binary is found, so the fast subset is what CI runs.

## Project layout

- `src/llm.py` — Ollama HTTP wrapper
- `src/roles/` — Suspect, Interrogator, Judge prompt logic
- `src/trial.py` — single-trial runner (suspect ↔ interrogator, judge scores per turn)
- `src/quad.py` — 4-leg quad (alternating ±2 directions, batched judge)
- `src/experiment.py` — sweep CLI, CSV/JSONL outputs
- `src/metrics.py` — magnitude, direction, consistency
- `scripts/ollama_runtime.py` — cross-OS Ollama binary discovery
- `scripts/setup.py` — one-command bootstrap
- `docs/PORTABILITY.md` — what made the M1+M2 code Windows-only and what changed

## Status

- ✅ M1: roles + single-trial runner
- ✅ M2: quad structure, metrics, experiment CLI, smoke tests
- ⏳ M3: RAG corpus (technique cards + ChromaDB index)
- ⏳ M4: treatment interrogator (2-stage select → apply pipeline)
- ⏳ M5: evaluation write-up
