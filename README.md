# AI Hardening Sandbox

AI Hardening Sandbox is a local cybersecurity lab for teaching LLM prompt-injection defenses through hands-on Red Team and Blue Team exercises. The repository is built around Docker Desktop, Ollama, and a Python-based security gateway so students can observe how model behavior changes across vulnerable, hardened, and filtered setups.

## Architecture

The lab runs as a two-service Docker stack defined in `docker-compose.yml`:

1. **`llm`** runs Ollama on port `11434` and stores model data in the persistent `ollama_storage` volume.
2. **`web`** runs the Python Flask gateway on port `5000`, installs the app dependencies at startup, and reaches Ollama via `OLLAMA_HOST=http://llm:11434` on the Compose network.

The gateway logic lives in `lab/scripts/secure_gateway.py`; it is started by the `web` container command in Compose and is not intended to be run manually in the normal Docker-first lab flow.

## Quickstart

From the repository root, start the Docker stack:

```bash
docker compose up -d
```

The app is then available in a browser at `http://localhost:5000`. In the Compose stack, the `web` service runs the Flask app automatically; it is not a separate manual step.

After the services come up, the stack is ready to use. In the current Compose setup, the model pull and the two lab model registrations are part of the local Ollama workflow you can run manually as needed, but they are not required as a separate startup step for the default web app to be reachable.

If you need to create or refresh the models explicitly, use:

```bash
docker compose exec llm ollama pull llama3.2

docker compose exec llm ollama create vulnerable_bot -f /app/lab/modelfiles/vulnerable.txt
docker compose exec llm ollama create hardened_bot -f /app/lab/modelfiles/hardened.txt
```

Optional: for host-side debugging only, you can run the gateway directly from the repo instead of using the Docker `web` container:

```bash
python lab/scripts/secure_gateway.py
```

> The Docker path is the active default for the lab. `docker-compose.yml` handles the container startup and dependency installation automatically.

## Classroom Use

The sandbox is built around a single scenario: "Piper," a customer-support chatbot for a
fictional credit union, available in an unhardened build (`vulnerable_bot`) and a
system-prompt-hardened build (`hardened_bot`). Both sit behind the same gateway, which students
can route traffic through — or around — to compare defense layers directly.

Clark Center instructors and students can use the included assignment materials for the two main
lab tracks:

- [Red Team Engagement](docs/assignments/RedTeam_Engagement_ClarkCenter.docx)
- [Blue Team Response](docs/assignments/BlueTeam_Response_ClarkCenter.docx)
- [Setup Guide](lab/SETUP_GUIDE.md) — step-by-step install and quick-reference card for either lesson

These documents are intended to support guided walkthroughs, team exercises, and validation of
prompt-injection defenses during class sessions. Maps to OWASP GenAI/LLM Top 10 (2026): LLM01
Prompt Injection, LLM02 Sensitive Information Disclosure, and LLM08 Hidden Context Exposure.

## Troubleshooting

- If `docker compose up -d` succeeds but Ollama does not answer, confirm Docker Desktop is running and check `docker compose logs llm`.
- If the browser gateway cannot reach Ollama, confirm the `llm` service is healthy and that the Docker network is using `OLLAMA_HOST=http://llm:11434` as configured in `docker-compose.yml`.
- If the host-only gateway script cannot connect, confirm the published port is `11434` and that the Ollama service is listening on the host port before using `http://localhost:11434`.
- If model creation fails, confirm `docker compose exec llm ls /app/lab/modelfiles` shows both files — they arrive automatically via the volume mount, so this usually means the repo wasn't cloned/unzipped correctly rather than a missing copy step.
- If the Python service exits immediately, confirm you are running it from the repository root so `lab/scripts/secure_gateway.py` can be found.
- If a model rejects the reasoning option with `does not support thinking`, the gateway will retry without the `think=True` flag automatically; this is expected for some Ollama models.

## Cleanup

Stop the stack and remove the persistent data when you want a fresh lab environment:

```bash
docker compose down -v
```

If you want to remove just the Ollama volume, delete the Compose-managed `ollama_storage` volume explicitly with `docker volume rm securing-ai_ollama_storage` after checking `docker volume ls`.