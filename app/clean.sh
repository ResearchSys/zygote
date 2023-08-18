#!/usr/bin/env bash


echo "Verificando diretorio de imagens"
image_dispath="imgs"

if [ "$(ls -A $image_dispath)" ]; then
    echo "removendo as imagens."
    rm $image_dispath/*
else
    echo "não a imagens para remover."
fi