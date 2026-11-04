#!/bin/zsh
set -eu

# Python dengan Tk modern untuk Mac Apple Silicon dan Intel.
PYTHON_BIN="/opt/homebrew/bin/python3.13"
if [[ ! -x "$PYTHON_BIN" ]]; then
    PYTHON_BIN="/usr/local/bin/python3.13"
fi
if [[ ! -x "$PYTHON_BIN" ]]; then
    print 'Python dengan Tkinter belum tersedia. Jalankan: brew install python-tk@3.13'
    exit 1
fi

exec "$PYTHON_BIN" "${0:A:h}/pig_pet.py"
