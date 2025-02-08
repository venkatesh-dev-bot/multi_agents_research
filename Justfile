image_name := "multi_agent_market_research"
container_name := "multi_agent_market_research"

rebuild: rm-container build

rm-container:
  docker rm -f {{container_name}}

build: rm-container
  docker build -t {{image_name}} .

run: build
  docker run -d  -p 8001:8501 --name {{container_name}} -it --restart unless-stopped {{image_name}}

watch: run
  docker logs -f {{container_name}}
