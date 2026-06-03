# 🤖 CRYPTO BOT MEXC - Enterprise Trading Bot

> **Trading Bot AI nhẹ, Async, CPU-only cho MEXC**
>
> Chạy trên CPU, không cần GPU. Đầy đủ AI: Q-Learning + XGBoost + LightGBM + Ollama LLM

## 🚀 Tính Năng Chính

### 📊 Trading
- ✅ **2 cặp song parallel**: BTC/USDT + ETH/USDT
- ✅ **Multi-timeframe**: 1m + 5m + 15m xác nhận
- ✅ **Paper → Live tự động**: Win rate > 55% → Live
- ✅ **Async + Event-driven**: Xử lý realtime
- ✅ **RabbitMQ**: Message queue production-ready

### 🧠 AI/ML
- ✅ **Q-Learning**: Học từ mỗi trade
- ✅ **XGBoost + LightGBM**: Dự đoán tín hiệu
- ✅ **Ollama Phi-3**: LLM local (CPU friendly)
- ✅ **10+ Indicators**: RSI, MACD, BB, ATR, Ichimoku, v.v
- ✅ **Signal Fusion**: Kết hợp đa source

### 💰 Risk Management
- ✅ **Position Sizing**: Tính theo % balance
- ✅ **Compound**: Lãi kép tự động
- ✅ **Per-trade SL/TP**: 1.5% loss / 0.8% profit
- ✅ **Daily Loss Control**: Stop nếu thua > 5%/ngày
- ✅ **Circuit Breaker**: Dừng nếu API fail

### 📈 Monitoring
- ✅ **Daily Summary**: Tổng kết 23:59 gửi Telegram
- ✅ **Per-trade Notification**: Mỗi lệnh đều notify
- ✅ **LLM Explanation**: Giải thích tại sao vào lệnh
- ✅ **Adaptive Optimizer**: Backtest + retrain mỗi 6h
- ✅ **Health Check**: Ping API mỗi 30s

### 🗄️ Database
- ✅ **Dev**: SQLite (zero config)
- ✅ **Prod**: TimescaleDB (high performance)
- ✅ **Auto-routing**: Tự chọn theo mode

## 📦 Cài Đặt

### 1️⃣ Clone & Setup

```bash
git clone https://github.com/von843993-pixel/crypto_bot_mexc.git
cd crypto_bot_mexc

python -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc venv\\Scripts\\activate  # Windows

pip install -r requirements.txt
cp .env.example .env
```

### 2️⃣ Config .env

```bash
# MEXC API
MEXC_API_KEY=your_key
MEXC_API_SECRET=your_secret
MEXC_TESTNET=true

# Telegram
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

### 3️⃣ Cài Ollama (Optional)

```bash
# Download từ https://ollama.ai
ollama pull phi3
ollama serve
```

### 4️⃣ Chạy Paper Trading

```bash
TRADING_MODE=paper python src/main.py
```

## 🏗️ Kiến Trúc

```
PERCEPTION LAYER (Indicators)
├── RSI Adaptive, MACD, EMA Crossover
├── ADX, Ichimoku, Keltner Channel
└── Volume Analysis, Regime Detection
        ↓
SIGNAL FUSION LAYER
├── Weighted Voting (10+ indicators)
├── XGBoost Score (0-1)
└── LightGBM Score (0-1)
        ↓
AI DECISION LAYER
├── Q-Learning Agent (RL)
├── LLM Explanation (Ollama)
└── Confidence Score
        ↓
RISK MANAGEMENT
├── Position Sizer, SL/TP
├── Compound Engine
└── Loss Controller
        ↓
EXECUTION
├── Order Placement
├── Real-time Monitoring
├── Trade Journal
└── Daily Summary
```

## 📝 Luồng Trading Chính

### Mỗi 1 phút:
1. Lấy candle mới từ MEXC
2. Cập nhật 3 timeframe (1m, 5m, 15m)
3. Tính 10+ indicators
4. Fusion signal từ 3 source
5. RL agent quyết định
6. LLM giải thích
7. Risk check
8. Vào lệnh
9. Gửi Telegram
10. Cập nhật DB

## 📊 Telegram Commands

```
/status          → Trạng thái bot
/balance         → Số dư realtime
/trades          → Danh sách trades
/stop            → Dừng bot
/paper           → Paper mode
/live            → Live mode
/explain         → LLM giải thích
/retrain         → Train lại model
```

## 🔧 Technology Stack

| Layer | Tech |
|-------|------|
| **Exchange** | CCXT |
| **Data** | Pandas, NumPy |
| **Indicators** | TA-Lib |
| **ML** | XGBoost, LightGBM |
| **RL** | Gymnasium |
| **LLM** | Ollama + Phi-3 |
| **Database** | SQLite / TimescaleDB |
| **Queue** | RabbitMQ |
| **Async** | asyncio |
| **Monitoring** | Prometheus |

## ⚠️ Risk Disclaimer

```
⚠️  DISCLAIMER:
- This bot trades with REAL money if set to LIVE mode
- Past performance ≠ future results
- Crypto trading is high-risk
- Start with PAPER mode 1-2 weeks
- Use only money you can afford to lose
```

## 📄 License

MIT License - See LICENSE file

---

**Made with ❤️ for crypto traders**
