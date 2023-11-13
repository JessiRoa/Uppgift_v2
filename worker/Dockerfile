FROM python:3.9-slim AS build
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ARG producer
COPY ${producer}.py ./worker.py   


FROM python:3.9-slim AS runtime
RUN adduser --disabled-password tucstudent
USER tucstudent
COPY --from=build /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=build --chown=tucstudent:tucstudent /app/worker.py ./worker.py
#ENV RAM_LIMITS    
#ENV CPU_LIMITS   

CMD ["python", "worker.py"]




