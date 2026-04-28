"""
NOWA ONLINE - PAZAR ALARM SISTEMI (Termux / Telefon)
=====================================================
Versiyon : 20260428052604
Calistir : python market_alarm.py
Durdur   : Ctrl+C

Gereksinimler (bir kez):
  pkg install python tcpdump
"""

import struct, socket, subprocess, time, os, sys, urllib.request, urllib.parse
import json as _json, ssl as _ssl
from datetime import datetime

# =============================================
#  AYARLAR
# =============================================
VERSION          = "20260428052604"
GITHUB_RAW_URL   = "https://raw.githubusercontent.com/husounlu67-del/nowa-alarm/main/market_alarm.py"
SCRIPT_PATH      = os.path.abspath(__file__)
PCAP_PATH        = "/data/local/tmp/alarm_scan.pcap"
GAME_SERVER      = "213.238.175.103"

# -- Telegram ---------------------------------
TELEGRAM_TOKEN   = "8514471086:AAHuzFcpqhWwX1c4cogEo1A11WzXZ-YZhhg"
TELEGRAM_CHAT_ID = "1598896323"
# ---------------------------------------------

ALARM_LIST = [
    {"name": "Hope's Frozen Staff +0", "max_price": 1500000, "item_ids": ["b078450b", "307a450b"]},
    {"name": "Hope's Frozen Staff +1", "max_price": 1500000, "item_ids": ["317a450b"]},
    {"name": "Hope's Frozen Staff +2", "max_price": 1500000, "item_ids": ["327a450b"]},
    {"name": "Hope's Frozen Staff +3", "max_price": 5000000, "item_ids": ["337a450b"]},
    {"name": "Hope's Frozen Staff +4", "max_price": 6000000, "item_ids": ["347a450b"]},
    {"name": "Hope's Frozen Staff +5", "max_price": 10000000, "item_ids": ["357a450b"]},
    {"name": "Hope's Frozen Staff +6", "max_price": 80000000, "item_ids": ["367a450b"]},
    {"name": "Hope's Frozen Staff +7", "max_price": 110000000, "item_ids": ["377a450b"]},
    {"name": "Hope's Frozen Staff +8", "max_price": 220000000, "item_ids": ["387a450b"]},
    {"name": "Iceberg Staff +1", "max_price": 1500000, "item_ids": ["6dfb460b"]},
    {"name": "Iceberg Staff +2", "max_price": 1500000, "item_ids": ["6efb460b"]},
    {"name": "Iceberg Staff +3", "max_price": 3000000, "item_ids": ["6ffb460b"]},
    {"name": "Iceberg Staff +4", "max_price": 4000000, "item_ids": ["70fb460b"]},
    {"name": "Iceberg Staff +5", "max_price": 6000000, "item_ids": ["71fb460b"]},
    {"name": "Iceberg Staff +6", "max_price": 50000000, "item_ids": ["72fb460b"]},
    {"name": "Iceberg Staff +7", "max_price": 70000000, "item_ids": ["73fb460b"]},
    {"name": "Iceberg Staff +8", "max_price": 220000000, "item_ids": ["74fb460b"]},
    {"name": "Iceberg Staff Reb+1", "max_price": 70000000, "item_ids": ["a522470b"]},
    {"name": "Iceberg Staff Reb+2", "max_price": 110000000, "item_ids": ["a622470b"]},
    {"name": "Iceberg Staff Reb+3", "max_price": 220000000, "item_ids": ["a722470b"]},
    {"name": "Iceberg Staff Reb+4", "max_price": 220000000, "item_ids": ["a822470b"]},
    {"name": "Iceberg Staff Reb+5", "max_price": 220000000, "item_ids": ["a922470b"]},
    {"name": "Katana Sword +0", "max_price": 20000000, "item_ids": ["2eedb107", "9aedb107"]},
    {"name": "Katana Sword +1", "max_price": 20000000, "item_ids": ["9bedb107"]},
    {"name": "Katana Sword +2", "max_price": 20000000, "item_ids": ["9cedb107"]},
    {"name": "Katana Sword +3", "max_price": 30000000, "item_ids": ["9dedb107"]},
    {"name": "Katana Sword +4", "max_price": 30000000, "item_ids": ["9eedb107"]},
    {"name": "Katana Sword +5", "max_price": 40000000, "item_ids": ["9fedb107"]},
    {"name": "Katana Sword +6", "max_price": 100000000, "item_ids": ["a0edb107"]},
    {"name": "Katana Sword +7", "max_price": 220000000, "item_ids": ["a1edb107"]},
    {"name": "Katana Sword +8", "max_price": 220000000, "item_ids": ["a2edb107"]},
    {"name": "Katana Sword Reb+1", "max_price": 220000000, "item_ids": ["3314b207"]},
    {"name": "Katana Sword Reb+2", "max_price": 220000000, "item_ids": ["3414b207"]},
    {"name": "Katana Sword Reb+3", "max_price": 220000000, "item_ids": ["3514b207"]},
    {"name": "Katana Sword Reb+4", "max_price": 220000000, "item_ids": ["3614b207"]},
    {"name": "Katana Sword Reb+5", "max_price": 220000000, "item_ids": ["3714b207"]},
    {"name": "Fireguard Hammer +0", "max_price": 150000000, "item_ids": ["b10ade0b", "380bde0b"]},
    {"name": "Fireguard Hammer +1", "max_price": 150000000, "item_ids": ["390bde0b"]},
    {"name": "Fireguard Hammer +2", "max_price": 150000000, "item_ids": ["3a0bde0b"]},
    {"name": "Fireguard Hammer +3", "max_price": 150000000, "item_ids": ["3b0bde0b"]},
    {"name": "Fireguard Hammer +4", "max_price": 150000000, "item_ids": ["3c0bde0b"]},
    {"name": "Fireguard Hammer +5", "max_price": 150000000, "item_ids": ["3d0bde0b"]},
    {"name": "Fireguard Hammer +6", "max_price": 220000000, "item_ids": ["3e0bde0b"]},
    {"name": "Fireguard Hammer +7", "max_price": 220000000, "item_ids": ["3f0bde0b"]},
    {"name": "Fireguard Hammer +8", "max_price": 220000000, "item_ids": ["400bde0b"]},
    {"name": "Fireguard Hammer Reb+1", "max_price": 220000000, "item_ids": ["4932de0b"]},
    {"name": "Fireguard Hammer Reb+2", "max_price": 220000000, "item_ids": ["4a32de0b"]},
    {"name": "Fireguard Hammer Reb+3", "max_price": 220000000, "item_ids": ["4b32de0b"]},
    {"name": "Fireguard Hammer Reb+4", "max_price": 220000000, "item_ids": ["4c32de0b"]},
    {"name": "Fireguard Hammer Reb+5", "max_price": 220000000, "item_ids": ["4d32de0b"]},
    {"name": "Cold Dagger +0", "max_price": 20000000, "item_ids": ["565b1907"]},
    {"name": "Cold Dagger +1", "max_price": 20000000, "item_ids": ["cb5b1907", "575b1907"]},
    {"name": "Cold Dagger +2", "max_price": 20000000, "item_ids": ["cc5b1907", "585b1907"]},
    {"name": "Cold Dagger +3", "max_price": 150000000, "item_ids": ["cd5b1907", "595b1907"]},
    {"name": "Cold Dagger +4", "max_price": 20000000, "item_ids": ["ce5b1907", "5a5b1907"]},
    {"name": "Cold Dagger +5", "max_price": 30000000, "item_ids": ["cf5b1907", "5b5b1907"]},
    {"name": "Cold Dagger +6", "max_price": 220000000, "item_ids": ["d05b1907", "5c5b1907"]},
    {"name": "Cold Dagger +7", "max_price": 220000000, "item_ids": ["d15b1907", "5d5b1907"]},
    {"name": "Cold Dagger +8", "max_price": 220000000, "item_ids": ["d25b1907", "5e5b1907"]},
    {"name": "Light Storm Staff +7", "max_price": 110000000, "item_ids": ["1d82480b"]},
    {"name": "Light Storm Staff +8", "max_price": 220000000, "item_ids": ["1e82480b"]},
    {"name": "Light Storm Staff Reb+1", "max_price": 110000000, "item_ids": ["63a9480b"]},
    {"name": "Light Storm Staff Reb+2", "max_price": 112000000, "item_ids": ["64a9480b"]},
    {"name": "Light Storm Staff Reb+3", "max_price": 220000000, "item_ids": ["65a9480b"]},
    {"name": "Light Storm Staff Reb+4", "max_price": 220000000, "item_ids": ["66a9480b"]},
    {"name": "Light Storm Staff Reb+5", "max_price": 220000000, "item_ids": ["67a9480b"]},
    {"name": "Arcane Bow +0", "max_price": 70000000, "item_ids": ["3047140a"]},
    {"name": "Arcane Bow +1", "max_price": 70000000, "item_ids": ["af47140a"]},
    {"name": "Arcane Bow +2", "max_price": 70000000, "item_ids": ["b047140a"]},
    {"name": "Arcane Bow +3", "max_price": 90000000, "item_ids": ["b147140a"]},
    {"name": "Arcane Bow +4", "max_price": 90000000, "item_ids": ["b247140a"]},
    {"name": "Arcane Bow +5", "max_price": 110000000, "item_ids": ["b347140a"]},
    {"name": "Arcane Bow +6", "max_price": 150000000, "item_ids": ["b447140a"]},
    {"name": "Arcane Bow +7", "max_price": 220000000, "item_ids": ["b547140a"]},
    {"name": "Arcane Bow +8", "max_price": 220000000, "item_ids": ["b647140a"]},
    {"name": "Arcane Bow Reb+1", "max_price": 220000000, "item_ids": ["6f6e140a"]},
    {"name": "Arcane Bow Reb+2", "max_price": 220000000, "item_ids": ["706e140a"]},
    {"name": "Arcane Bow Reb+3", "max_price": 220000000, "item_ids": ["716e140a"]},
    {"name": "Arcane Bow Reb+4", "max_price": 220000000, "item_ids": ["726e140a"]},
    {"name": "Arcane Bow Reb+5", "max_price": 220000000, "item_ids": ["736e140a"]},
    {"name": "Hell Strike +0", "max_price": 220000000, "item_ids": ["2f1ae308", "a41ae308"]},
    {"name": "Hell Strike +1", "max_price": 220000000, "item_ids": ["a51ae308"]},
    {"name": "Hell Strike +2", "max_price": 220000000, "item_ids": ["a61ae308"]},
    {"name": "Hell Strike +3", "max_price": 220000000, "item_ids": ["a71ae308"]},
    {"name": "Hell Strike +4", "max_price": 220000000, "item_ids": ["a81ae308"]},
    {"name": "Hell Strike +5", "max_price": 220000000, "item_ids": ["a91ae308"]},
    {"name": "Hell Strike +6", "max_price": 220000000, "item_ids": ["aa1ae308"]},
    {"name": "Hell Strike +7", "max_price": 220000000, "item_ids": ["ab1ae308"]},
    {"name": "Hell Strike +8", "max_price": 220000000, "item_ids": ["ac1ae308"]},
    {"name": "Hell Strike Reb+1", "max_price": 220000000, "item_ids": ["1541e308"]},
    {"name": "Hell Strike Reb+2", "max_price": 220000000, "item_ids": ["1641e308"]},
    {"name": "Hell Strike Reb+3", "max_price": 220000000, "item_ids": ["1741e308"]},
    {"name": "Hell Strike Reb+4", "max_price": 220000000, "item_ids": ["1841e308"]},
    {"name": "Hell Strike Reb+5", "max_price": 220000000, "item_ids": ["1941e308"]},
    {"name": "HellFire Staff +0", "max_price": 20000000, "item_ids": []},
    {"name": "HellFire Staff +1", "max_price": 20000000, "item_ids": ["f574450b"]},
    {"name": "HellFire Staff +2", "max_price": 30000000, "item_ids": ["f674450b"]},
    {"name": "HellFire Staff +3", "max_price": 30000000, "item_ids": ["f774450b"]},
    {"name": "HellFire Staff +4", "max_price": 40000000, "item_ids": ["f874450b"]},
    {"name": "HellFire Staff +5", "max_price": 50000000, "item_ids": ["f974450b"]},
    {"name": "HellFire Staff +6", "max_price": 80000000, "item_ids": ["fa74450b"]},
    {"name": "HellFire Staff +7", "max_price": 220000000, "item_ids": ["fb74450b"]},
    {"name": "HellFire Staff +8", "max_price": 220000000, "item_ids": ["fc74450b"]},
    {"name": "HellFire Staff Reb+1", "max_price": 220000000, "item_ids": ["e79b450b"]},
    {"name": "HellFire Staff Reb+2", "max_price": 220000000, "item_ids": ["e89b450b"]},
    {"name": "HellFire Staff Reb+3", "max_price": 220000000, "item_ids": ["e99b450b"]},
    {"name": "HellFire Staff Reb+4", "max_price": 220000000, "item_ids": ["ea9b450b"]},
    {"name": "HellFire Staff Reb+5", "max_price": 220000000, "item_ids": ["eb9b450b"]},
    {"name": "Wrath's Spear +0", "max_price": 15000000, "item_ids": ["a7c27e09", "0ac37e09"]},
    {"name": "Wrath's Spear +1", "max_price": 20000000, "item_ids": ["0bc37e09"]},
    {"name": "Wrath's Spear +2", "max_price": 30000000, "item_ids": ["0cc37e09"]},
    {"name": "Wrath's Spear +3", "max_price": 30000000, "item_ids": ["0dc37e09"]},
    {"name": "Wrath's Spear +4", "max_price": 30000000, "item_ids": ["0ec37e09"]},
    {"name": "Wrath's Spear +5", "max_price": 40000000, "item_ids": ["0fc37e09"]},
    {"name": "Wrath's Spear +6", "max_price": 220000000, "item_ids": ["10c37e09"]},
    {"name": "Wrath's Spear +7", "max_price": 220000000, "item_ids": ["11c37e09"]},
    {"name": "Wrath's Spear +8", "max_price": 220000000, "item_ids": ["12c37e09"]},
    {"name": "Wrath's Spear Reb+1", "max_price": 220000000, "item_ids": ["f9e87e09"]},
    {"name": "Wrath's Spear Reb+2", "max_price": 220000000, "item_ids": ["fae87e09"]},
    {"name": "Wrath's Spear Reb+3", "max_price": 220000000, "item_ids": ["fbe87e09"]},
    {"name": "Wrath's Spear Reb+4", "max_price": 220000000, "item_ids": ["fce87e09"]},
    {"name": "Wrath's Spear Reb+5", "max_price": 220000000, "item_ids": ["fde87e09"]},
    {"name": "Hope's Fire Staff +0", "max_price": 5000000, "item_ids": []},
    {"name": "Hope's Fire Staff +1", "max_price": 5000000, "item_ids": ["6787480b"]},
    {"name": "Hope's Fire Staff +2", "max_price": 10000000, "item_ids": ["6887480b"]},
    {"name": "Hope's Fire Staff +3", "max_price": 10000000, "item_ids": ["6987480b"]},
    {"name": "Hope's Fire Staff +4", "max_price": 15000000, "item_ids": ["6a87480b"]},
    {"name": "Hope's Fire Staff +5", "max_price": 15000000, "item_ids": ["6b87480b"]},
    {"name": "Hope's Fire Staff +6", "max_price": 22000000, "item_ids": ["6c87480b"]},
    {"name": "Hope's Fire Staff +7", "max_price": 120000000, "item_ids": ["6d87480b"]},
    {"name": "Hope's Fire Staff +8", "max_price": 220000000, "item_ids": ["6e87480b"]},
    {"name": "Dark Shadow Dagger +0", "max_price": 20000000, "item_ids": ["ad561907"]},
    {"name": "Dark Shadow Dagger +1", "max_price": 20000000, "item_ids": ["11571907"]},
    {"name": "Dark Shadow Dagger +2", "max_price": 20000000, "item_ids": ["12571907"]},
    {"name": "Dark Shadow Dagger +3", "max_price": 20000000, "item_ids": ["13571907"]},
    {"name": "Dark Shadow Dagger +4", "max_price": 25000000, "item_ids": ["14571907"]},
    {"name": "Dark Shadow Dagger +5", "max_price": 50000000, "item_ids": ["15571907"]},
    {"name": "Dark Shadow Dagger +6", "max_price": 100000000, "item_ids": ["16571907"]},
    {"name": "Dark Shadow Dagger +7", "max_price": 220000000, "item_ids": ["17571907"]},
    {"name": "Dark Shadow Dagger +8", "max_price": 220000000, "item_ids": ["18571907"]},
    {"name": "Dark Shadow Dagger Reb+1", "max_price": 220000000, "item_ids": ["d17d1907"]},
    {"name": "Dark Shadow Dagger Reb+2", "max_price": 220000000, "item_ids": ["d27d1907"]},
    {"name": "Dark Shadow Dagger Reb+3", "max_price": 220000000, "item_ids": ["d37d1907"]},
    {"name": "Dark Shadow Dagger Reb+4", "max_price": 220000000, "item_ids": ["d47d1907"]},
    {"name": "Dark Shadow Dagger Reb+5", "max_price": 220000000, "item_ids": ["d57d1907"]},
    {"name": "Starlight Staff +7", "max_price": 120000000, "item_ids": ["c7084a0b"]},
    {"name": "Starlight Staff +8", "max_price": 220000000, "item_ids": ["c8084a0b"]},
    {"name": "Dragon Wing Bow +0", "max_price": 220000000, "item_ids": ["4959170a"]},
    {"name": "Dragon Wing Bow +1", "max_price": 220000000, "item_ids": ["8b59170a"]},
    {"name": "Dragon Wing Bow +2", "max_price": 220000000, "item_ids": ["8c59170a"]},
    {"name": "Dragon Wing Bow +3", "max_price": 220000000, "item_ids": ["8d59170a"]},
    {"name": "Dragon Wing Bow +4", "max_price": 220000000, "item_ids": ["8e59170a"]},
    {"name": "Dragon Wing Bow +5", "max_price": 220000000, "item_ids": ["8f59170a"]},
    {"name": "Dragon Wing Bow +6", "max_price": 220000000, "item_ids": ["9059170a"]},
    {"name": "Dragon Wing Bow +7", "max_price": 220000000, "item_ids": ["9159170a"]},
    {"name": "Dragon Wing Bow +8", "max_price": 220000000, "item_ids": ["9259170a", "5159170a"]},
    {"name": "Hope's Thunder Staff +7", "max_price": 110000000, "item_ids": ["e100470b"]},
    {"name": "Hope's Thunder Staff +8", "max_price": 220000000, "item_ids": ["e200470b"]},
    {"name": "Hope's Thunder Staff Reb+1", "max_price": 110000000, "item_ids": ["f527470b"]},
    {"name": "Hope's Thunder Staff Reb+2", "max_price": 150000000, "item_ids": ["f627470b"]},
    {"name": "Hope's Thunder Staff Reb+3", "max_price": 220000000, "item_ids": ["f727470b"]},
    {"name": "Hope's Thunder Staff Reb+4", "max_price": 220000000, "item_ids": ["f827470b"]},
    {"name": "Hope's Thunder Staff Reb+5", "max_price": 220000000, "item_ids": ["f927470b"]},
    {"name": "Thunder Animor +5", "max_price": 65000000, "item_ids": ["c719e10b"]},
    {"name": "Thunder Animor +6", "max_price": 220000000, "item_ids": ["c819e10b"]},
    {"name": "Thunder Animor +7", "max_price": 220000000, "item_ids": ["c919e10b"]},
    {"name": "Thunder Animor +8", "max_price": 220000000, "item_ids": ["ca19e10b"]},
    {"name": "Firelance +5", "max_price": 65000000, "item_ids": ["8bbf7e09"]},
    {"name": "Firelance +6", "max_price": 220000000, "item_ids": ["8cbf7e09"]},
    {"name": "Firelance +7", "max_price": 220000000, "item_ids": ["8dbf7e09"]},
    {"name": "Firelance +8", "max_price": 220000000, "item_ids": ["8ebf7e09"]},
    {"name": "Frozendeath Dagger +0", "max_price": 110000000, "item_ids": ["0b641c07", "7c651c07"]},
    {"name": "Frozendeath Dagger +1", "max_price": 110000000, "item_ids": ["7d651c07"]},
    {"name": "Frozendeath Dagger +2", "max_price": 150000000, "item_ids": ["7e651c07"]},
    {"name": "Frozendeath Dagger +3", "max_price": 150000000, "item_ids": ["7f651c07"]},
    {"name": "Frozendeath Dagger +4", "max_price": 150000000, "item_ids": ["80651c07"]},
    {"name": "Frozendeath Dagger +5", "max_price": 170000000, "item_ids": ["81651c07"]},
    {"name": "Frozendeath Dagger +6", "max_price": 220000000, "item_ids": ["82651c07"]},
    {"name": "Frozendeath Dagger +7", "max_price": 220000000, "item_ids": ["83651c07"]},
    {"name": "Frozendeath Dagger +8", "max_price": 220000000, "item_ids": ["84651c07"]},
    {"name": "Frozen Cross Bow +0", "max_price": 100000000, "item_ids": ["8e54170a", "1a56170a"]},
    {"name": "Frozen Cross Bow +1", "max_price": 100000000, "item_ids": ["1b56170a"]},
    {"name": "Frozen Cross Bow +2", "max_price": 100000000, "item_ids": ["1c56170a"]},
    {"name": "Frozen Cross Bow +3", "max_price": 100000000, "item_ids": ["1d56170a"]},
    {"name": "Frozen Cross Bow +4", "max_price": 100000000, "item_ids": ["1e56170a"]},
    {"name": "Frozen Cross Bow +5", "max_price": 100000000, "item_ids": ["1f56170a"]},
    {"name": "Frozen Cross Bow +6", "max_price": 220000000, "item_ids": ["2056170a"]},
    {"name": "Frozen Cross Bow +7", "max_price": 220000000, "item_ids": ["2156170a"]},
    {"name": "Frozen Cross Bow +8", "max_price": 220000000, "item_ids": ["2256170a"]},
    {"name": "Gaze of Icedeath +8", "max_price": 220000000, "item_ids": ["fe1a4d0b"]},
    {"name": "King Axe +0", "max_price": 50000000, "item_ids": ["73621708"]},
    {"name": "HellFire Bow +0", "max_price": 50000000, "item_ids": ["cf469009"]},
    {"name": "HellFire Bow +1", "max_price": 50000000, "item_ids": ["df469009"]},
    {"name": "HellFire Bow +2", "max_price": 60000000, "item_ids": ["e0469009"]},
    {"name": "HellFire Bow +3", "max_price": 80000000, "item_ids": ["e1469009"]},
    {"name": "HellFire Bow +4", "max_price": 110000000, "item_ids": ["e2469009"]},
    {"name": "HellFire Bow +5", "max_price": 110000000, "item_ids": ["e3469009"]},
    {"name": "HellFire Bow +6", "max_price": 220000000, "item_ids": ["e4469009"]},
    {"name": "HellFire Bow +7", "max_price": 220000000, "item_ids": ["e5469009"]},
    {"name": "HellFire Bow +8", "max_price": 220000000, "item_ids": ["e6469009"]},
    {"name": "Venom Hammer +8", "max_price": 220000000, "item_ids": ["26fd560b"]},
    {"name": "Claw Hammer +0", "max_price": 25000000, "item_ids": ["0dfd560b", "32fd560b"]},
    {"name": "Claw Hammer +1", "max_price": 25000000, "item_ids": ["33fd560b"]},
    {"name": "Claw Hammer +2", "max_price": 25000000, "item_ids": ["34fd560b"]},
    {"name": "Claw Hammer +3", "max_price": 50000000, "item_ids": ["35fd560b"]},
    {"name": "Claw Hammer +4", "max_price": 50000000, "item_ids": ["36fd560b"]},
    {"name": "Claw Hammer +5", "max_price": 50000000, "item_ids": ["37fd560b"]},
    {"name": "Claw Hammer +6", "max_price": 70000000, "item_ids": ["38fd560b"]},
    {"name": "Claw Hammer +7", "max_price": 120000000, "item_ids": ["39fd560b"]},
    {"name": "Claw Hammer +8", "max_price": 220000000, "item_ids": ["3afd560b"]},
    {"name": "Claw Hammer Reb+1", "max_price": 120000000, "item_ids": ["7100570b"]},
    {"name": "Claw Hammer Reb+2", "max_price": 220000000, "item_ids": ["7200570b"]},
    {"name": "Claw Hammer Reb+3", "max_price": 220000000, "item_ids": ["7300570b"]},
    {"name": "Claw Hammer Reb+4", "max_price": 220000000, "item_ids": ["7400570b"]},
    {"name": "Claw Hammer Reb+5", "max_price": 220000000, "item_ids": ["7500570b"]},
    {"name": "Nightfang Hammer +1", "max_price": 20000000, "item_ids": ["29fd560b"]},
    {"name": "Nightfang Hammer +2", "max_price": 30000000, "item_ids": ["2afd560b"]},
    {"name": "Nightfang Hammer +3", "max_price": 30000000, "item_ids": ["2bfd560b"]},
    {"name": "Nightfang Hammer +4", "max_price": 50000000, "item_ids": ["2cfd560b"]},
    {"name": "Nightfang Hammer +5", "max_price": 50000000, "item_ids": ["2dfd560b"]},
    {"name": "Nightfang Hammer +6", "max_price": 70000000, "item_ids": ["2efd560b"]},
    {"name": "Nightfang Hammer +7", "max_price": 220000000, "item_ids": ["2ffd560b"]},
    {"name": "Nightfang Hammer +8", "max_price": 220000000, "item_ids": ["30fd560b"]},
    {"name": "Lord's Sentinel Shield +0", "max_price": 20000000, "item_ids": ["b6ddac0a"]},
    {"name": "Lord's Sentinel Shield +1", "max_price": 20000000, "item_ids": ["6bdeac0a"]},
    {"name": "Lord's Sentinel Shield +2", "max_price": 30000000, "item_ids": ["6cdeac0a"]},
    {"name": "Lord's Sentinel Shield +3", "max_price": 50000000, "item_ids": ["6ddeac0a"]},
    {"name": "Lord's Sentinel Shield +4", "max_price": 60000000, "item_ids": ["6edeac0a"]},
    {"name": "Lord's Sentinel Shield +5", "max_price": 80000000, "item_ids": ["6fdeac0a"]},
    {"name": "Lord's Sentinel Shield +6", "max_price": 100000000, "item_ids": ["70deac0a"]},
    {"name": "Lord's Sentinel Shield +7", "max_price": 220000000, "item_ids": ["71deac0a"]},
    {"name": "Lord's Sentinel Shield +8", "max_price": 220000000, "item_ids": ["72deac0a"]},
    {"name": "Lord's Sentinel Shield Reb+1", "max_price": 220000000, "item_ids": ["a305ad0a"]},
    {"name": "Lord's Sentinel Shield Reb+2", "max_price": 220000000, "item_ids": ["a405ad0a"]},
    {"name": "Lord's Sentinel Shield Reb+3", "max_price": 220000000, "item_ids": ["a505ad0a"]},
    {"name": "Lord's Sentinel Shield Reb+4", "max_price": 220000000, "item_ids": ["a605ad0a"]},
    {"name": "Lord's Sentinel Shield Reb+5", "max_price": 220000000, "item_ids": ["a705ad0a"]},
    {"name": "Phantom Shield +0", "max_price": 220000000, "item_ids": ["efe1ac0a"]},
    {"name": "Phantom Shield +1", "max_price": 220000000, "item_ids": ["71e2ac0a"]},
    {"name": "Phantom Shield +2", "max_price": 220000000, "item_ids": ["72e2ac0a"]},
    {"name": "Phantom Shield +3", "max_price": 220000000, "item_ids": ["73e2ac0a"]},
    {"name": "Phantom Shield +4", "max_price": 220000000, "item_ids": ["74e2ac0a"]},
    {"name": "Phantom Shield +5", "max_price": 220000000, "item_ids": ["75e2ac0a", "f4e1ac0a"]},
    {"name": "Phantom Shield +6", "max_price": 220000000, "item_ids": ["76e2ac0a"]},
    {"name": "Phantom Shield +7", "max_price": 220000000, "item_ids": ["77e2ac0a"]},
    {"name": "Phantom Shield +8", "max_price": 220000000, "item_ids": ["78e2ac0a"]},
    {"name": "Phantom Shield Reb+1", "max_price": 220000000, "item_ids": ["ef09ad0a"]},
    {"name": "Phantom Shield Reb+2", "max_price": 220000000, "item_ids": ["f009ad0a"]},
    {"name": "Phantom Shield Reb+3", "max_price": 220000000, "item_ids": ["f109ad0a"]},
    {"name": "Phantom Shield Reb+4", "max_price": 220000000, "item_ids": ["f209ad0a"]},
    {"name": "Phantom Shield Reb+5", "max_price": 220000000, "item_ids": ["f309ad0a"]},
    {"name": "Frozen Axe +0", "max_price": 220000000, "item_ids": ["0d914d08", "90924d08"]},
    {"name": "Frozen Axe +1", "max_price": 220000000, "item_ids": ["91924d08"]},
    {"name": "Frozen Axe +2", "max_price": 220000000, "item_ids": ["92924d08"]},
    {"name": "Frozen Axe +3", "max_price": 220000000, "item_ids": ["93924d08"]},
    {"name": "Frozen Axe +4", "max_price": 220000000, "item_ids": ["94924d08"]},
    {"name": "Frozen Axe +5", "max_price": 220000000, "item_ids": ["95924d08"]},
    {"name": "Frozen Axe +6", "max_price": 220000000, "item_ids": ["96924d08"]},
    {"name": "Frozen Axe +7", "max_price": 220000000, "item_ids": ["97924d08"]},
    {"name": "Frozen Axe +8", "max_price": 220000000, "item_ids": ["98924d08"]},
    {"name": "Shade Dagger +4", "max_price": 2000000, "item_ids": ["14eea006", "3ceea006"]},
    {"name": "Shade Dagger +5", "max_price": 9000000, "item_ids": ["15eea006", "3deea006"]},
    {"name": "Shade Dagger +6", "max_price": 20000000, "item_ids": ["16eea006", "3eeea006"]},
    {"name": "Shade Dagger +7", "max_price": 90000000, "item_ids": ["17eea006", "3feea006"]},
    {"name": "Shade Dagger +8", "max_price": 220000000, "item_ids": ["40eea006", "18eea006"]},
    {"name": "Shade Dagger Reb+1", "max_price": 90000000, "item_ids": ["17f2a006"]},
    {"name": "Shade Dagger Reb+2", "max_price": 150000000, "item_ids": ["18f2a006"]},
    {"name": "Shade Dagger Reb+3", "max_price": 220000000, "item_ids": ["19f2a006"]},
    {"name": "Shade Dagger Reb+4", "max_price": 220000000, "item_ids": ["1af2a006"]},
    {"name": "Shade Dagger Reb+5", "max_price": 220000000, "item_ids": ["1bf2a006"]},
    {"name": "Reaper +1", "max_price": 1500000, "item_ids": ["51934f09", "79934f09"]},
    {"name": "Reaper +2", "max_price": 3000000, "item_ids": ["52934f09", "7a934f09"]},
    {"name": "Reaper +3", "max_price": 3000000, "item_ids": ["53934f09", "7b934f09"]},
    {"name": "Reaper +4", "max_price": 2000000, "item_ids": ["54934f09", "7c934f09"]},
    {"name": "Reaper +5", "max_price": 9000000, "item_ids": ["55934f09", "7d934f09"]},
    {"name": "Reaper +6", "max_price": 30000000, "item_ids": ["56934f09", "7e934f09"]},
    {"name": "Reaper +7", "max_price": 150000000, "item_ids": ["7f934f09", "57934f09"]},
    {"name": "Reaper +8", "max_price": 220000000, "item_ids": ["58934f09", "80934f09"]},
    {"name": "Reaper Reb+1", "max_price": 150000000, "item_ids": ["57974f09"]},
    {"name": "Reaper Reb+2", "max_price": 190000000, "item_ids": ["58974f09"]},
    {"name": "Reaper Reb+3", "max_price": 220000000, "item_ids": ["59974f09"]},
    {"name": "Reaper Reb+4", "max_price": 220000000, "item_ids": ["5a974f09"]},
    {"name": "Reaper Reb+5", "max_price": 220000000, "item_ids": ["5b974f09"]},
    {"name": "Thunder Impact +3", "max_price": 2000000, "item_ids": ["d3fcb608", "fbfdb608"]},
    {"name": "Thunder Impact +4", "max_price": 2000000, "item_ids": ["d4fcb608", "fcfdb608"]},
    {"name": "Thunder Impact +5", "max_price": 6000000, "item_ids": ["d5fcb608", "fdfdb608"]},
    {"name": "Thunder Impact +6", "max_price": 20000000, "item_ids": ["d6fcb608", "fefdb608"]},
    {"name": "Thunder Impact +7", "max_price": 99000000, "item_ids": ["d7fcb608", "fffdb608"]},
    {"name": "Thunder Impact +8", "max_price": 220000000, "item_ids": ["00fdb608", "d8fcb608"]},
    {"name": "Thunder Impact Reb+1", "max_price": 99000000, "item_ids": ["d700b708"]},
    {"name": "Thunder Impact Reb+2", "max_price": 150000000, "item_ids": ["d800b708"]},
    {"name": "Thunder Impact Reb+3", "max_price": 220000000, "item_ids": ["d900b708"]},
    {"name": "Thunder Impact Reb+4", "max_price": 220000000, "item_ids": ["da00b708"]},
    {"name": "Thunder Impact Reb+5", "max_price": 220000000, "item_ids": ["db00b708"]},
    {"name": "IronShade Bow +3", "max_price": 2000000, "item_ids": ["93bb090a", "bbbb090a"]},
    {"name": "IronShade Bow +4", "max_price": 2000000, "item_ids": ["94bb090a", "bcbb090a"]},
    {"name": "IronShade Bow +5", "max_price": 5000000, "item_ids": ["95bb090a", "bdbb090a"]},
    {"name": "IronShade Bow +6", "max_price": 8000000, "item_ids": ["96bb090a", "bebb090a"]},
    {"name": "IronShade Bow +7", "max_price": 90000000, "item_ids": ["bfbb090a", "97bb090a"]},
    {"name": "IronShade Bow +8", "max_price": 220000000, "item_ids": ["98bb090a", "c0bb090a"]},
    {"name": "IronShade Bow Reb+1", "max_price": 90000000, "item_ids": ["97bf090a"]},
    {"name": "IronShade Bow Reb+2", "max_price": 150000000, "item_ids": ["98bf090a"]},
    {"name": "IronShade Bow Reb+3", "max_price": 220000000, "item_ids": ["99bf090a"]},
    {"name": "IronShade Bow Reb+4", "max_price": 220000000, "item_ids": ["9abf090a"]},
    {"name": "IronShade Bow Reb+5", "max_price": 220000000, "item_ids": ["9bbf090a"]},
    {"name": "Bloody Dagger +7", "max_price": 5000000, "item_ids": ["9f679f06", "77679f06"]},
    {"name": "Bloody Dagger +8", "max_price": 150000000, "item_ids": ["a0679f06", "78679f06"]},
    {"name": "Bloody Dagger Reb+1", "max_price": 5000000, "item_ids": ["776b9f06"]},
    {"name": "Bloody Dagger Reb+2", "max_price": 6000000, "item_ids": ["786b9f06"]},
    {"name": "Bloody Dagger Reb+3", "max_price": 30000000, "item_ids": ["796b9f06"]},
    {"name": "Bloody Dagger Reb+4", "max_price": 30000000, "item_ids": ["7a6b9f06"]},
    {"name": "Bloody Dagger Reb+5", "max_price": 150000000, "item_ids": ["7b6b9f06"]},
    {"name": "Phantom Sword +3", "max_price": 2000000, "item_ids": ["13dd8807", "3bdd8807"]},
    {"name": "Phantom Sword +4", "max_price": 2000000, "item_ids": ["14dd8807", "3cdd8807"]},
    {"name": "Phantom Sword +5", "max_price": 8000000, "item_ids": ["15dd8807", "3ddd8807"]},
    {"name": "Phantom Sword +6", "max_price": 20000000, "item_ids": ["16dd8807", "3edd8807"]},
    {"name": "Phantom Sword +7", "max_price": 50000000, "item_ids": ["3fdd8807", "17dd8807"]},
    {"name": "Phantom Sword +8", "max_price": 220000000, "item_ids": ["18dd8807", "40dd8807"]},
    {"name": "Phantom Sword Reb+1", "max_price": 70000000, "item_ids": ["17e18807"]},
    {"name": "Phantom Sword Reb+2", "max_price": 80000000, "item_ids": ["18e18807"]},
    {"name": "Phantom Sword Reb+3", "max_price": 150000000, "item_ids": ["19e18807"]},
    {"name": "Phantom Sword Reb+4", "max_price": 220000000, "item_ids": ["1ae18807"]},
    {"name": "Phantom Sword Reb+5", "max_price": 220000000, "item_ids": ["1be18807"]},
    {"name": "Giant Reaper +1", "max_price": 5000000, "item_ids": ["f1195109", "191a5109"]},
    {"name": "Giant Reaper +2", "max_price": 5000000, "item_ids": ["1a1a5109", "f2195109"]},
    {"name": "Giant Reaper +3", "max_price": 5000000, "item_ids": ["1b1a5109", "f3195109"]},
    {"name": "Giant Reaper +4", "max_price": 10000000, "item_ids": ["1c1a5109", "f4195109"]},
    {"name": "Giant Reaper +5", "max_price": 10000000, "item_ids": ["1d1a5109", "f5195109"]},
    {"name": "Giant Reaper +6", "max_price": 90000000, "item_ids": ["f6195109", "1e1a5109"]},
    {"name": "Giant Reaper +7", "max_price": 150000000, "item_ids": ["1f1a5109", "f7195109"]},
    {"name": "Giant Reaper +8", "max_price": 220000000, "item_ids": ["201a5109", "f8195109"]},
    {"name": "Giant Reaper Reb+1", "max_price": 150000000, "item_ids": ["f71d5109"]},
    {"name": "Giant Reaper Reb+2", "max_price": 220000000, "item_ids": ["f81d5109"]},
    {"name": "Giant Reaper Reb+3", "max_price": 220000000, "item_ids": ["f91d5109"]},
    {"name": "Giant Reaper Reb+4", "max_price": 220000000, "item_ids": ["fa1d5109"]},
    {"name": "Giant Reaper Reb+5", "max_price": 220000000, "item_ids": ["fb1d5109"]},
    {"name": "Giant Thunder Impact +3", "max_price": 5000000, "item_ids": ["9b83b808", "7383b808"]},
    {"name": "Giant Thunder Impact +4", "max_price": 7000000, "item_ids": ["9c83b808", "7483b808"]},
    {"name": "Giant Thunder Impact +5", "max_price": 10000000, "item_ids": ["9d83b808", "7583b808"]},
    {"name": "Giant Thunder Impact +6", "max_price": 50000000, "item_ids": ["9e83b808", "7683b808"]},
    {"name": "Giant Thunder Impact +7", "max_price": 80000000, "item_ids": ["9f83b808", "7783b808"]},
    {"name": "Giant Thunder Impact +8", "max_price": 220000000, "item_ids": ["a083b808", "7883b808"]},
    {"name": "Giant Thunder Impact Reb+1", "max_price": 110000000, "item_ids": ["7787b808"]},
    {"name": "Giant Thunder Impact Reb+2", "max_price": 150000000, "item_ids": ["7887b808"]},
    {"name": "Giant Thunder Impact Reb+3", "max_price": 220000000, "item_ids": ["7987b808"]},
    {"name": "Giant Thunder Impact Reb+4", "max_price": 220000000, "item_ids": ["7a87b808"]},
    {"name": "Giant Thunder Impact Reb+5", "max_price": 220000000, "item_ids": ["7b87b808"]},
    {"name": "Giant Phantom Sword +6", "max_price": 40000000, "item_ids": ["7eea8b07"]},
    {"name": "Giant Phantom Sword +7", "max_price": 70000000, "item_ids": ["7fea8b07"]},
    {"name": "Giant Phantom Sword +8", "max_price": 220000000, "item_ids": ["80ea8b07"]},
    {"name": "Giant Phantom Sword Reb+1", "max_price": 70000000, "item_ids": ["57ee8b07"]},
    {"name": "Giant Phantom Sword Reb+2", "max_price": 80000000, "item_ids": ["58ee8b07"]},
    {"name": "Giant Phantom Sword Reb+3", "max_price": 220000000, "item_ids": ["59ee8b07"]},
    {"name": "Giant Phantom Sword Reb+4", "max_price": 220000000, "item_ids": ["5aee8b07"]},
    {"name": "Giant Phantom Sword Reb+5", "max_price": 220000000, "item_ids": ["5bee8b07"]},
    {"name": "Giant IronShade Bow +5", "max_price": 10000000, "item_ids": ["d5c80c0a", "fdc80c0a"]},
    {"name": "Giant IronShade Bow +6", "max_price": 25000000, "item_ids": ["d6c80c0a", "fec80c0a"]},
    {"name": "Giant IronShade Bow +7", "max_price": 120000000, "item_ids": ["ffc80c0a", "d7c80c0a"]},
    {"name": "Giant IronShade Bow +8", "max_price": 220000000, "item_ids": ["d8c80c0a", "00c80c0a"]},
    {"name": "Giant IronShade Bow Reb+1", "max_price": 120000000, "item_ids": ["d7cc0c0a"]},
    {"name": "Giant IronShade Bow Reb+2", "max_price": 150000000, "item_ids": ["d8cc0c0a"]},
    {"name": "Giant IronShade Bow Reb+3", "max_price": 220000000, "item_ids": ["d9cc0c0a"]},
    {"name": "Giant IronShade Bow Reb+4", "max_price": 220000000, "item_ids": ["dacc0c0a"]},
    {"name": "Giant IronShade Bow Reb+5", "max_price": 220000000, "item_ids": ["dbcc0c0a"]},
    {"name": "Giant Shade Dagger +1", "max_price": 2000000, "item_ids": ["d974a206", "b174a206"]},
    {"name": "Giant Shade Dagger +2", "max_price": 2000000, "item_ids": ["da74a206", "b274a206"]},
    {"name": "Giant Shade Dagger +3", "max_price": 3000000, "item_ids": ["db74a206", "b374a206"]},
    {"name": "Giant Shade Dagger +4", "max_price": 5000000, "item_ids": ["dc74a206", "b474a206"]},
    {"name": "Giant Shade Dagger +5", "max_price": 5000000, "item_ids": ["dd74a206", "b574a206"]},
    {"name": "Giant Shade Dagger +6", "max_price": 20000000, "item_ids": ["de74a206", "b674a206"]},
    {"name": "Giant Shade Dagger +7", "max_price": 90000000, "item_ids": ["df74a206", "b774a206"]},
    {"name": "Giant Shade Dagger +8", "max_price": 220000000, "item_ids": ["e074a206", "b874a206"]},
    {"name": "Bloody Bow +7", "max_price": 15000000, "item_ids": ["1f35080a", "f734080a"]},
    {"name": "Bloody Bow +8", "max_price": 70000000, "item_ids": ["2035080a", "f834080a"]},
    {"name": "Bloody Bow Reb+1", "max_price": 15000000, "item_ids": ["f738080a"]},
    {"name": "Bloody Bow Reb+2", "max_price": 15000000, "item_ids": ["f838080a"]},
    {"name": "Bloody Bow Reb+3", "max_price": 15000000, "item_ids": ["f938080a"]},
    {"name": "Bloody Bow Reb+4", "max_price": 15000000, "item_ids": ["fa38080a"]},
    {"name": "Bloody Bow Reb+5", "max_price": 70000000, "item_ids": ["fb38080a"]},
    {"name": "Master Warrior Earring Old", "max_price": 15000000, "item_ids": ["956ed117"]},
    {"name": "Master Rogue Earring Old", "max_price": 45000000, "item_ids": ["7e72d117"]},
    {"name": "Master Rogue Earring +0", "max_price": 220000000, "item_ids": ["f8098212"]},
    {"name": "Master Priest Earring Old", "max_price": 10000000, "item_ids": ["507ad117"]},
    {"name": "Master Courage Ring Old", "max_price": 10000000, "item_ids": ["6d7dd117"]},
    {"name": "Master Hextech Ring Old", "max_price": 12000000, "item_ids": ["5681d117"]},
    {"name": "Master Belt Of Courage Old", "max_price": 220000000, "item_ids": ["8a89d117"]},
    {"name": "Master Belt Of Str Old", "max_price": 2000000, "item_ids": ["738dd117"]},
    {"name": "Master Belt Of Dexterity Old", "max_price": 2000000, "item_ids": ["5c91d117"]},
    {"name": "Elarin Ring Old", "max_price": 12000000, "item_ids": ["ab94d117"]},
    {"name": "Fire Ring Old", "max_price": 2000000, "item_ids": ["6e2b7a14"]},
    {"name": "Fire Ring +0", "max_price": 100000000, "item_ids": ["bc49b913"]},
    {"name": "Fire Ring +1", "max_price": 220000000, "item_ids": ["894bb913"]},
    {"name": "Frozen Ring Old", "max_price": 2000000, "item_ids": ["3f987e14"]},
    {"name": "Frozen Ring +0", "max_price": 30000000, "item_ids": ["cd70b913"]},
    {"name": "Thunder Ring Old", "max_price": 2000000, "item_ids": ["10058314"]},
    {"name": "Essence Pendant Old", "max_price": 2000000, "item_ids": ["17786814"]},
    {"name": "Essence Pendant +0", "max_price": 220000000, "item_ids": ["247e1413"]},
    {"name": "Essence Pendant +1", "max_price": 220000000, "item_ids": ["e77e1413"]},
    {"name": "Holy Pendant Old", "max_price": 2000000, "item_ids": ["e8e46c14"]},
    {"name": "Courage Pendant Old", "max_price": 8000000, "item_ids": ["460b6414"]},
    {"name": "Courage Pendant +1", "max_price": 220000000, "item_ids": ["dd7e1413"]},
    {"name": "Elderwood Belt Old", "max_price": 5000000, "item_ids": ["97de8b14"]},
    {"name": "Elderwood Belt +0", "max_price": 220000000, "item_ids": ["013f4a14"]},
    {"name": "Elderwood Belt +1", "max_price": 220000000, "item_ids": ["3f404a14"]},
    {"name": "Skull Belt Old", "max_price": 20000000, "item_ids": ["684b9014"]},
    {"name": "Belt of STR Old", "max_price": 2000000, "item_ids": ["58ef4b14"]},
    {"name": "Bronze Earring Old", "max_price": 2000000, "item_ids": ["67387c12"]},
    {"name": "Elfen Earring Old", "max_price": 3000000, "item_ids": ["ac278412"]},
    {"name": "Elfen Earring +0", "max_price": 220000000, "item_ids": ["ba888312"]},
    {"name": "Elfen Earring +1", "max_price": 220000000, "item_ids": ["4b898312"]},
    {"name": "Berserker Earring Old", "max_price": 3000000, "item_ids": ["f0528212"]},
    {"name": "Berserker Earring +1", "max_price": 220000000, "item_ids": ["d3028212"]},
    {"name": "Courage Earring Old", "max_price": 12000000, "item_ids": ["5bf38012"]},
    {"name": "Courage Earring +0", "max_price": 220000000, "item_ids": ["797b8012"]},
    {"name": "Courage Earring +1", "max_price": 220000000, "item_ids": ["017c8012"]},
    {"name": "Shadow Earring Old", "max_price": 4000000, "item_ids": ["ae315b14"]},
    {"name": "Shaman Silver Earring Old", "max_price": 2000000, "item_ids": ["6d1a8112"]},
    {"name": "Shaman Silver Earring +0", "max_price": 100000000, "item_ids": ["7b7b8012"]},
    {"name": "Shaman Silver Earring +1", "max_price": 220000000, "item_ids": ["157c8012"]},
    {"name": "Rogue Silver Earring Old", "max_price": 3000000, "item_ids": ["78b28312"]},
    {"name": "Rogue Silver Earring +0", "max_price": 100000000, "item_ids": ["b6888312"]},
    {"name": "Rogue Silver Earring +1", "max_price": 220000000, "item_ids": ["23898312"]},
    {"name": "Hero Ring Old", "max_price": 25000000, "item_ids": ["9dbe7514"]},
    {"name": "Hero Ring +0", "max_price": 220000000, "item_ids": ["2f15ad13"]},
    {"name": "Loyal Earring Old", "max_price": 2000000, "item_ids": ["be4e8412"]},
    {"name": "Black Drake Neck Old", "max_price": 2000000, "item_ids": ["5d511813"]},
    {"name": "Blue Drake Neck +0", "max_price": 80000000, "item_ids": ["501f1c13"]},
    {"name": "Amulet Of Evil Old", "max_price": 3000000, "item_ids": ["b3851b13"]},
    {"name": "Amulet Of Evil +0", "max_price": 120000000, "item_ids": ["a6981a13"]},
    {"name": "Amulet Of Evil +1", "max_price": 220000000, "item_ids": ["7b991a13"]},
    {"name": "Elder Necklace Old", "max_price": 2000000, "item_ids": ["37031813"]},
    {"name": "Amulet of Divinity Old", "max_price": 2000000, "item_ids": ["58c21a13"]},
    {"name": "Red Drake Neck Old", "max_price": 2000000, "item_ids": ["4c2a1813"]},
    {"name": "Str Necklace Old", "max_price": 2000000, "item_ids": ["10701c13"]},
    {"name": "Str Necklace +0", "max_price": 100000000, "item_ids": ["471f1c13"]},
    {"name": "Str Necklace +1", "max_price": 220000000, "item_ids": ["25201c13"]},
    {"name": "White Drake Neck Old", "max_price": 2000000, "item_ids": ["7a101b13"]},
    {"name": "Secret Power Ring Old", "max_price": 5000000, "item_ids": ["8047b213"]},
    {"name": "Secret Power Ring +1", "max_price": 220000000, "item_ids": ["79a9b113"]},
    {"name": "Elderwood Ring Old", "max_price": 2000000, "item_ids": ["b754b513"]},
    {"name": "Elderwood Ring +0", "max_price": 220000000, "item_ids": ["59b6b413"]},
    {"name": "Elderwood Ring +1", "max_price": 220000000, "item_ids": ["e1b6b413"]},
    {"name": "Ring of Shadow Old", "max_price": 50000000, "item_ids": ["cc517114"]},
    {"name": "Ring of Shadow +0", "max_price": 220000000, "item_ids": ["71b1ad13"]},
    {"name": "Hero Earring Old", "max_price": 5000000, "item_ids": ["ddc45614"]},
    {"name": "Warrior Holy Titan Helmet +4", "max_price": 3000000, "item_ids": ["465b470c", "3c5b470c"]},
    {"name": "Warrior Holy Titan Helmet +5", "max_price": 5000000, "item_ids": ["475b470c", "3d5b470c"]},
    {"name": "Warrior Holy Titan Helmet +6", "max_price": 15000000, "item_ids": ["485b470c", "3e5b470c"]},
    {"name": "Warrior Holy Titan Helmet +7", "max_price": 35000000, "item_ids": ["3f5b470c", "495b470c"]},
    {"name": "Warrior Holy Titan Helmet +8", "max_price": 220000000, "item_ids": ["4a5b470c", "405b470c"]},
    {"name": "Warrior Holy Titan Helmet Reb+1", "max_price": 35000000, "item_ids": ["b9f1df0c"]},
    {"name": "Warrior Holy Titan Helmet Reb+2", "max_price": 60000000, "item_ids": ["baf1df0c"]},
    {"name": "Warrior Holy Titan Helmet Reb+3", "max_price": 220000000, "item_ids": ["bbf1df0c"]},
    {"name": "Warrior Holy Titan Helmet Reb+4", "max_price": 220000000, "item_ids": ["bcf1df0c"]},
    {"name": "Warrior Holy Titan Helmet Reb+5", "max_price": 220000000, "item_ids": ["bdf1df0c"]},
    {"name": "Warrior Holy Titan Pauldron +4", "max_price": 3000000, "item_ids": ["6c53470c", "7653470c"]},
    {"name": "Warrior Holy Titan Pauldron +5", "max_price": 5000000, "item_ids": ["6d53470c", "7753470c"]},
    {"name": "Warrior Holy Titan Pauldron +6", "max_price": 15000000, "item_ids": ["6e53470c", "7853470c"]},
    {"name": "Warrior Holy Titan Pauldron +7", "max_price": 35000000, "item_ids": ["7953470c", "6f53470c"]},
    {"name": "Warrior Holy Titan Pauldron +8", "max_price": 220000000, "item_ids": ["7053470c", "7a53470c"]},
    {"name": "Warrior Holy Titan Pauldron Reb+1", "max_price": 35000000, "item_ids": ["e9e9df0c"]},
    {"name": "Warrior Holy Titan Pauldron Reb+2", "max_price": 60000000, "item_ids": ["eae9df0c"]},
    {"name": "Warrior Holy Titan Pauldron Reb+3", "max_price": 220000000, "item_ids": ["ebe9df0c"]},
    {"name": "Warrior Holy Titan Pauldron Reb+4", "max_price": 220000000, "item_ids": ["ece9df0c"]},
    {"name": "Warrior Holy Titan Pauldron Reb+5", "max_price": 220000000, "item_ids": ["ede9df0c"]},
    {"name": "Warrior Holy Titan Pads +4", "max_price": 3000000, "item_ids": ["5457470c"]},
    {"name": "Warrior Holy Titan Pads +5", "max_price": 5000000, "item_ids": ["5557470c"]},
    {"name": "Warrior Holy Titan Pads +6", "max_price": 15000000, "item_ids": ["5657470c"]},
    {"name": "Warrior Holy Titan Pads +7", "max_price": 35000000, "item_ids": ["5757470c"]},
    {"name": "Warrior Holy Titan Pads +8", "max_price": 220000000, "item_ids": ["5857470c"]},
    {"name": "Warrior Holy Titan Pads Reb+1", "max_price": 35000000, "item_ids": ["d1eddf0c"]},
    {"name": "Warrior Holy Titan Pads Reb+2", "max_price": 60000000, "item_ids": ["d2eddf0c"]},
    {"name": "Warrior Holy Titan Pads Reb+3", "max_price": 220000000, "item_ids": ["d3eddf0c"]},
    {"name": "Warrior Holy Titan Pads Reb+4", "max_price": 220000000, "item_ids": ["d4eddf0c"]},
    {"name": "Warrior Holy Titan Pads Reb+5", "max_price": 220000000, "item_ids": ["d5eddf0c"]},
    {"name": "Warrior Holy Titan Boots +4", "max_price": 3000000, "item_ids": ["0c63470c"]},
    {"name": "Warrior Holy Titan Boots +5", "max_price": 5000000, "item_ids": ["0d63470c"]},
    {"name": "Warrior Holy Titan Boots +6", "max_price": 15000000, "item_ids": ["0e63470c"]},
    {"name": "Warrior Holy Titan Boots +7", "max_price": 35000000, "item_ids": ["0f63470c"]},
    {"name": "Warrior Holy Titan Boots +8", "max_price": 220000000, "item_ids": ["1063470c"]},
    {"name": "Warrior Holy Titan Boots Reb+1", "max_price": 35000000, "item_ids": ["89f9df0c"]},
    {"name": "Warrior Holy Titan Boots Reb+2", "max_price": 60000000, "item_ids": ["8af9df0c"]},
    {"name": "Warrior Holy Titan Boots Reb+3", "max_price": 220000000, "item_ids": ["8bf9df0c"]},
    {"name": "Warrior Holy Titan Boots Reb+4", "max_price": 220000000, "item_ids": ["8cf9df0c"]},
    {"name": "Warrior Holy Titan Boots Reb+5", "max_price": 220000000, "item_ids": ["8df9df0c"]},
    {"name": "Warrior Holy Titan Gauntlets +4", "max_price": 3000000, "item_ids": ["245f470c", "2e5f470c"]},
    {"name": "Warrior Holy Titan Gauntlets +5", "max_price": 5000000, "item_ids": ["255f470c", "2f5f470c"]},
    {"name": "Warrior Holy Titan Gauntlets +6", "max_price": 15000000, "item_ids": ["305f470c", "265f470c"]},
    {"name": "Warrior Holy Titan Gauntlets +7", "max_price": 35000000, "item_ids": ["315f470c", "275f470c"]},
    {"name": "Warrior Holy Titan Gauntlets +8", "max_price": 220000000, "item_ids": ["285f470c", "325f470c"]},
    {"name": "Warrior Holy Titan Gauntlets Reb+1", "max_price": 35000000, "item_ids": ["a1f5df0c"]},
    {"name": "Warrior Holy Titan Gauntlets Reb+2", "max_price": 60000000, "item_ids": ["a2f5df0c"]},
    {"name": "Warrior Holy Titan Gauntlets Reb+3", "max_price": 220000000, "item_ids": ["a3f5df0c"]},
    {"name": "Warrior Holy Titan Gauntlets Reb+4", "max_price": 220000000, "item_ids": ["a4f5df0c"]},
    {"name": "Warrior Holy Titan Gauntlets Reb+5", "max_price": 220000000, "item_ids": ["a5f5df0c"]},
    {"name": "Warrior Titan Helmet +5", "max_price": 2000000, "item_ids": ["fd18380c", "0719380c"]},
    {"name": "Warrior Titan Helmet +6", "max_price": 5000000, "item_ids": ["fe18380c", "0819380c"]},
    {"name": "Warrior Titan Helmet +7", "max_price": 10000000, "item_ids": ["ff18380c", "0919380c"]},
    {"name": "Warrior Titan Helmet +8", "max_price": 555000000, "item_ids": ["0a19380c", "0018380c"]},
    {"name": "Warrior Titan Helmet Reb+1", "max_price": 10000000, "item_ids": ["79afd00c"]},
    {"name": "Warrior Titan Helmet Reb+2", "max_price": 50000000, "item_ids": ["7aafd00c"]},
    {"name": "Warrior Titan Helmet Reb+3", "max_price": 70000000, "item_ids": ["7bafd00c"]},
    {"name": "Warrior Titan Helmet Reb+4", "max_price": 220000000, "item_ids": ["7cafd00c"]},
    {"name": "Warrior Titan Helmet Reb+5", "max_price": 555000000, "item_ids": ["7dafd00c"]},
    {"name": "Warrior Titan Pauldron +5", "max_price": 2000000, "item_ids": ["2d11380c", "3711380c"]},
    {"name": "Warrior Titan Pauldron +6", "max_price": 5000000, "item_ids": ["2e11380c", "3811380c"]},
    {"name": "Warrior Titan Pauldron +7", "max_price": 10000000, "item_ids": ["3911380c", "2f11380c"]},
    {"name": "Warrior Titan Pauldron +8", "max_price": 220000000, "item_ids": ["3011380c", "3a11380c"]},
    {"name": "Warrior Titan Pauldron Reb+1", "max_price": 10000000, "item_ids": ["a9a7d00c"]},
    {"name": "Warrior Titan Pauldron Reb+2", "max_price": 50000000, "item_ids": ["aaa7d00c"]},
    {"name": "Warrior Titan Pauldron Reb+3", "max_price": 70000000, "item_ids": ["aba7d00c"]},
    {"name": "Warrior Titan Pauldron Reb+4", "max_price": 220000000, "item_ids": ["aca7d00c"]},
    {"name": "Warrior Titan Pauldron Reb+5", "max_price": 220000000, "item_ids": ["ada7d00c"]},
    {"name": "Warrior Titan Pads +5", "max_price": 2000000, "item_ids": ["1515380c", "1f15380c"]},
    {"name": "Warrior Titan Pads +6", "max_price": 5000000, "item_ids": ["2015380c", "1615380c"]},
    {"name": "Warrior Titan Pads +7", "max_price": 10000000, "item_ids": ["2115380c", "1715380c"]},
    {"name": "Warrior Titan Pads +8", "max_price": 555000000, "item_ids": ["2215380c", "1815380c"]},
    {"name": "Warrior Titan Pads Reb+1", "max_price": 10000000, "item_ids": ["91abd00c"]},
    {"name": "Warrior Titan Pads Reb+2", "max_price": 50000000, "item_ids": ["92abd00c"]},
    {"name": "Warrior Titan Pads Reb+3", "max_price": 70000000, "item_ids": ["93abd00c"]},
    {"name": "Warrior Titan Pads Reb+4", "max_price": 220000000, "item_ids": ["94abd00c"]},
    {"name": "Warrior Titan Pads Reb+5", "max_price": 555000000, "item_ids": ["95abd00c"]},
    {"name": "Warrior Titan Boots +5", "max_price": 2000000, "item_ids": ["cd20380c", "d720380c"]},
    {"name": "Warrior Titan Boots +6", "max_price": 5000000, "item_ids": ["ce20380c", "d820380c"]},
    {"name": "Warrior Titan Boots +7", "max_price": 10000000, "item_ids": ["d920380c", "cf20380c"]},
    {"name": "Warrior Titan Boots +8", "max_price": 555000000, "item_ids": ["d020380c", "da20380c"]},
    {"name": "Warrior Titan Boots Reb+1", "max_price": 20000000, "item_ids": ["49b7d00c"]},
    {"name": "Warrior Titan Boots Reb+2", "max_price": 20000000, "item_ids": ["4ab7d00c"]},
    {"name": "Warrior Titan Boots Reb+3", "max_price": 70000000, "item_ids": ["4bb7d00c"]},
    {"name": "Warrior Titan Boots Reb+4", "max_price": 100000000, "item_ids": ["4cb7d00c"]},
    {"name": "Warrior Titan Boots Reb+5", "max_price": 555000000, "item_ids": ["4db7d00c"]},
    {"name": "Warrior Titan Gauntlets +5", "max_price": 2000000, "item_ids": ["e51c380c", "ef1c380c"]},
    {"name": "Warrior Titan Gauntlets +6", "max_price": 5000000, "item_ids": ["e61c380c", "f01c380c"]},
    {"name": "Warrior Titan Gauntlets +7", "max_price": 10000000, "item_ids": ["f11c380c", "e71c380c"]},
    {"name": "Warrior Titan Gauntlets +8", "max_price": 555000000, "item_ids": ["e81c380c", "f21c380c"]},
    {"name": "Warrior Titan Gauntlets Reb+1", "max_price": 10000000, "item_ids": ["61b3d00c"]},
    {"name": "Warrior Titan Gauntlets Reb+2", "max_price": 20000000, "item_ids": ["62b3d00c"]},
    {"name": "Warrior Titan Gauntlets Reb+3", "max_price": 50000000, "item_ids": ["63b3d00c"]},
    {"name": "Warrior Titan Gauntlets Reb+4", "max_price": 60000000, "item_ids": ["64b3d00c"]},
    {"name": "Warrior Titan Gauntlets Reb+5", "max_price": 555000000, "item_ids": ["65b3d00c"]},
    {"name": "Rogue Holy Titan Helmet +4", "max_price": 5000000, "item_ids": ["3ab7a90e", "3cb5a90e"]},
    {"name": "Rogue Holy Titan Helmet +5", "max_price": 5000000, "item_ids": ["3bb7a90e", "3db5a90e"]},
    {"name": "Rogue Holy Titan Helmet +6", "max_price": 15000000, "item_ids": ["3cb7a90e", "3eb5a90e"]},
    {"name": "Rogue Holy Titan Helmet +7", "max_price": 35000000, "item_ids": ["3db7a90e", "3fb5a90e"]},
    {"name": "Rogue Holy Titan Helmet +8", "max_price": 220000000, "item_ids": ["3eb7a90e", "40b5a90e"]},
    {"name": "Rogue Holy Titan Helmet Reb+1", "max_price": 35000000, "item_ids": ["f54b420f"]},
    {"name": "Rogue Holy Titan Helmet Reb+2", "max_price": 60000000, "item_ids": ["f64b420f"]},
    {"name": "Rogue Holy Titan Helmet Reb+3", "max_price": 220000000, "item_ids": ["f74b420f"]},
    {"name": "Rogue Holy Titan Helmet Reb+4", "max_price": 220000000, "item_ids": ["f84b420f"]},
    {"name": "Rogue Holy Titan Helmet Reb+5", "max_price": 220000000, "item_ids": ["f94b420f"]},
    {"name": "Rogue Holy Titan Pauldron +4", "max_price": 5000000, "item_ids": ["6cada90e", "6aafa90e"]},
    {"name": "Rogue Holy Titan Pauldron +5", "max_price": 5000000, "item_ids": ["6dada90e", "6bafa90e"]},
    {"name": "Rogue Holy Titan Pauldron +6", "max_price": 15000000, "item_ids": ["6eada90e", "6cafa90e"]},
    {"name": "Rogue Holy Titan Pauldron +7", "max_price": 35000000, "item_ids": ["6fada90e", "6dafa90e"]},
    {"name": "Rogue Holy Titan Pauldron +8", "max_price": 220000000, "item_ids": ["70ada90e", "6eafa90e"]},
    {"name": "Rogue Holy Titan Pauldron Reb+1", "max_price": 35000000, "item_ids": ["2544420f"]},
    {"name": "Rogue Holy Titan Pauldron Reb+2", "max_price": 60000000, "item_ids": ["2644420f"]},
    {"name": "Rogue Holy Titan Pauldron Reb+3", "max_price": 220000000, "item_ids": ["2744420f"]},
    {"name": "Rogue Holy Titan Pauldron Reb+4", "max_price": 220000000, "item_ids": ["2844420f"]},
    {"name": "Rogue Holy Titan Pauldron Reb+5", "max_price": 220000000, "item_ids": ["2944420f"]},
    {"name": "Rogue Holy Titan Pads +4", "max_price": 5000000, "item_ids": ["52b3a90e", "54b1a90e"]},
    {"name": "Rogue Holy Titan Pads +5", "max_price": 5000000, "item_ids": ["53b3a90e", "55b1a90e"]},
    {"name": "Rogue Holy Titan Pads +6", "max_price": 15000000, "item_ids": ["54b3a90e", "56b1a90e"]},
    {"name": "Rogue Holy Titan Pads +7", "max_price": 35000000, "item_ids": ["57b1a90e", "55b3a90e"]},
    {"name": "Rogue Holy Titan Pads +8", "max_price": 220000000, "item_ids": ["56b3a90e", "58b1a90e"]},
    {"name": "Rogue Holy Titan Pads Reb+1", "max_price": 35000000, "item_ids": ["0d48420f"]},
    {"name": "Rogue Holy Titan Pads Reb+2", "max_price": 60000000, "item_ids": ["0e48420f"]},
    {"name": "Rogue Holy Titan Pads Reb+3", "max_price": 220000000, "item_ids": ["0f48420f"]},
    {"name": "Rogue Holy Titan Pads Reb+4", "max_price": 220000000, "item_ids": ["1048420f"]},
    {"name": "Rogue Holy Titan Pads Reb+5", "max_price": 220000000, "item_ids": ["1148420f"]},
    {"name": "Rogue Holy Titan Boots +4", "max_price": 5000000, "item_ids": ["0cbda90e", "0abfa90e"]},
    {"name": "Rogue Holy Titan Boots +5", "max_price": 5000000, "item_ids": ["0bbfa90e", "0dbda90e"]},
    {"name": "Rogue Holy Titan Boots +6", "max_price": 15000000, "item_ids": ["0cbfa90e", "0ebda90e"]},
    {"name": "Rogue Holy Titan Boots +7", "max_price": 35000000, "item_ids": ["0dbfa90e", "0fbda90e"]},
    {"name": "Rogue Holy Titan Boots +8", "max_price": 220000000, "item_ids": ["0ebfa90e", "10bda90e"]},
    {"name": "Rogue Holy Titan Boots Reb+1", "max_price": 35000000, "item_ids": ["c553420f"]},
    {"name": "Rogue Holy Titan Boots Reb+2", "max_price": 60000000, "item_ids": ["c653420f"]},
    {"name": "Rogue Holy Titan Boots Reb+3", "max_price": 220000000, "item_ids": ["c753420f"]},
    {"name": "Rogue Holy Titan Boots Reb+4", "max_price": 220000000, "item_ids": ["c853420f"]},
    {"name": "Rogue Holy Titan Boots Reb+5", "max_price": 220000000, "item_ids": ["c953420f"]},
    {"name": "Rogue Holy Titan Gauntlets +4", "max_price": 5000000, "item_ids": ["22bba90e", "24b9a90e"]},
    {"name": "Rogue Holy Titan Gauntlets +5", "max_price": 5000000, "item_ids": ["25b9a90e", "23bba90e"]},
    {"name": "Rogue Holy Titan Gauntlets +6", "max_price": 15000000, "item_ids": ["24bba90e", "26b9a90e"]},
    {"name": "Rogue Holy Titan Gauntlets +7", "max_price": 35000000, "item_ids": ["27b9a90e", "25bba90e"]},
    {"name": "Rogue Holy Titan Gauntlets +8", "max_price": 220000000, "item_ids": ["26bba90e", "28b9a90e"]},
    {"name": "Rogue Holy Titan Gauntlets Reb+1", "max_price": 35000000, "item_ids": ["dd4f420f"]},
    {"name": "Rogue Holy Titan Gauntlets Reb+2", "max_price": 60000000, "item_ids": ["de4f420f"]},
    {"name": "Rogue Holy Titan Gauntlets Reb+3", "max_price": 220000000, "item_ids": ["df4f420f"]},
    {"name": "Rogue Holy Titan Gauntlets Reb+4", "max_price": 220000000, "item_ids": ["e04f420f"]},
    {"name": "Rogue Holy Titan Gauntlets Reb+5", "max_price": 220000000, "item_ids": ["e14f420f"]},
    {"name": "Rogue Titan Helmet +5", "max_price": 2000000, "item_ids": ["fd729a0e", "fb749a0e"]},
    {"name": "Rogue Titan Helmet +6", "max_price": 5000000, "item_ids": ["fe729a0e", "fc749a0e"]},
    {"name": "Rogue Titan Helmet +7", "max_price": 10000000, "item_ids": ["fd749a0e", "ff729a0e"]},
    {"name": "Rogue Titan Helmet +8", "max_price": 220000000, "item_ids": ["00729a0e", "fe749a0e"]},
    {"name": "Rogue Titan Helmet Reb+1", "max_price": 10000000, "item_ids": ["b509330f"]},
    {"name": "Rogue Titan Helmet Reb+2", "max_price": 50000000, "item_ids": ["b609330f"]},
    {"name": "Rogue Titan Helmet Reb+3", "max_price": 70000000, "item_ids": ["b709330f"]},
    {"name": "Rogue Titan Helmet Reb+4", "max_price": 220000000, "item_ids": ["b809330f"]},
    {"name": "Rogue Titan Helmet Reb+5", "max_price": 220000000, "item_ids": ["b909330f"]},
    {"name": "Rogue Titan Pauldron +5", "max_price": 2000000, "item_ids": ["2d6b9a0e", "2b6d9a0e"]},
    {"name": "Rogue Titan Pauldron +6", "max_price": 5000000, "item_ids": ["2e6b9a0e", "2c6d9a0e"]},
    {"name": "Rogue Titan Pauldron +7", "max_price": 10000000, "item_ids": ["2f6b9a0e", "2d6d9a0e"]},
    {"name": "Rogue Titan Pauldron +8", "max_price": 220000000, "item_ids": ["306b9a0e", "2e6d9a0e"]},
    {"name": "Rogue Titan Pauldron Reb+1", "max_price": 10000000, "item_ids": ["e501330f"]},
    {"name": "Rogue Titan Pauldron Reb+2", "max_price": 50000000, "item_ids": ["e601330f"]},
    {"name": "Rogue Titan Pauldron Reb+3", "max_price": 70000000, "item_ids": ["e701330f"]},
    {"name": "Rogue Titan Pauldron Reb+4", "max_price": 220000000, "item_ids": ["e801330f"]},
    {"name": "Rogue Titan Pauldron Reb+5", "max_price": 220000000, "item_ids": ["e901330f"]},
    {"name": "Rogue Titan Pads +5", "max_price": 2000000, "item_ids": ["156f9a0e", "13719a0e"]},
    {"name": "Rogue Titan Pads +6", "max_price": 5000000, "item_ids": ["166f9a0e", "14719a0e"]},
    {"name": "Rogue Titan Pads +7", "max_price": 10000000, "item_ids": ["15719a0e", "176f9a0e"]},
    {"name": "Rogue Titan Pads +8", "max_price": 220000000, "item_ids": ["186f9a0e", "16719a0e"]},
    {"name": "Rogue Titan Pads Reb+2", "max_price": 50000000, "item_ids": ["ce05330f"]},
    {"name": "Rogue Titan Pads Reb+3", "max_price": 70000000, "item_ids": ["cf05330f"]},
    {"name": "Rogue Titan Pads Reb+4", "max_price": 220000000, "item_ids": ["d005330f"]},
    {"name": "Rogue Titan Pads Reb+5", "max_price": 220000000, "item_ids": ["d105330f"]},
    {"name": "Rogue Titan Boots +5", "max_price": 2000000, "item_ids": ["cd7a9a0e", "cb7c9a0e"]},
    {"name": "Rogue Titan Boots +6", "max_price": 5000000, "item_ids": ["ce7a9a0e", "cc7c9a0e"]},
    {"name": "Rogue Titan Boots +7", "max_price": 10000000, "item_ids": ["cf7a9a0e", "cd7c9a0e"]},
    {"name": "Rogue Titan Boots +8", "max_price": 220000000, "item_ids": ["ce7c9a0e", "d07a9a0e"]},
    {"name": "Rogue Titan Boots Reb+1", "max_price": 10000000, "item_ids": ["8511330f"]},
    {"name": "Rogue Titan Boots Reb+2", "max_price": 50000000, "item_ids": ["8611330f"]},
    {"name": "Rogue Titan Boots Reb+3", "max_price": 70000000, "item_ids": ["8711330f"]},
    {"name": "Rogue Titan Boots Reb+4", "max_price": 220000000, "item_ids": ["8811330f"]},
    {"name": "Rogue Titan Boots Reb+5", "max_price": 220000000, "item_ids": ["8911330f"]},
    {"name": "Rogue Titan Gauntlets +5", "max_price": 2000000, "item_ids": ["e5769a0e", "e3789a0e"]},
    {"name": "Rogue Titan Gauntlets +6", "max_price": 5000000, "item_ids": ["e6769a0e", "e4789a0e"]},
    {"name": "Rogue Titan Gauntlets +7", "max_price": 10000000, "item_ids": ["e7769a0e", "e5789a0e"]},
    {"name": "Rogue Titan Gauntlets +8", "max_price": 220000000, "item_ids": ["e8769a0e", "e6789a0e"]},
    {"name": "Rogue Titan Gauntlets Reb+1", "max_price": 10000000, "item_ids": ["9d0d330f"]},
    {"name": "Rogue Titan Gauntlets Reb+2", "max_price": 50000000, "item_ids": ["9e0d330f"]},
    {"name": "Rogue Titan Gauntlets Reb+3", "max_price": 70000000, "item_ids": ["9f0d330f"]},
    {"name": "Rogue Titan Gauntlets Reb+4", "max_price": 220000000, "item_ids": ["a00d330f"]},
    {"name": "Rogue Titan Gauntlets Reb+5", "max_price": 220000000, "item_ids": ["a10d330f"]},
    {"name": "Rogue Full Guard Helmet +7", "max_price": 1000000, "item_ids": ["bf308b0e", "bd328b0e"]},
    {"name": "Rogue Full Guard Helmet +8", "max_price": 30000000, "item_ids": ["be328b0e", "c0308b0e"]},
    {"name": "Rogue Full Guard Helmet +9", "max_price": 220000000, "item_ids": ["bf328b0e", "c1308b0e"]},
    {"name": "Rogue Full Guard Pauldron +7", "max_price": 1000000, "item_ids": ["ed2a8b0e", "ef288b0e"]},
    {"name": "Rogue Full Guard Pauldron +8", "max_price": 30000000, "item_ids": ["ee2a8b0e", "f0288b0e"]},
    {"name": "Rogue Full Guard Pauldron +9", "max_price": 220000000, "item_ids": ["ef2a8b0e", "f1288b0e"]},
    {"name": "Rogue Full Guard Pads +7", "max_price": 1000000, "item_ids": ["d72c8b0e", "d52e8b0e"]},
    {"name": "Rogue Full Guard Pads +8", "max_price": 30000000, "item_ids": ["d62e8b0e", "d82c8b0e"]},
    {"name": "Rogue Full Guard Pads +9", "max_price": 220000000, "item_ids": ["d72e8b0e", "d92c8b0e"]},
    {"name": "Rogue Full Guard Boots +7", "max_price": 1000000, "item_ids": ["8f388b0e", "8d3a8b0e"]},
    {"name": "Rogue Full Guard Boots +8", "max_price": 30000000, "item_ids": ["90388b0e", "8e3a8b0e"]},
    {"name": "Rogue Full Guard Boots +9", "max_price": 220000000, "item_ids": ["91388b0e", "8f3a8b0e"]},
    {"name": "Rogue Full Guard Gauntlets +7", "max_price": 1000000, "item_ids": ["a5368b0e", "a7348b0e"]},
    {"name": "Rogue Full Guard Gauntlets +8", "max_price": 30000000, "item_ids": ["a6368b0e", "a8348b0e"]},
    {"name": "Rogue Full Guard Gauntlets +9", "max_price": 220000000, "item_ids": ["a7368b0e", "a9348b0e"]},
    {"name": "Priest Holy Titan Helmet +4", "max_price": 5000000, "item_ids": ["30110c11"]},
    {"name": "Priest Holy Titan Helmet +5", "max_price": 5000000, "item_ids": ["31110c11"]},
    {"name": "Priest Holy Titan Helmet +6", "max_price": 15000000, "item_ids": ["32110c11"]},
    {"name": "Priest Holy Titan Helmet +7", "max_price": 35000000, "item_ids": ["33110c11"]},
    {"name": "Priest Holy Titan Helmet +8", "max_price": 220000000, "item_ids": ["34110c11"]},
    {"name": "Priest Holy Titan Helmet Reb+1", "max_price": 35000000, "item_ids": ["d7a5a411"]},
    {"name": "Priest Holy Titan Helmet Reb+2", "max_price": 50000000, "item_ids": ["d8a5a411"]},
    {"name": "Priest Holy Titan Helmet Reb+3", "max_price": 100000000, "item_ids": ["d9a5a411"]},
    {"name": "Priest Holy Titan Helmet Reb+4", "max_price": 100000000, "item_ids": ["daa5a411"]},
    {"name": "Priest Holy Titan Helmet Reb+5", "max_price": 220000000, "item_ids": ["dba5a411"]},
    {"name": "Priest Holy Titan Pauldron +4", "max_price": 5000000, "item_ids": ["6c070c11", "60090c11"]},
    {"name": "Priest Holy Titan Pauldron +5", "max_price": 5000000, "item_ids": ["6d070c11", "61090c11"]},
    {"name": "Priest Holy Titan Pauldron +6", "max_price": 15000000, "item_ids": ["6e070c11", "62090c11"]},
    {"name": "Priest Holy Titan Pauldron +7", "max_price": 35000000, "item_ids": ["63090c11", "6f070c11"]},
    {"name": "Priest Holy Titan Pauldron +8", "max_price": 220000000, "item_ids": ["70070c11", "64090c11"]},
    {"name": "Priest Holy Titan Pads +4", "max_price": 5000000, "item_ids": ["540b0c11", "480d0c11"]},
    {"name": "Priest Holy Titan Pads +5", "max_price": 5000000, "item_ids": ["550b0c11", "490d0c11"]},
    {"name": "Priest Holy Titan Pads +6", "max_price": 15000000, "item_ids": ["560b0c11", "4a0d0c11"]},
    {"name": "Priest Holy Titan Pads +7", "max_price": 35000000, "item_ids": ["570b0c11", "4b0d0c11"]},
    {"name": "Priest Holy Titan Pads +8", "max_price": 220000000, "item_ids": ["580b0c11", "4c0d0c11"]},
    {"name": "Priest Holy Titan Pads Reb+1", "max_price": 35000000, "item_ids": ["efa1a411"]},
    {"name": "Priest Holy Titan Pads Reb+2", "max_price": 35000000, "item_ids": ["f0a1a411"]},
    {"name": "Priest Holy Titan Pads Reb+3", "max_price": 50000000, "item_ids": ["f1a1a411"]},
    {"name": "Priest Holy Titan Pads Reb+4", "max_price": 100000000, "item_ids": ["f2a1a411"]},
    {"name": "Priest Holy Titan Pads Reb+5", "max_price": 220000000, "item_ids": ["f3a1a411"]},
    {"name": "Priest Holy Titan Boots +4", "max_price": 5000000, "item_ids": ["00190c11", "3c0f0c11"]},
    {"name": "Priest Holy Titan Boots +5", "max_price": 5000000, "item_ids": ["01190c11", "3d0f0c11"]},
    {"name": "Priest Holy Titan Boots +6", "max_price": 15000000, "item_ids": ["3e0f0c11", "02190c11"]},
    {"name": "Priest Holy Titan Boots +7", "max_price": 35000000, "item_ids": ["03190c11", "3f0f0c11"]},
    {"name": "Priest Holy Titan Boots +8", "max_price": 220000000, "item_ids": ["04190c11", "400f0c11"]},
    {"name": "Priest Holy Titan Gauntlets +4", "max_price": 5000000, "item_ids": ["24130c11"]},
    {"name": "Priest Holy Titan Gauntlets +5", "max_price": 5000000, "item_ids": ["25130c11"]},
    {"name": "Priest Holy Titan Gauntlets +6", "max_price": 15000000, "item_ids": ["26130c11"]},
    {"name": "Priest Holy Titan Gauntlets +7", "max_price": 35000000, "item_ids": ["27130c11"]},
    {"name": "Priest Holy Titan Gauntlets +8", "max_price": 220000000, "item_ids": ["28130c11"]},
    {"name": "Priest Titan Helmet +5", "max_price": 2000000, "item_ids": ["f1cefc10", "fdccfc10"]},
    {"name": "Priest Titan Helmet +6", "max_price": 5000000, "item_ids": ["f2cefc10", "feccfc10"]},
    {"name": "Priest Titan Helmet +7", "max_price": 10000000, "item_ids": ["ffccfc10", "f3cefc10"]},
    {"name": "Priest Titan Helmet +8", "max_price": 220000000, "item_ids": ["f4cefc10", "00ccfc10"]},
    {"name": "Priest Titan Helmet Reb+1", "max_price": 20000000, "item_ids": ["97639511"]},
    {"name": "Priest Titan Helmet Reb+2", "max_price": 40000000, "item_ids": ["98639511"]},
    {"name": "Priest Titan Helmet Reb+3", "max_price": 100000000, "item_ids": ["99639511"]},
    {"name": "Priest Titan Helmet Reb+4", "max_price": 150000000, "item_ids": ["9a639511"]},
    {"name": "Priest Titan Helmet Reb+5", "max_price": 220000000, "item_ids": ["9b639511"]},
    {"name": "Priest Titan Pauldron +5", "max_price": 2000000, "item_ids": ["2dc5fc10"]},
    {"name": "Priest Titan Pauldron +6", "max_price": 5000000, "item_ids": ["2ec5fc10"]},
    {"name": "Priest Titan Pauldron +7", "max_price": 10000000, "item_ids": ["2fc5fc10"]},
    {"name": "Priest Titan Pauldron +8", "max_price": 220000000, "item_ids": ["30c5fc10"]},
    {"name": "Priest Titan Pads +5", "max_price": 2000000, "item_ids": ["15c9fc10", "09cbfc10"]},
    {"name": "Priest Titan Pads +6", "max_price": 5000000, "item_ids": ["16c9fc10", "0acbfc10"]},
    {"name": "Priest Titan Pads +7", "max_price": 10000000, "item_ids": ["17c9fc10", "0bcbfc10"]},
    {"name": "Priest Titan Pads +8", "max_price": 220000000, "item_ids": ["18c9fc10", "0ccbfc10"]},
    {"name": "Priest Titan Pads Reb+1", "max_price": 20000000, "item_ids": ["af5f9511"]},
    {"name": "Priest Titan Pads Reb+2", "max_price": 40000000, "item_ids": ["b05f9511"]},
    {"name": "Priest Titan Pads Reb+3", "max_price": 100000000, "item_ids": ["b15f9511"]},
    {"name": "Priest Titan Pads Reb+4", "max_price": 150000000, "item_ids": ["b25f9511"]},
    {"name": "Priest Titan Pads Reb+5", "max_price": 220000000, "item_ids": ["b35f9511"]},
    {"name": "Priest Titan Boots +5", "max_price": 2000000, "item_ids": ["c1d6fc10"]},
    {"name": "Priest Titan Boots +6", "max_price": 5000000, "item_ids": ["c2d6fc10"]},
    {"name": "Priest Titan Boots +7", "max_price": 10000000, "item_ids": ["c3d6fc10"]},
    {"name": "Priest Titan Boots +8", "max_price": 220000000, "item_ids": ["c4d6fc10"]},
    {"name": "Priest Titan Boots Reb+1", "max_price": 20000000, "item_ids": ["676b9511"]},
    {"name": "Priest Titan Boots Reb+2", "max_price": 40000000, "item_ids": ["686b9511"]},
    {"name": "Priest Titan Boots Reb+3", "max_price": 100000000, "item_ids": ["696b9511"]},
    {"name": "Priest Titan Boots Reb+4", "max_price": 150000000, "item_ids": ["6a6b9511"]},
    {"name": "Priest Titan Boots Reb+5", "max_price": 220000000, "item_ids": ["6b6b9511"]},
    {"name": "Priest Titan Gauntlets +5", "max_price": 2000000, "item_ids": ["e5d0fc10"]},
    {"name": "Priest Titan Gauntlets +6", "max_price": 5000000, "item_ids": ["e6d0fc10"]},
    {"name": "Priest Titan Gauntlets +7", "max_price": 10000000, "item_ids": ["e7d0fc10"]},
    {"name": "Priest Titan Gauntlets +8", "max_price": 220000000, "item_ids": ["e8d0fc10"]},
    {"name": "Priest Half Guard Helmet +7", "max_price": 1000000, "item_ids": ["3f06cf10", "4906cf10"]},
    {"name": "Priest Half Guard Helmet +8", "max_price": 20000000, "item_ids": ["4006cf10", "4a06cf10"]},
    {"name": "Priest Half Guard Helmet +9", "max_price": 220000000, "item_ids": ["4106cf10", "4b06cf10"]},
    {"name": "Priest Half Guard Pauldron +7", "max_price": 1000000, "item_ids": ["79fece10", "6ffece10"]},
    {"name": "Priest Half Guard Pauldron +8", "max_price": 20000000, "item_ids": ["7afece10", "70fece10"]},
    {"name": "Priest Half Guard Pauldron +9", "max_price": 220000000, "item_ids": ["7bfece10", "71fece10"]},
    {"name": "Priest Half Guard Pads +7", "max_price": 1000000, "item_ids": ["5702cf10", "6102cf10"]},
    {"name": "Priest Half Guard Pads +8", "max_price": 20000000, "item_ids": ["5802cf10", "6202cf10"]},
    {"name": "Priest Half Guard Pads +9", "max_price": 220000000, "item_ids": ["5902cf10", "6302cf10"]},
    {"name": "Priest Half Guard Boots +7", "max_price": 1000000, "item_ids": ["0f0ecf10", "190ecf10"]},
    {"name": "Priest Half Guard Boots +8", "max_price": 20000000, "item_ids": ["1a0ecf10", "100ecf10"]},
    {"name": "Priest Half Guard Boots +9", "max_price": 220000000, "item_ids": ["1b0ecf10", "110ecf10"]},
    {"name": "Priest Half Guard Gauntlets +7", "max_price": 1000000, "item_ids": ["270acf10", "310acf10"]},
    {"name": "Priest Half Guard Gauntlets +8", "max_price": 20000000, "item_ids": ["280acf10", "320acf10"]},
    {"name": "Priest Half Guard Gauntlets +9", "max_price": 220000000, "item_ids": ["290acf10", "330acf10"]},
    {"name": "Priest Fabric Helmet +7", "max_price": 1000000, "item_ids": ["09c4bf10", "ffc3bf10"]},
    {"name": "Priest Fabric Helmet +8", "max_price": 10000000, "item_ids": ["0ac4bf10", "00c3bf10"]},
    {"name": "Priest Fabric Helmet +9", "max_price": 220000000, "item_ids": ["0bc4bf10", "01c3bf10"]},
    {"name": "Priest Fabric Pauldron +7", "max_price": 1000000, "item_ids": ["39bcbf10", "2fbcbf10"]},
    {"name": "Priest Fabric Pauldron +8", "max_price": 10000000, "item_ids": ["3abcbf10", "30bcbf10"]},
    {"name": "Priest Fabric Pauldron +9", "max_price": 220000000, "item_ids": ["3bbcbf10", "31bcbf10"]},
    {"name": "Priest Fabric Pads +7", "max_price": 1000000, "item_ids": ["21c0bf10", "17c0bf10"]},
    {"name": "Priest Fabric Pads +8", "max_price": 10000000, "item_ids": ["22c0bf10", "18c0bf10"]},
    {"name": "Priest Fabric Pads +9", "max_price": 220000000, "item_ids": ["23c0bf10", "19c0bf10"]},
    {"name": "Priest Fabric Boots +7", "max_price": 1000000, "item_ids": ["cfcbbf10", "d9cbbf10"]},
    {"name": "Priest Fabric Boots +8", "max_price": 10000000, "item_ids": ["dacbbf10", "d0cbbf10"]},
    {"name": "Priest Fabric Boots +9", "max_price": 220000000, "item_ids": ["dbcbbf10", "d1cbbf10"]},
    {"name": "Priest Fabric Gauntlets +7", "max_price": 1000000, "item_ids": ["dbc9bf10", "f1c7bf10"]},
    {"name": "Priest Fabric Gauntlets +8", "max_price": 10000000, "item_ids": ["f2c7bf10", "dcc9bf10"]},
    {"name": "Priest Fabric Gauntlets +9", "max_price": 220000000, "item_ids": ["f3c7bf10", "ddc9bf10"]},
    {"name": "Mage Holy Titan Helmet +5", "max_price": 5000000, "item_ids": ["3de2da0f"]},
    {"name": "Mage Holy Titan Helmet +6", "max_price": 15000000, "item_ids": ["3ee2da0f"]},
    {"name": "Mage Holy Titan Helmet +7", "max_price": 35000000, "item_ids": ["3fe2da0f"]},
    {"name": "Mage Holy Titan Helmet +8", "max_price": 220000000, "item_ids": ["40e2da0f"]},
    {"name": "Mage Holy Titan Pauldron +5", "max_price": 5000000, "item_ids": ["6ddada0f"]},
    {"name": "Mage Holy Titan Pauldron +6", "max_price": 15000000, "item_ids": ["6edada0f"]},
    {"name": "Mage Holy Titan Pauldron +7", "max_price": 35000000, "item_ids": ["6fdada0f"]},
    {"name": "Mage Holy Titan Pauldron +8", "max_price": 220000000, "item_ids": ["70dada0f"]},
    {"name": "Mage Holy Titan Pauldron Reb+1", "max_price": 35000000, "item_ids": ["07717310"]},
    {"name": "Mage Holy Titan Pauldron Reb+2", "max_price": 60000000, "item_ids": ["08717310"]},
    {"name": "Mage Holy Titan Pauldron Reb+3", "max_price": 220000000, "item_ids": ["09717310"]},
    {"name": "Mage Holy Titan Pauldron Reb+4", "max_price": 220000000, "item_ids": ["0a717310"]},
    {"name": "Mage Holy Titan Pauldron Reb+5", "max_price": 220000000, "item_ids": ["0b717310"]},
    {"name": "Mage Holy Titan Pads +5", "max_price": 5000000, "item_ids": ["49e0da0f", "55deda0f"]},
    {"name": "Mage Holy Titan Pads +6", "max_price": 15000000, "item_ids": ["4ae0da0f", "56deda0f"]},
    {"name": "Mage Holy Titan Pads +7", "max_price": 35000000, "item_ids": ["4be0da0f", "57deda0f"]},
    {"name": "Mage Holy Titan Pads +8", "max_price": 220000000, "item_ids": ["4ce0da0f", "58deda0f"]},
    {"name": "Mage Holy Titan Boots +5", "max_price": 5000000, "item_ids": ["0deada0f"]},
    {"name": "Mage Holy Titan Boots +6", "max_price": 15000000, "item_ids": ["0eeada0f"]},
    {"name": "Mage Holy Titan Boots +7", "max_price": 35000000, "item_ids": ["0feada0f"]},
    {"name": "Mage Holy Titan Boots +8", "max_price": 220000000, "item_ids": ["10eada0f"]},
    {"name": "Mage Holy Titan Gauntlets +5", "max_price": 5000000, "item_ids": ["19e8da0f", "25e6da0f"]},
    {"name": "Mage Holy Titan Gauntlets +6", "max_price": 15000000, "item_ids": ["1ae8da0f", "26e6da0f"]},
    {"name": "Mage Holy Titan Gauntlets +7", "max_price": 35000000, "item_ids": ["1be8da0f", "27e6da0f"]},
    {"name": "Mage Holy Titan Gauntlets +8", "max_price": 220000000, "item_ids": ["1ce8da0f", "28e6da0f"]},
    {"name": "Mage Holy Titan Gauntlets Reb+1", "max_price": 35000000, "item_ids": ["bf7c7310"]},
    {"name": "Mage Holy Titan Gauntlets Reb+2", "max_price": 60000000, "item_ids": ["c07c7310"]},
    {"name": "Mage Holy Titan Gauntlets Reb+3", "max_price": 220000000, "item_ids": ["c17c7310"]},
    {"name": "Mage Holy Titan Gauntlets Reb+4", "max_price": 220000000, "item_ids": ["c27c7310"]},
    {"name": "Mage Holy Titan Gauntlets Reb+5", "max_price": 220000000, "item_ids": ["c37c7310"]},
    {"name": "Mage Titan Helmet +5", "max_price": 500000, "item_ids": ["fd9fcb0f", "f1a1cb0f"]},
    {"name": "Mage Titan Helmet +6", "max_price": 5000000, "item_ids": ["fe9fcb0f", "f2a1cb0f"]},
    {"name": "Mage Titan Helmet +7", "max_price": 10000000, "item_ids": ["ff9fcb0f", "f3a1cb0f"]},
    {"name": "Mage Titan Helmet +8", "max_price": 220000000, "item_ids": ["009fcb0f", "f4a1cb0f"]},
    {"name": "Mage Titan Helmet Reb+1", "max_price": 10000000, "item_ids": ["97366410"]},
    {"name": "Mage Titan Helmet Reb+2", "max_price": 40000000, "item_ids": ["98366410"]},
    {"name": "Mage Titan Helmet Reb+3", "max_price": 70000000, "item_ids": ["99366410"]},
    {"name": "Mage Titan Helmet Reb+4", "max_price": 220000000, "item_ids": ["9a366410"]},
    {"name": "Mage Titan Helmet Reb+5", "max_price": 220000000, "item_ids": ["9b366410"]},
    {"name": "Mage Titan Pauldron +5", "max_price": 500000, "item_ids": ["2d98cb0f", "219acb0f"]},
    {"name": "Mage Titan Pauldron +6", "max_price": 5000000, "item_ids": ["2e98cb0f", "229acb0f"]},
    {"name": "Mage Titan Pauldron +7", "max_price": 10000000, "item_ids": ["2f98cb0f", "239acb0f"]},
    {"name": "Mage Titan Pauldron +8", "max_price": 220000000, "item_ids": ["3098cb0f", "249acb0f"]},
    {"name": "Mage Titan Pauldron Reb+1", "max_price": 10000000, "item_ids": ["c72e6410"]},
    {"name": "Mage Titan Pauldron Reb+2", "max_price": 40000000, "item_ids": ["c82e6410"]},
    {"name": "Mage Titan Pauldron Reb+3", "max_price": 70000000, "item_ids": ["c92e6410"]},
    {"name": "Mage Titan Pauldron Reb+4", "max_price": 220000000, "item_ids": ["ca2e6410"]},
    {"name": "Mage Titan Pauldron Reb+5", "max_price": 220000000, "item_ids": ["cb2e6410"]},
    {"name": "Mage Titan Pads +5", "max_price": 500000, "item_ids": ["099ecb0f", "159ccb0f"]},
    {"name": "Mage Titan Pads +6", "max_price": 5000000, "item_ids": ["0a9ecb0f", "169ccb0f"]},
    {"name": "Mage Titan Pads +7", "max_price": 10000000, "item_ids": ["0b9ecb0f", "179ccb0f"]},
    {"name": "Mage Titan Pads +8", "max_price": 220000000, "item_ids": ["0c9ecb0f", "189ccb0f"]},
    {"name": "Mage Titan Pads Reb+1", "max_price": 10000000, "item_ids": ["af326410"]},
    {"name": "Mage Titan Pads Reb+2", "max_price": 40000000, "item_ids": ["b0326410"]},
    {"name": "Mage Titan Pads Reb+3", "max_price": 70000000, "item_ids": ["b1326410"]},
    {"name": "Mage Titan Pads Reb+4", "max_price": 220000000, "item_ids": ["b2326410"]},
    {"name": "Mage Titan Pads Reb+5", "max_price": 220000000, "item_ids": ["b3326410"]},
    {"name": "Mage Titan Boots +5", "max_price": 500000, "item_ids": ["c1a9cb0f", "cda7cb0f"]},
    {"name": "Mage Titan Boots +6", "max_price": 5000000, "item_ids": ["c2a9cb0f", "cea7cb0f"]},
    {"name": "Mage Titan Boots +7", "max_price": 10000000, "item_ids": ["c3a9cb0f", "cfa7cb0f"]},
    {"name": "Mage Titan Boots +8", "max_price": 220000000, "item_ids": ["c4a9cb0f", "d0a7cb0f"]},
    {"name": "Mage Titan Gauntlets +5", "max_price": 500000, "item_ids": ["d9a5cb0f"]},
    {"name": "Mage Titan Gauntlets +6", "max_price": 5000000, "item_ids": ["daa5cb0f"]},
    {"name": "Mage Titan Gauntlets +7", "max_price": 500000, "item_ids": ["dba5cb0f"]},
    {"name": "Mage Titan Gauntlets +8", "max_price": 220000000, "item_ids": ["dca5cb0f"]},
    {"name": "Mage Half Guard Helmet +7", "max_price": 1000000, "item_ids": ["51db9d0f", "3fd99d0f"]},
    {"name": "Mage Half Guard Helmet +8", "max_price": 20000000, "item_ids": ["52db9d0f", "40d99d0f"]},
    {"name": "Mage Half Guard Helmet +9", "max_price": 220000000, "item_ids": ["41d99d0f", "53db9d0f"]},
    {"name": "Mage Half Guard Pauldron +7", "max_price": 1000000, "item_ids": ["6fd19d0f"]},
    {"name": "Mage Half Guard Pauldron +8", "max_price": 20000000, "item_ids": ["70d19d0f"]},
    {"name": "Mage Half Guard Pauldron +9", "max_price": 220000000, "item_ids": ["71d19d0f"]},
    {"name": "Mage Half Guard Pads +7", "max_price": 1000000, "item_ids": ["57d59d0f"]},
    {"name": "Mage Half Guard Pads +8", "max_price": 20000000, "item_ids": ["58d59d0f"]},
    {"name": "Mage Half Guard Pads +9", "max_price": 220000000, "item_ids": ["59d59d0f"]},
    {"name": "Mage Half Guard Boots +7", "max_price": 1000000, "item_ids": ["21e39d0f", "0fe19d0f"]},
    {"name": "Mage Half Guard Boots +8", "max_price": 20000000, "item_ids": ["10e19d0f", "22e39d0f"]},
    {"name": "Mage Half Guard Boots +9", "max_price": 220000000, "item_ids": ["11e19d0f", "23e39d0f"]},
    {"name": "Mage Half Guard Gauntlets +7", "max_price": 1000000, "item_ids": ["39df9d0f", "27dd9d0f"]},
    {"name": "Mage Half Guard Gauntlets +8", "max_price": 20000000, "item_ids": ["28dd9d0f", "3adf9d0f"]},
    {"name": "Mage Half Guard Gauntlets +9", "max_price": 220000000, "item_ids": ["29dd9d0f", "3bdf9d0f"]},
    {"name": "Mage Fabric Helmet +7", "max_price": 1000000, "item_ids": ["ff968e0f", "11998e0f"]},
    {"name": "Mage Fabric Helmet +8", "max_price": 20000000, "item_ids": ["00968e0f", "12998e0f"]},
    {"name": "Mage Fabric Helmet +9", "max_price": 120000000, "item_ids": ["01968e0f", "13998e0f"]},
    {"name": "Mage Fabric Pauldron +7", "max_price": 1000000, "item_ids": ["81d39d0f", "23918e0f", "41918e0f"]},
    {"name": "Mage Fabric Pauldron +8", "max_price": 20000000, "item_ids": ["82d39d0f", "24918e0f", "42918e0f"]},
    {"name": "Mage Fabric Pauldron +9", "max_price": 120000000, "item_ids": ["43918e0f", "83d39d0f", "25918e0f"]},
    {"name": "Mage Fabric Pads +7", "max_price": 1000000, "item_ids": ["17938e0f", "29958e0f"]},
    {"name": "Mage Fabric Pads +8", "max_price": 20000000, "item_ids": ["18938e0f", "2a958e0f"]},
    {"name": "Mage Fabric Pads +9", "max_price": 120000000, "item_ids": ["19938e0f", "2b958e0f"]},
    {"name": "Mage Fabric Boots +7", "max_price": 1000000, "item_ids": ["e1a08e0f", "cf9e8e0f", "c3a08e0f"]},
    {"name": "Mage Fabric Boots +8", "max_price": 20000000, "item_ids": ["e2a08e0f", "d09e8e0f", "c4a08e0f"]},
    {"name": "Mage Fabric Boots +9", "max_price": 120000000, "item_ids": ["e3a08e0f", "d19e8e0f", "c5a08e0f"]},
    {"name": "Mage Fabric Gauntlets +7", "max_price": 1000000, "item_ids": ["db9c8e0f", "f99c8e0f"]},
    {"name": "Mage Fabric Gauntlets +8", "max_price": 20000000, "item_ids": ["dc9c8e0f", "fa9c8e0f"]},
    {"name": "Mage Fabric Gauntlets +9", "max_price": 120000000, "item_ids": ["dd9c8e0f", "fb9c8e0f"]},
    {"name": "SKILL QUEST +0", "max_price": 50000000, "item_ids": ["c03da516"]},
    {"name": "Low Mastery CR BOX +0", "max_price": 3000000, "item_ids": ["88f47206"]},
    {"name": "Middle Mastery CR BOX +0", "max_price": 3000000, "item_ids": ["70f87206"]},
    {"name": "High Mastery CR BOX +0", "max_price": 5000000, "item_ids": ["58fc7206"]},
    {"name": "Red Chest +0", "max_price": 1000000, "item_ids": ["506e9916"]},
    {"name": "Green Chest +0", "max_price": 2000000, "item_ids": ["38729916"]},
    {"name": "Blue Chest +0", "max_price": 3000000, "item_ids": ["20769916"]},
    {"name": "Fragment of Blaze LWL 1 +0", "max_price": 1000000, "item_ids": ["401c3217"]},
    {"name": "Fragment of Mirage LWL 2 +0", "max_price": 2000000, "item_ids": ["28203217"]},
    {"name": "Fragment of Thnder LWL 3 +0", "max_price": 3000000, "item_ids": ["10243217"]},
    {"name": "Fragment of Eclipse LWL 4 +0", "max_price": 4000000, "item_ids": ["f8273217"]},
    {"name": "Fragment of Tempest LWL 5 +0", "max_price": 7000000, "item_ids": ["e02b3217"]},
    {"name": "Fragment of Aurora LWL 6 +0", "max_price": 8000000, "item_ids": ["c82f3217"]},
    {"name": "Fragment of Obsidian LWL 7 +0", "max_price": 1000000, "item_ids": ["b0333217"]},
    {"name": "Silver Gem LWL 6 +0", "max_price": 3000000, "item_ids": ["e0a83217"]},
    {"name": "Red Gem LWL 5 +0", "max_price": 2000000, "item_ids": ["c8ac3217"]},
    {"name": "Sunlight Gem LWL 4 +0", "max_price": 1000000, "item_ids": ["b0b03217"]},
    {"name": "High CR BOX +0", "max_price": 4000000, "item_ids": ["a0f7491e"]},
    {"name": "Low CR BOX +0", "max_price": 2000000, "item_ids": ["b8704a1e"]},
    {"name": "Middle CR BOX +0", "max_price": 3000000, "item_ids": ["78344b30"]},
    {"name": "Mystic Jewel +0", "max_price": 10000000, "item_ids": ["d02eb929"]},
    {"name": "Legendary Cape +0", "max_price": 20000000, "item_ids": ["90d57006"]},
    {"name": "Full Premium +0", "max_price": 20000000, "item_ids": ["10b6b335"]},
    {"name": "Clan Premium +0", "max_price": 100000000, "item_ids": ["d0f2c913"]},
    {"name": "Talisman +0", "max_price": 10000000, "item_ids": ["90049b16"]},
    {"name": "Lucky Tried +0", "max_price": 10000000, "item_ids": ["284ab929"]},
    {"name": "Storem Mp Pot +0", "max_price": 1000000, "item_ids": ["c0c53517"]},
    {"name": "Character Seal Scrool +0", "max_price": 25000000, "item_ids": ["98b9b02f"]},
]
# =============================================

