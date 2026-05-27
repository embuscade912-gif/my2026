import urllib.request
import json
import datetime
import os

def get_stock_info(symbol, name, market_prefix):
    result = {"name": name, "symbol": symbol}
    try:
        url = f"http://qt.gtimg.cn/q={market_prefix}{symbol}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            raw = response.read().decode('gbk')
        content = raw.split('="')[1].rstrip('";\n')
        fields = content.split('~')
        result["price"] = float(fields[3])
        result["prev_close"] = float(fields[4])
        result["open"] = float(fields[5])
        result["volume"] = float(fields[6])
        result["change"] = float(fields[31])
        result["change_pct"] = float(fields[32])
        result["high"] = float(fields[33])
        result["low"] = float(fields[34])
        result["turnover"] = float(fields[38])
        result["pe_ttm"] = float(fields[39])
        result["pb"] = float(fields[46]) if len(fields) > 46 and fields[46] else 0
        result["total_mv"] = float(fields[45])
        result["date"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        trend = "上涨" if result["change_pct"] > 0 else ("下跌" if result["change_pct"] < 0 else "持平")
        result["analysis"] = f"{name}今日{trend}{abs(result['change_pct'])}%，收盘价{result['price']}元。换手率{result['turnover']}%，PE-TTM约{result['pe_ttm']}倍，总市值{result['total_mv']}亿元。建议持续关注基本面变化与行业景气度。"
        return result
    except Exception as e:
        result["error"] = str(e)
        return result


if __name__ == "__main__":
    data = {
        "阳光电源": get_stock_info("300274", "阳光电源", "sz"),
        "山东黄金": get_stock_info("600547", "山东黄金", "sh")
    }
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("✅ 数据更新成功！")
    print(json.dumps(data, ensure_ascii=False, indent=2))
