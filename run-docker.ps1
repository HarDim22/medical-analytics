docker build -t medical-analytics .
docker run --rm -p 8000:8000 -e ANALYTICS_API_KEY=change-me-strong medical-analytics
