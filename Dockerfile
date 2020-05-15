# Use an official Python runtime as a parent image
#FROM frolvlad/alpine-python3
FROM python:3.7-slim

# Set the working directory to /app
WORKDIR /app

#Install gcc and update pip
RUN apt-get update && apt-get install gcc -y && pip3 install --upgrade pip && mkdir /app/data

#https://codeload.github.com/neunzehnhundert97/marvin-telegram-bot/zip/master
# Install any needed packages specified in requirements.txt
RUN pip3 install toml telepot aiotask_context more-itertools parse tinydb awake youtube_dl

# Copy the current directory contents into the container at /app
ADD bot /app


# Run app.py when the container launches
CMD ["python3.7", "app.py"]
