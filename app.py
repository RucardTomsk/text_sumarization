# -*- coding: utf-8 -*-
import logging

import typer
from typing import Optional
from pathlib import Path
from baseline_summarizer import Summarizer

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S', filemode='a')

logger = logging.getLogger(__name__)

app = typer.Typer()

_sum = Summarizer()

@app.command()
def init():
	_sum.initels()
	logging.info(f"Initialization carried out")

@app.command()
def summariz(path: Optional[str]):
	_sum._summariz_(path_text = path)
	logging.info(f"Text {path} summarizer")

if __name__ == '__main__':
    app()