FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY servers/mining_news_mcp/ ./servers/mining_news_mcp/
COPY shared/ ./shared/
ENV MCP_TRANSPORT=sse
ENV MCP_PORT=8001
EXPOSE 8001
CMD ["python", "servers/mining_news_mcp/server.py"]
