FROM python:3.13-slim
WORKDIR /app
COPY app.py domain.py project.json ./
COPY static ./static
RUN useradd --uid 10001 --create-home appuser && mkdir /app/data && chown appuser /app/data
USER appuser
ENV HOST=0.0.0.0 PORT=8102 PYTHONUNBUFFERED=1
EXPOSE 8102
CMD ["python", "app.py"]
