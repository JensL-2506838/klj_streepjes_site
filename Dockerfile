FROM ubuntu:latest
LABEL authors="jenslaurijssen"

ENTRYPOINT ["top", "-b"]