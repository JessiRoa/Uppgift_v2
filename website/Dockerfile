FROM python:3.9-slim AS build
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


FROM python:3.9-slim AS runtime
WORKDIR /app
COPY --from=build /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY . .
RUN adduser --disabled-password tucstudent
USER tucstudent
ENV PORT 80


CMD [ "python", "server.py" ]
