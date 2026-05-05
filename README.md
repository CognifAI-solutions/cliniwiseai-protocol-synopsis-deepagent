# CliniwiseAI Protocol Synopsis DeepAgent

LangGraph DeepAgent service for protocol synopsis workflows.

## Prerequisites

- Python 3.11+ (recommended)
- [`uv`](https://github.com/astral-sh/uv)
- Docker + Docker Compose
- LangGraph CLI (`langgraph`)

## Environment Setup

1. Copy the environment template:

```bash
cp .env.example .env
```

2. Fill in all values in `.env`.

Required variables are listed in `.env.example`:

- `AZURE_OPENAI_API_KEY`
- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_DEPLOYMENT`
- `TAVILY_API_KEY`
- `LANGSMITH_API_KEY`
- `LANGSMITH_TRACING`
- `DB_URI`
- `CLERK_SECRET_KEY`

## Install Dependencies (uv)

Run dependency installation with `uv`:

```bash
uv sync
```

## Run Locally (LangGraph Dev)

Start the local development server:

```bash
langgraph dev
```

## Build Docker Image

Build the LangGraph image:

```bash
langgraph build -t <image-name>
```

Replace `<image-name>` with your actual image tag.

## Run with Docker Compose

Run Compose using the built image:

```bash
IMAGE_NAME=<image-name> docker compose up
```

You can append `-d` to run in detached mode:

```bash
IMAGE_NAME=<image-name> docker compose up -d
```

## Post-Deployment Troubleshooting

For server/runtime issues after deployment, refer to:

- `cursor_langchain_deepagent_server_error.md`

## Deploy to Azure Container Apps.

Build the LangGraph image:

```bash
langgraph build -t synopsis-agent
```

Login to the container registry
```
az acr login --name cliniwiseprotocolagent
```

Tag docker image

```
docker tag synopsis-agent cliniwiseprotocolagent.azurecr.io/synopsis-agent
```

Push docker image

```
 docker push cliniwiseprotocolagent.azurecr.io/synopsis-agent
```

Create a new revision in the container app **protocol-deep-agent**

Add env variables from the .env.example. Add the following additional env variables

```
DATABASE_URI=<same as DB_URI value>
REDIS_URI
```

