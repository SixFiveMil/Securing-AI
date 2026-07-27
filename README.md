# AI Hardening Sandbox

AI Hardening Sandbox is a local cybersecurity lab for teaching LLM prompt-injection defenses through hands-on Red Team and Blue Team exercises. The repository is built around Docker Desktop, Ollama, and a Python-based security gateway so students can observe how model behavior changes across vulnerable, hardened, and filtered setups.

## Architecture

The lab uses three layers:

1. **Docker Desktop** runs the full stack locally and keeps the environment reproducible for classrooms and workshops.
2. **Ollama** provides the model runtime on port `11434` and stores model data in the persistent `ollama_storage` volume.
3. **secure_gateway.py** runs as the Python web service on port `5000`, talks to Ollama through the Compose network, and demonstrates basic ingress and egress filtering.

The Compose file wires the services together so the gateway can reach Ollama by service name instead of relying on host-specific configuration.

## Quickstart

From the repository root:

```bash
docker compose up -d
```

Initialize the local models after the stack is running:

The Ollama container is named `llm`, so direct commands like `docker exec -it llm ...` work as well.

```bash
docker compose exec llm ollama pull llama3

docker compose exec llm ollama create vulnerable_bot -f /app/lab/modelfiles/vulnerable.txt
docker compose exec llm ollama create hardened_bot -f /app/lab/modelfiles/hardened.txt
```

To run the gateway locally on the host instead of through Docker, use:

```bash
python lab/scripts/secure_gateway.py
```

## Classroom Use

Clark Center instructors and students can use the included assignment materials for the two main lab tracks:

- [Red Team Engagement](docs/assignments/RedTeam_Engagement_ClarkCenter.docx)
- [Blue Team Response](docs/assignments/BlueTeam_Response_ClarkCenter.docx)

These documents are intended to support guided walkthroughs, team exercises, and validation of prompt-injection defenses during class sessions.

## Troubleshooting

- If `docker compose up -d` succeeds but Ollama does not answer, confirm Docker Desktop is running and check `docker compose logs llm`.
- If the gateway cannot reach Ollama, confirm the published port is `11434` and that the `llm` service is healthy enough for the model pull.
- If model creation fails, make sure the Modelfiles were copied into the container before running `ollama create` and that the filenames match exactly.
- If the Python service exits immediately, confirm you are running it from the repository root so `lab/scripts/secure_gateway.py` can be found.

## Cleanup

Stop the stack and remove the persistent data when you want a fresh lab environment:

```bash
docker compose down -v
```

If you want to remove just the Ollama volume, delete the Compose-managed `ollama_storage` volume explicitly with `docker volume rm securing-ai_ollama_storage` after checking `docker volume ls`.
