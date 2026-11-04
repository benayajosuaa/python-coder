#!/bin/zsh
set -eu

# Gunakan Python Homebrew dengan Tk modern, bukan Python bawaan macOS.
PYTHON_BIN="/opt/homebrew/bin/python3.13"
if [[ ! -x "$PYTHON_BIN" ]]; then
    PYTHON_BIN="/usr/local/bin/python3.13"
fi
if [[ ! -x "$PYTHON_BIN" ]]; then
    print 'Python dengan Tkinter belum tersedia. Jalankan: brew install python-tk@3.13'
    exit 1
fi

exec "$PYTHON_BIN" "${0:A:h}/m11_countdown_calendar.py"


# INI UNCUK MAC OS