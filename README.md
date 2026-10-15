# sonar-template-python

A deliberately tiny Python app for practising **local** SonarQube scans:
**terminal on the SonarQube Mac → ruff → pytest + coverage → pysonar → quality gate**.

This is the companion to [sonar-template](https://github.com/shanehowl/sonar-template) (React). The two repos test different ways of triggering a scan against the same self-hosted SonarQube:

| Repo | How the scan is triggered |
|---|---|
| `sonar-template` (React) | GitHub Actions, using a self-hosted runner on the SonarQube Mac |
| `sonar-template-python` (this repo) | You run `scripts/scan.sh` yourself on the SonarQube Mac. There's no CI. |

## Stack

| Area | Tools |
|---|---|
| App | Python 3.12+, standard library only (a `Counter` class, `greet()`, and a small CLI) |
| Packaging | [uv](https://docs.astral.sh/uv/) |
| Lint and tests | ruff; pytest + pytest-cov, which writes `coverage.xml` |
| Scanner | [pysonar](https://pypi.org/project/pysonar/), the official SonarScanner for Python. It's installed as a dev dependency and downloads its own JRE, so you don't need Java or Docker |
| Code quality | The SonarQube Community Build stack from `sonar-template/infra/sonarqube`, at `http://localhost:9000` |

## Local development

```bash
uv sync                         # creates .venv and installs dev tools
uv run sonar-template-python Ada --count 2
uv run ruff check .
uv run ruff format .
uv run pytest                   # also writes coverage.xml
```

## One-time setup on the SonarQube Mac

1. **Start SonarQube.** Use the stack from the React repo:

   ```bash
   cd ~/path/to/sonar-template && infra/sonarqube/setup.sh
   ```

   Check that `curl -s http://localhost:9000/api/system/status` returns `"status":"UP"`.
2. **Install uv** if you don't have it: `brew install uv`
3. **Clone this repo and install its dependencies:**

   ```bash
   git clone https://github.com/shanehowl/sonar-template-python.git
   cd sonar-template-python && uv sync
   ```

4. **Create the project in SonarQube.** At http://localhost:9000, go to **Create Project → Local project**:
   - Project display name: `sonar-template-python`
   - Project key: `sonar-template-python`. It must match `projectKey` in `pyproject.toml`.
   - Main branch: `main`
   - New code: **Previous version**, or whatever you used for the React project
5. **Create a token.** Choose **Locally** as the analysis method, then generate a **project analysis token**. Copy it now, because SonarQube only shows it once.
6. **Save the token** in a git-ignored `.env` file:

   ```bash
   cp .env.example .env
   # edit .env and set SONAR_TOKEN=sqp_...
   ```

## Run a scan

```bash
scripts/scan.sh
```

The script:

1. Loads `.env`.
2. Checks that SonarQube is `UP`.
3. Runs `ruff check` and `ruff format --check`.
4. Runs `pytest` with coverage, which writes `coverage.xml`.
5. Runs `uv run pysonar`, which reads `[tool.sonar]` in `pyproject.toml` and waits for the quality gate.

The script exits with a non-zero status if any step fails, including a failed quality gate (`qualitygate.wait = true`). That matches how the React pipeline fails its `sonar` job. Check it with `echo $?`.

If you don't want to use `.env`, pass the values inline:

```bash
SONAR_TOKEN=sqp_... SONAR_HOST_URL=http://localhost:9000 scripts/scan.sh
```

The results appear at http://localhost:9000/dashboard?id=sonar-template-python.

## Practice exercises

1. **Break the gate on coverage.** Add an untested module of 20+ lines under `src/sonar_template_python/`, then run `scripts/scan.sh`. The scan reports `QUALITY GATE STATUS: FAILED` and the script exits non-zero. Then revert the change.
2. **Break the gate on an issue.** Add a `# TODO` comment, or a function with an unused parameter, then rescan.
3. **Custom quality gate.** In SonarQube, copy "Sonar way", raise coverage on new code to 90%, assign the new gate to this project, then rescan.
4. **Rotate the token.** Generate a new token, put it in `.env`, rescan, then revoke the old token.
5. **SonarQube offline.** Stop the stack, then run `scripts/scan.sh`. It fails fast at the status check.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `SonarQube is not UP` | The stack is stopped or still starting | Run `infra/sonarqube/setup.sh` in the React repo and wait for it to finish |
| `Not authorized` / HTTP 401 | The token is wrong, revoked, or for another project | Generate a new project analysis token for `sonar-template-python` |
| Coverage shows 0% | `coverage.xml` is missing, or its paths don't match | Run `uv run pytest` first. Paths are repo-relative because of `relative_files = true` |
| `QUALITY GATE STATUS: FAILED` | The gate did its job | Open the dashboard link printed in the output |

## Known limitations

- SonarQube Community Build analyses one branch only. Scan from `main`.
- pysonar downloads a JRE and the scanner engine to `~/.sonar` the first time it runs. Later runs use that cache.
