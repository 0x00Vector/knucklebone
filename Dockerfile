FROM python:3.12-slim

# 1. Best Practices Env Vars
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DB_PATH=/app/data/bot.db

WORKDIR /app

# 2. Install Deps (Cached Layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Create Data Directory & User
# We do this before switching users so we can assign permissions
RUN mkdir -p /app/data && \
    useradd -m botuser && \
    chown -R botuser:botuser /app/data

# 4. Copy Code
COPY bot/ ./bot/

# 5. Switch to Non-Root
USER botuser

# 6. Run (Exec Form)
# Ensure your script reads os.getenv('DISCORD_TOKEN') internally!
CMD ["python", "-m", "bot.main"]