def log(msg):
    ts = datetime.now().strftime('%H:%M:%S')
    print(f"[{ts}] {msg}", flush=True)

# ── VERSIYON KONTROL & OTOMATIK GUNCELLEME ───────────────────────
def check_update():
    try:
        ctx = _ssl._create_unverified_context()
        with urllib.request.urlopen(GITHUB_RAW_URL, timeout=10, context=ctx) as r:
            new_code = r.read().decode("utf-8")
        # VERSION satirini bul
        for line in new_code.splitlines():
            if line.startswith("VERSION"):
                new_ver = line.split("=")[1].strip().strip('"').strip("'")
                if new_ver != VERSION:
                    log(f"  Yeni versiyon bulundu: {new_ver} (mevcut: {VERSION})")
                    log("  Script guncelleniyor...")
                    with open(SCRIPT_PATH, "w", encoding="utf-8") as f:
                        f.write(new_code)
                    log("  Guncellendi! Yeniden baslatiliyor...")
                    os.execv(sys.executable, [sys.executable, SCRIPT_PATH])
                else:
                    log(f"  Versiyon guncel: {VERSION}")
                return
    except Exception as e:
        log(f"  Guncelleme kontrolu basarisiz: {e}")

# ── TCPDUMP (dogrudan telefon icinde) ────────────────────────────
def run_shell(cmd):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, timeout=20)
        return r
    except Exception as e:
        log(f"Shell hata: {e}")
        return None

