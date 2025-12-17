########################################
############## API Image ###############
########################################
FROM python:3.12

WORKDIR /srv/app

# Copy the Python source files into the container
COPY ./src ./src

# Copy the Python pip requuirements into the container
COPY ./requirements.txt ./requirements.txt

# Install Python dependencies
RUN python3 -m pip install --upgrade pip && python3 -m pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

USER 1000:1000

CMD ["python", "-m uvicorn --host 0.0.0.0 --port 8000 --root-path / --log-level info --access-log --proxy-headers dnsmin.api:app"]
