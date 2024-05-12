docker build -t experiments .
docker run --gpus all -it --rm -v $(pwd):/app experiments
