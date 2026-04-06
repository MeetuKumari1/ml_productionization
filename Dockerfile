FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN mkdir -p artifacts
RUN sed -i 's/\r$//' start.sh && chmod +x start.sh

EXPOSE 5000

CMD ["./start.sh"]
