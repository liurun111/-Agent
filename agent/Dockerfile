FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/
COPY shared/ ./shared/
ENV NEWS_MCP_HOST=mining-news
ENV PDF_MCP_HOST=mineral-pdf
ENV PRICE_MCP_HOST=lme-price
ENV OPENAI_API_KEY=sk-placeholder
ENV OPENAI_BASE_URL=https://api.openai.com/v1
ENV LLM_MODEL=gpt-4o
ENTRYPOINT ["python", "agent/react_agent.py"]
