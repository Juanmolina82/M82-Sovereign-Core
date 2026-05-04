# -*- coding: utf-8 -*-
# M82 INTRADAY TRANSACTIONAL LOG - 27 APR 2026

class M82Data:
    def __init__(self):
        self.blocks = {
            "OSIS": {"action": "BLOCK_BUY", "vol": "10.18K", "price": 288.52},
            "PSX": {"action": "BLOCK_SALE", "vol": "14.75K", "price": 163.73},
            "CNQ": {"action": "HUGE_VOLUME", "vol": "3.2M", "status": "Accumulation"}
        }
        self.amazon_intel = {
            "X-Energy": "65.8M shares declared (Nuclear Infra)",
            "Insider_Sell": "Jonathan Rubinstein - $1M (Form 144)"
        }

    def log(self):
        print("\n" + "="*50)
        print("     M82 INTRADAY AUDIT - BLOCK TRADES & SEC")
        print("="*50)
        for ticker, data in self.blocks.items():
            print(f"• {ticker}: {data['action']} | {data['vol']} @ {data['price'] if 'price' in data else ''}")
        print("-" * 50)
        print(f"AMZN STRATEGY: {self.amazon_intel['X-Energy']}")
        print("="*50 + "\n")

if __name__ == "__main__":
    M82Data().log()
