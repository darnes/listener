#!/bin/bash

mkdir -p ./build
rm -rf ./build/*
pwd
tar -zcvf ./build/artifact.tar.gz src/
# cp -r ./src/* ./build
cp ./appspec.yml ./build/appspec.yml
cp ./service/hooks/* ./build/
cp ./supervisor/* ./build/
cp ./requirements.txt ./build/