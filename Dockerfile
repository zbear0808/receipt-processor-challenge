# # Build stage
# FROM python:3.12 AS builder

# WORKDIR /app/

# COPY requirements.txt ./
# RUN pip install --target /app/ --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.12-alpine

# WORKDIR /app

# COPY --from=builder /app/ /app/
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

EXPOSE 80

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]