import os
import csv
import random

from PIL import Image, ImageDraw, ImageFont
from tqdm import tqdm

from conf.zygo import (
    IMG_HEIGHT,
    IMG_WIDTH,
    IMAGE_DIR,
    CSV_PATH,
    FONT_LIST,
    FONT_SIZE,
    BACKGROUND_IMG,
)


def essay_body_fixer(text):
    """
    Remove caracteres especiais do início e fim de uma string.

    Esta função remove os caracteres especiais '[' e ']' (colchetes), aspas
    simples e aspas duplas do início e do fim da string 'texto'. Além disso,
    realiza uma operação de strip() para remover espaços em branco do
    início e do fim da string resultante.

    Args:
        text (str): A string da qual os caracteres especiais devem ser removidos.

    Returns:
        str: A string 'text' sem os caracteres especiais e espaços em branco
        do início e do fim.
    """
    caracteres_especiais = ["[", "]", "'", '"']
    for char in caracteres_especiais:
        text = text.replace(char, "")

    return text.strip()


def criar_imagem(essay_csv):
    """
    Cria uma imagem com título e texto a partir dos dados de um registro.

    Esta função recebe um registro contendo um título e um texto, e cria uma
    imagem com o título posicionado no topo e o texto formatado abaixo dele.
    A fonte para o título e o texto é escolhida aleatoriamente entre as fontes
    disponíveis. A imagem resultante é salva em um diretório especificado.

    Args:
        registro (dict): Um dicionário contendo os dados do registro, incluindo
        'title' e 'essay'.
    Returns:
        None
    """
    title = essay_csv["title"]
    text = essay_body_fixer(essay_csv["essay"])
    font = random.choice(FONT_LIST)

    image = Image.new("RGB", (IMG_WIDTH, IMG_HEIGHT), BACKGROUND_IMG)
    draw = ImageDraw.Draw(image)
    font_text = ImageFont.truetype(font, FONT_SIZE)

    pos_x_title = (IMG_WIDTH - draw.textlength(title, font=font_text)) / 2
    pos_y_title = 50
    draw.text((pos_x_title, pos_y_title), title, font=font_text, fill=(0, 0, 0))

    text_lines = []
    words = text.split()
    current_line = ""

    for word in words:
        if draw.textlength(current_line + word, font=font_text) <= IMG_WIDTH:
            current_line += word + " "
        else:
            text_lines.append(current_line)
            current_line = word + " "
    text_lines.append(current_line)

    pos_x_text = (IMG_WIDTH - draw.textlength(text_lines[0], font=font_text)) / 2
    pos_y_text = (IMG_HEIGHT - (len(text_lines) * FONT_SIZE)) / 2

    for linha in text_lines:
        draw.text((pos_x_text, pos_y_text), linha, font=font_text, fill=(0, 0, 0))
        pos_y_text += FONT_SIZE

    image_name = f"{essay_csv['id']}.png"
    image_out_path = os.path.join(IMAGE_DIR, image_name)
    image.save(image_out_path)


with open(CSV_PATH, "r", encoding="utf-8") as file:
    reader_csv = csv.DictReader(file)

    for registro in tqdm(reader_csv, desc="Criando as imagens", unit=" imagens"):
        criar_imagem(registro)
