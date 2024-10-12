FROM python:3.11.8-slim-bookworm

EXPOSE 8002

WORKDIR /app
COPY ../requirements.txt requirements.txt
# See Datadog Static Analysis -- https://docs.datadoghq.com/code_analysis/static_analysis_rules/docker-best-practices/pip-pin-versions/
RUN python3 -m pip install --upgrade pip==24.2 && python3 -m pip install --no-cache-dir -r requirements.txt
COPY . .
ENV RUNNING_IN_FUNCTION=true

RUN useradd appuser && chown -R appuser /app
USER appuser

CMD exec gunicorn -b :8002 --workers 1 --threads 8 --timeout 0 app:app