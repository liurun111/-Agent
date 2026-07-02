FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY servers/mineral_pdf_mcp/ ./servers/mineral_pdf_mcp/
COPY shared/ ./shared/
ENV MCP_TRANSPORT=sse
ENV MCP_PORT=8002
EXPOSE 8002
CMD ["python", "servers/mineral_pdf_mcp/server.py"]
