FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY servers/lme_price_mcp/ ./servers/lme_price_mcp/
COPY shared/ ./shared/
ENV MCP_TRANSPORT=sse
ENV MCP_PORT=8003
EXPOSE 8003
CMD ["python", "servers/lme_price_mcp/server.py"]
