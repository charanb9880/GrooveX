#!/bin/bash

# Development script for PlayWise Music Engine

echo "Starting PlayWise Music Engine development environment..."

# Check if docker is installed
if ! command -v docker &> /dev/null
then
    echo "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null
then
    echo "docker-compose is not installed. Please install docker-compose first."
    exit 1
fi

# Start services
echo "Building and starting services..."
docker-compose up --build

echo "Services started!"
echo "Visit http://localhost:3000 for the web interface"
echo "Visit http://localhost:8000/docs for API documentation"