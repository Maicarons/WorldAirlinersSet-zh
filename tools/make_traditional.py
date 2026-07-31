#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import io, re
from opencc import OpenCC

cc = OpenCC("s2tw")  # Simplified -> Traditional (Taiwan variant)

SRC = "lang/chinese_simplified.lng"
# Output file: traditional Chinese (OpenTTD lang id 0x62 = CHINESE_TRADITIONAL)
OUT = "lang/chinese_traditional.lng"

# Taiwan-region airline naming overrides (applied AFTER s2tw conversion).
# Rationale: for the Taiwan locale, legacy/overseas carriers use local conventions.
TW = {
    "STR_VLIV_AIR_CHINA": "中國航空",
    "STR_VLIV_AIR_CHINA_CARGO": "中國貨運航空",
    "STR_VLIV_CHINA_EASTERN": "中國東方航空",
    "STR_VLIV_CHINA_SOUTHERN": "中國南方航空",
    "STR_VLIV_CHINA_WEST_AIR": "中國西部航空",
    "STR_VLIV_CATHAY_PACIFIC": "國泰航空",
    "STR_VLIV_CATHAY_PACIFIC_CARGO": "國泰航空貨運",
    "STR_VLIV_DRAGONAIR": "港龍航空",
    "STR_VLIV_HAINAN_AIRLINES": "海南航空",
    "STR_VLIV_SHADONG_AIRLINES": "山東航空",
    "STR_VLIV_SHENZHEN_AIRLINES": "深圳航空",
    "STR_VLIV_XIAMEN_AIR": "廈門航空",
    "STR_VLIV_CHINA_AIRLINES": "中華航空",
    "STR_VLIV_CHINA_AIRLINES_CARGO": "中華航空貨運",
    "STR_VLIV_AIR_MACAU": "澳門航空",
    "STR_VLIV_EVA_AIR": "長榮航空",
    "STR_VLIV_EVA_AIR_CARGO": "長榮航空貨運",
    # common global carriers localised for TW
    "STR_VLIV_AIR_FRANCE": "法國航空",
    "STR_VLIV_LUFTHANSA": "漢莎航空",
    "STR_VLIV_KLM": "荷蘭皇家航空",
    "STR_VLIV_BRITISH_AIRWAYS_UNION_FLAG": "英國航空（米字旗）",
    "STR_VLIV_BRITISH_AIRWAYS_UNION_FLAG_COMAIR": "英國航空 米字旗（Comair）",
    "STR_VLIV_AIR_NEW_ZEALAND": "紐西蘭航空",
    "STR_VLIV_AIR_AUSTRAL": "留尼旺南方航空",
    "STR_VLIV_QANTAS": "澳洲航空",
    "STR_VLIV_ANA": "全日空",
    "STR_VLIV_JAL": "日本航空",
    "STR_VLIV_SAS": "北歐航空",
    "STR_VLIV_AER_LINGUS": "愛爾蘭航空",
    "STR_VLIV_EMIRATES": "阿拉伯聯合大公國航空",
    "STR_VLIV_QATAR_AIRWAYS": "卡達航空",
    "STR_VLIV_ETIHAD_AIRWAYS": "阿提哈德航空",
    "STR_VLIV_SINGAPORE_AIRLINES": "新加坡航空",
    "STR_VLIV_KOREAN_AIR": "大韓航空",
    "STR_VLIV_ASIANA_AIRLINES": "韓亞航空",
    "STR_VLIV_GARUDA_INDONESIA": "印尼鷹航",
    "STR_VLIV_THAI_AIRWAYS_INTERNATIONAL": "泰國國際航空",
    "STR_VLIV_MALAYSIA_AIRLINES": "馬來西亞航空",
    "STR_VLIV_VIETNAM_AIRLINES": "越南航空",
    "STR_VLIV_PHILIPPINES_AIRLINES": "菲律賓航空",
    "STR_VLIV_AEROLINEAS_ARGENTINAS": "阿根廷航空",
    "STR_VLIV_AEROMEXICO": "墨西哥航空",
    "STR_VLIV_AVIANCA": "哥倫比亞航空",
    "STR_VLIV_LAN_AIRLINES": "智利國家航空",
    "STR_VLIV_LATAM": "拉塔姆航空",
    "STR_VLIV_TAM_AIRLINES": "TAM 航空",
    "STR_VLIV_GOL": "高爾航空",
    "STR_VLIV_AEROFLOG": "俄羅斯航空",
    "STR_VLIV_AEROFLOT": "俄羅斯航空",
    "STR_VLIV_TURKISH_AIRLINES": "土耳其航空",
    "STR_VLIV_SWISS": "瑞士國際航空",
    "STR_VLIV_SWISS_INTERNATIONAL_AIRLINES": "瑞士國際航空",
    "STR_VLIV_AUSTRIAN_AIRLINES": "奧地利航空",
    "STR_VLIV_FINNAIR": "芬蘭航空",
    "STR_VLIV_IBERIA": "西班牙國家航空",
    "STR_VLIV_ALITALIA": "義大利航空",
    "STR_VLIV_TAP": "葡萄牙航空",
    "STR_VLIV_BRUSSELS_AIRLINES": "布魯塞爾航空",
    "STR_VLIV_AIR_CANADA": "加拿大航空",
    "STR_VLIV_UNITED_AIRLINES": "聯合航空",
    "STR_VLIV_AMERICAN_AIRLINES": "美國航空",
    "STR_VLIV_DELTA_AIR_LINES": "達美航空",
    "STR_VLIV_SOUTHWEST_AIRLINES": "西南航空",
    "STR_VLIV_JETBLUE": "捷藍航空",
    "STR_VLIV_ALASKA_AIRLINES": "阿拉斯加航空",
    "STR_VLIV_FRONTIER_AIRLINES": "邊疆航空",
    "STR_VLIV_S7_AIRLINES": "S7 西伯利亞航空",
    "STR_VLIV_UTAIR": "UTair 航空",
}

pat = re.compile(r'^(\s*)(STR_[A-Za-z0-9_]+)(\s*):(.*)$')
hdr_done = False
out = []

with io.open(SRC, encoding="utf-8") as f:
    for line in f:
        raw = line.rstrip("\n")
        # language id header
        if raw.startswith("##grflangid"):
            out.append("##grflangid 0x62")
            hdr_done = True
            continue
        m = pat.match(raw)
        if m:
            key = m.group(2)
            tail = m.group(4)  # original value (simplified)
            if key in TW:
                val = TW[key]
            else:
                val = cc.convert(tail)
            out.append(m.group(1) + key + m.group(3) + ":" + val)
        else:
            # comments: also convert any CJK in comments for consistency
            out.append(cc.convert(raw) if any('\u4e00'<=c<='\u9fff' for c in raw) else raw)

io.open(OUT, "w", encoding="utf-8").write("\r\n".join(out) + "\r\n")
print("Wrote", OUT, "lines:", len(out))
