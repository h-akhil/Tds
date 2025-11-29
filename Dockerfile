FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV QUIZ_SECRET=my_secret_key
ENV API_KEY=eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIzZjIwMDUzODdAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.O_yfwzUXpj2qMoeATWjA5MtqLD2YNAnZfww4Tw8jwX4

EXPOSE 8000
CMD ["python", "app.py"]
