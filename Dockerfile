FROM python:3.9-slim

# Working directory
WORKDIR /usr/src/app
COPY . /usr/src/app

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Run
CMD ["python", "./bot.py"]