def start_tcpdump():
    log("Tcpdump baslatiliyor...")
    # Termux tcpdump yolu
    tcpdump_bin = "/data/data/com.termux/files/usr/bin/tcpdump"
    run_shell("su -c 'killall tcpdump 2>/dev/null'")
    time.sleep(1)
    run_shell(f"su -c 'rm -f {PCAP_PATH}'")
    run_shell("su -c 'chmod 755 /data/local/tmp'")
    run_shell(f"chmod 755 {tcpdump_bin} 2>/dev/null")
    proc = subprocess.Popen(
        f"su -c '{tcpdump_bin} -i any -s 0 tcp -w {PCAP_PATH}'",
        shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    time.sleep(2)
    log(f"  Tcpdump aktif (PID: {proc.pid})")
    return proc

def get_pcap_size():
    try:
        r = run_shell(f"su -c 'wc -c {PCAP_PATH} 2>/dev/null'")
        if r and r.stdout:
            parts = r.stdout.decode("utf-8", errors="ignore").strip().split()
            if parts:
                return int(parts[0])
    except:
        pass
    return 0

def pull_pcap():
    # Termux: pcap zaten telefonda, direkt oku
    try:
        # Okunabilir yap
        run_shell(f"su -c 'chmod 644 {PCAP_PATH}'")
        # Termux home'a kopyala
        local = os.path.join(os.path.expanduser("~"), "alarm_scan.pcap")
        run_shell(f"su -c 'cp {PCAP_PATH} {local} && chmod 644 {local}'")
        if os.path.exists(local) and os.path.getsize(local) > 24:
            run_shell(f"su -c 'rm -f {PCAP_PATH}'")
            return local
    except Exception as e:
        log(f"  Pcap kopyalama hatasi: {e}")
    return None

def read_packets(path):
    packets = []
    link_type = 1
    try:
        with open(path, "rb") as f:
            magic = f.read(4)
            if len(magic) < 4: return packets, link_type
            endian = "<" if magic == b"\xd4\xc3\xb2\xa1" else ">"
            gh = f.read(20)
            if len(gh) == 20:
                link_type = struct.unpack(endian + "I", gh[16:20])[0]
            while True:
                hdr = f.read(16)
                if len(hdr) < 16: break
                _, _, incl_len, _ = struct.unpack(endian + "IIII", hdr)
                data = f.read(incl_len)
                if len(data) == incl_len:
                    packets.append(data)
    except Exception as e:
        log(f"Pcap okuma hatasi: {e}")
    return packets, link_type

def extract_server_payloads(packets, link_type=1):
    result = b""
    for pkt in packets:
        try:
            if len(pkt) < 20: continue
            if link_type == 276:
                # LINUX_SLL2: 20 byte header, EtherType at bytes 0-1
                if len(pkt) < 20: continue
                et = struct.unpack(">H", pkt[0:2])[0]
                if et != 0x0800: continue
                ip_start = 20
            elif link_type == 113:
                # LINUX_SLL: 16 byte header, EtherType at bytes 14-15
                if len(pkt) < 16: continue
                et = struct.unpack(">H", pkt[14:16])[0]
                if et != 0x0800: continue
                ip_start = 16
            else:
                # Ethernet: EtherType at bytes 12-13
                if len(pkt) < 14: continue
                et = struct.unpack(">H", pkt[12:14])[0]
                if et != 0x0800: continue
                ip_start = 14
            if len(pkt) <= ip_start + 20: continue
            if (pkt[ip_start] >> 4) != 4: continue
            ihl      = (pkt[ip_start] & 0x0F) * 4
            proto    = pkt[ip_start + 9]
            if proto != 6: continue
            tcp_start = ip_start + ihl
            if len(pkt) <= tcp_start + 20: continue
            data_off  = ((pkt[tcp_start + 12] >> 4) & 0xF) * 4
            payload   = pkt[tcp_start + data_off:]
            if len(payload) >= 10: result += payload
        except: pass
    return result

def parse_market_records(data):
    records, seen, n, i = [], set(), len(data), 0
    while i < n - 22:
        if data[i] == 0xaa and i + 1 < n and data[i+1] == 0x55:
            i += 2; continue
        if i + 2 > n: break
        name_len = struct.unpack("<H", data[i:i+2])[0]
        if not (2 <= name_len <= 25):
            i += 1; continue
        name_start = i + 2
        name_end   = name_start + name_len * 2
        if name_end + 20 > n:
            i += 1; continue
        try:
            name = data[name_start:name_end].decode("utf-16-le")
        except:
            i += 1; continue
        if not (all(32 <= ord(c) < 127 for c in name) and len(name) >= 2):
            i += 1; continue
        j = name_end
        item_count = 0
        while j + 20 <= n:
            item_id = data[j+1:j+5].hex()
            price   = struct.unpack("<I", data[j+9:j+13])[0]
            if 10_000 <= price <= 9_999_999_999 and all(x == 0 for x in data[j+13:j+20]):
                key = (name, item_id, price)
                if key not in seen:
                    seen.add(key)
                    records.append({"seller": name, "item_id": item_id, "price": price})
                item_count += 1
                j += 20
            else:
                break
        if item_count > 0:
            i = j
        else:
            i += 1
    return records

def check_alarms(records):
    if not records:
        log("  Kayit bulunamadi.")
        return
    log(f"  {len(records)} kayit / {len(set(r['item_id'] for r in records))} unique ID analiz ediliyor...")
    cheapest = {}
    for r in records:
        iid = r["item_id"]
        if iid not in cheapest or r["price"] < cheapest[iid]["price"]:
            cheapest[iid] = r
    all_alarm_ids = set(iid for alarm in ALARM_LIST for iid in alarm["item_ids"])
    fired = 0
    for alarm in ALARM_LIST:
        hits = [cheapest[iid] for iid in alarm["item_ids"] if iid in cheapest]
        if not hits: continue
        best = min(hits, key=lambda x: x["price"])
        if best["price"] <= alarm["max_price"]:
            fire_alarm(alarm["name"], best["seller"], best["price"], alarm["max_price"])
            fired += 1
        else:
            pct = best["price"] / alarm["max_price"] * 100
            log(f"  x {alarm['name']:<35} {best['price']:>14,}  (esik {alarm['max_price']:,}  %{pct:.0f})")
    unknown = {iid: cheapest[iid] for iid in cheapest if iid not in all_alarm_ids}
    if unknown:
        log(f"  [{len(unknown)} bilinmeyen ID pazarda goruldu]")
    if fired == 0: log("  -> Esik altinda alarm yok.")
    else:          log(f"  *** {fired} ALARM ATESLENEDI! ***")

def send_telegram(text):
    try:
        url     = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = _json.dumps({"chat_id": TELEGRAM_CHAT_ID, "text": text}).encode("utf-8")
        req     = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
        ctx     = _ssl._create_unverified_context()
        with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
            body = resp.read().decode("utf-8")
            if '"ok":true' in body:
                log("  Telegram gonderildi.")
            else:
                log(f"  Telegram hatasi: {body[:200]}")
    except Exception as e:
        log(f"  Telegram hatasi: {e}")

def fire_alarm(item_name, seller, price, max_price):
    log(f"  *** ALARM *** {item_name}  |  {seller}  |  {price:,} gold")
    msg = (
        "NOWA PAZAR ALARMI!\n\n"
        f"Item  : {item_name}\n"
        f"Satan : {seller}\n"
        f"Fiyat : {price:,} gold\n"
        f"Esik  : {max_price:,} gold\n\n"
        "Hemen pazari ac!"
    )
    send_telegram(msg)

def main():
    log("=" * 60)
    log("  NOWA ONLINE - PAZAR ALARM SISTEMI (Termux)")
    log(f"  Versiyon: {VERSION}")
    log("=" * 60)
    log(f"  Alarm sayisi  : {len(ALARM_LIST)}")
    log(f"  Toplam item_id: {sum(len(a['item_ids']) for a in ALARM_LIST)}")
    log("")

    # Versiyon kontrolu
    log("Guncelleme kontrol ediliyor...")
    check_update()
    log("")

    # Telegram testi
    log("Telegram test ediliyor...")
    send_telegram(f"NOWA Alarm baslatildi (v{VERSION}). {len(ALARM_LIST)} alarm aktif.")
    log("")

    scan_no      = 0
    tcpdump_proc = None
    last_update_check = time.time()
    UPDATE_CHECK_INTERVAL = 60  # Her 60 saniyede versiyon kontrol et

    BURST_THRESHOLD = 15_000
    BURST_END_SECS  = 3

    try:
        while True:
            if tcpdump_proc is None or tcpdump_proc.poll() is not None:
                tcpdump_proc = start_tcpdump()
                log("Dinleniyor... Pazar persomenini ac.")

            prev_size     = get_pcap_size()
            in_burst      = False
            burst_end_cnt = 0

            while True:
                time.sleep(1)

                # Versiyon kontrolu (her 60sn)
                if time.time() - last_update_check >= UPDATE_CHECK_INTERVAL:
                    last_update_check = time.time()
                    log("Guncelleme kontrol ediliyor...")
                    check_update()  # Yeni versiyon varsa buradan yeniden baslatir

                sz   = get_pcap_size()
                diff = sz - prev_size
                prev_size = sz

                if diff >= BURST_THRESHOLD:
                    if not in_burst:
                        log(f"  >>> Pazar verisi geliyor! ({diff//1024}KB/sn)")
                        in_burst = True
                    burst_end_cnt = 0
                elif in_burst:
                    burst_end_cnt += 1
                    if burst_end_cnt >= BURST_END_SECS:
                        log(f"  Burst bitti, analiz basliyor...")
                        break
                else:
                    pass

            scan_no += 1
            log(f"\nTarama #{scan_no}")
            local_pcap = pull_pcap()
            if not local_pcap:
                log("  Pcap alinamadi.")
                in_burst = False
                burst_end_cnt = 0
                continue

            pkts, link_type = read_packets(local_pcap)
            payload = extract_server_payloads(pkts, link_type)
            log(f"  {len(pkts)} paket / {len(payload):,} byte server verisi")

            # Gecici dosyayi temizle
            try: os.remove(local_pcap)
            except: pass

            if len(payload) == 0:
                log("  Server verisi bos.")
            else:
                recs = parse_market_records(payload)
                check_alarms(recs)

            log("  30sn sonra persomeni tekrar ac.")
            log("")
            run_shell("su -c 'killall tcpdump 2>/dev/null'")
            time.sleep(2)
            tcpdump_proc  = None
            in_burst      = False
            burst_end_cnt = 0

    except KeyboardInterrupt:
        log("\nKullanici durdurdu.")
    except Exception as e:
        log(f"\nBeklenmeyen hata: {e}")
        import traceback
        traceback.print_exc()
    finally:
        log("Tcpdump durduruluyor...")
        run_shell("su -c 'killall tcpdump 2>/dev/null'")
        log("Sistem durduruldu.")

if __name__ == "__main__":
    main()
