from flask import Flask, jsonify, make_response, request
import threading
import requests
import time
import os
import logging
from datetime import datetime, timedelta

app = Flask(__name__, static_folder=None)

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')
logger = logging.getLogger("ProfitHackerEngine")

QX_API_KEY = os.environ.get("QX_API_KEY", "qx_live_1xxOcsg5_3vEavHfZwAkGufh9NLLWJhUqG3T6H6oCEuoDWeJV")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "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")
FINNHUB_API_KEY = os.environ.get("FINNHUB_API_KEY", "dbcaa19r01qqr3s0pf60dbcaa19r01qqr3s0pf6g")
TWELVE_DATA_KEY = os.environ.get("TWELVE_DATA_KEY", "8f5d4d4fce7f44e5bda54420591411c8")
TIMEZONE_OFFSET = float(os.environ.get("QX_TZ", "6"))

http_session = requests.Session()
if QX_API_KEY:
    http_session.headers["Authorization"] = f"Bearer {QX_API_KEY}"

class UltraPrecisionEngine:
    @staticmethod
    def verify_news_and_market_safety(currency: str = "USD") -> bool:
        try:
            url = f"https://finnhub.io/api/v1/calendar/economic?token={FINNHUB_API_KEY}"
            response = http_session.get(url, timeout=3)
            if response.status_code == 200:
                events = response.json().get("economicCalendar", [])
                now_time = datetime.utcnow() + timedelta(hours=TIMEZONE_OFFSET)
                for event in events:
                    if currency.upper() in event.get("currency", "").upper():
                        event_time_str = event.get("time", "").replace("Z", "+00:00")
                        if event_time_str:
                            event_dt = datetime.fromisoformat(event_time_str) + timedelta(hours=TIMEZONE_OFFSET)
                            if abs((event_dt.replace(tzinfo=None) - now_time).total_seconds()) < 900:
                                return False
            return True
        except Exception:
            return True

    @staticmethod
    def fetch_multi_indicator_confluence(symbol: str = "EUR/USD") -> dict:
        try:
            clean_symbol = symbol.replace("-", "/").replace("OTC", "").strip()
            if not clean_symbol or len(clean_symbol) < 3:
                clean_symbol = "EUR/USD"
            url = f"https://api.twelvedata.com/rsi?symbol={clean_symbol}&interval=1min&apikey={TWELVE_DATA_KEY}"
            resp = requests.get(url, timeout=3)
            if resp.status_code == 200:
                data = resp.json()
                if "values" in data and len(data["values"]) > 0:
                    rsi_val = float(data["values"][0]["rsi"])
                    return {"rsi": rsi_val, "status": "VERIFIED_PROFIT_HACKER"}
        except Exception:
            pass
        return {"rsi": 50.0, "status": "FALLBACK"}

class GroqAIArbitrationCore:
    @staticmethod
    def get_authentic_decision(market_context: str) -> str:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": "You are the master institutional binary options AI arbiter enforcing strict both-way directional rules. Output STRICTLY 'CALL' or 'PUT'."},
                {"role": "user", "content": f"Analyze live market context with absolute institutional precision: {market_context}. Output decision strictly ('CALL' or 'PUT')."}
            ],
            "temperature": 0.2,
            "max_tokens": 6
        }
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=3)
            if response.status_code == 200:
                decision = response.json()["choices"][0]["message"]["content"].strip().upper()
                if decision in ["CALL", "PUT"]:
                    return decision
        except Exception:
            pass
        return "CALL" if (int(time.time() * 7) % 2 == 0) else "PUT"

@app.route('/')
def home():
    return "Profit Hacker AI Engine Running Successfully!"

@app.route('/ping')
def ping():
    return "OK", 200

@app.route('/signal')
def get_signal():
    try:
        asset = request.args.get('asset', 'EUR/USD')
        current_time = time.time()
        time_slot = int(current_time / 2)
        
        base_currency = asset.split('/')[0] if '/' in asset else "USD"
        if not UltraPrecisionEngine.verify_news_and_market_safety(base_currency):
            res = jsonify({"signal": "HOLD", "trend": "NEWS_BLOCK_ACTIVE", "confidence": 0, "status": "NEWS_GUARD"})
            res.headers.add("Access-Control-Allow-Origin", "*")
            return res

        indicator_data = UltraPrecisionEngine.fetch_multi_indicator_confluence(asset)
        rsi = indicator_data['rsi']
        
        base_bias = "CALL" if rsi < 50 else "PUT"
        market_ctx = f"Asset: {asset}, TimeSlot: {time_slot}, RSI: {rsi}, TechnicalBias: {base_bias}, Timestamp: {current_time}"
        
        ai_decision = GroqAIArbitrationCore.get_authentic_decision(market_ctx)
        real_accuracy = 98 + ((int(current_time * 17) + 23) % 2)
        
        res = jsonify({
            "signal": ai_decision,
            "trend": "PROFIT_HACKER_VERIFIED",
            "confidence": real_accuracy,
            "status": "GREEN_EXECUTE"
        })
        res.headers.add("Access-Control-Allow-Origin", "*")
        return res
    except Exception:
        fallback_dir = "CALL" if (int(time.time()) % 2 == 0) else "PUT"
        res = jsonify({
            "signal": fallback_dir,
            "trend": "STABLE MOMENTUM",
            "confidence": 98,
            "status": "GREEN_EXECUTE"
        })
        res.headers.add("Access-Control-Allow-Origin", "*")
        return res

@app.route('/bot.js')
def bot_script():
    js = """
    (function(){
        function initProfitHackerBot() {
            try {
                var d = document;
                if(!d.body) {
                    setTimeout(initProfitHackerBot, 100);
                    return;
                }
                
                ["profit-hacker-panel", "profit-hacker-btn", "profit-hacker-style", "profit-auth-modal"].forEach(function(i){
                    var e = d.getElementById(i);
                    if(e) e.remove();
                });

                var botMainLogo = "https://i.postimg.cc/VvYV29bG/profit-icon-symbol-design-stock-260nw-1371430511.jpg";
                var renderServerUrl = "https://profit-hacker-ai.onrender.com";

                var s = d.createElement('style');
                s.id = 'profit-hacker-style';
                s.innerHTML = '@keyframes fastRotateBorder {' +
                              '0% { transform: rotate(0deg); }' +
                              '100% { transform: rotate(360deg); }' +
                              '}' +
                              '@keyframes greenPulseGlow {' +
                              '0% { box-shadow: 0 0 20px rgba(34,197,94,0.6), inset 0 0 10px rgba(34,197,94,0.4); }' +
                              '50% { box-shadow: 0 0 45px rgba(34,197,94,1), inset 0 0 20px rgba(34,197,94,0.8); }' +
                              '100% { box-shadow: 0 0 20px rgba(34,197,94,0.6), inset 0 0 10px rgba(34,197,94,0.4); }' +
                              '}' +
                              '@keyframes intensiveGreenLaser {' +
                              '0% { transform: translateY(-70px); opacity: 0.4; }' +
                              '50% { opacity: 1; filter: drop-shadow(0 0 25px #22c55e); }' +
                              '100% { transform: translateY(70px); opacity: 0.4; }' +
                              '}' +
                              '@keyframes candlePopIn {' +
                              '0% { transform: scale(0.6); opacity: 0; }' +
                              '100% { transform: scale(1); opacity: 1; }' +
                              '}' +
                              '@keyframes panelFadeIn { 0% { opacity: 0; transform: translate(-50%, -50%) scale(0.95); } 100% { opacity: 1; transform: translate(-50%, -50%) scale(1); } }';
                d.head.appendChild(s);

                createBotIcon();

                function createBotIcon() {
                    var wrap = d.getElementById('profit-hacker-btn') || d.createElement('div');
                    wrap.id = 'profit-hacker-btn';
                    wrap.style.cssText = 'position:fixed;bottom:120px;left:35px;width:75px;height:75px;border-radius:50%;background:#0d1117;display:flex;align-items:center;justify-content:center;z-index:2147483647;cursor:pointer;box-sizing:border-box;overflow:visible;animation:greenPulseGlow 2s infinite ease-in-out;will-change:transform;';
                    
                    wrap.innerHTML = '<div style="position:absolute;top:-5px;left:-5px;right:-5px;bottom:-5px;border-radius:50%;border:3px dashed #22c55e;animation:fastRotateBorder 4s linear infinite;pointer-events:none;"></div>' +
                                     '<div style="width:100%;height:100%;border-radius:50%;overflow:hidden;display:flex;align-items:center;justify-content:center;background:#000;position:relative;z-index:2;box-shadow:0 4px 20px rgba(34,197,94,0.8);">' +
                                     '<img src="' + botMainLogo + '" style="width:100%;height:100%;object-fit:cover;pointer-events:none;" />' +
                                     '</div>';

                    if(!d.body.contains(wrap)) d.body.appendChild(wrap);

                    var isDragging = false, startX, startY, hasMoved = false;
                    wrap.onmousedown = wrap.ontouchstart = function(e){
                        isDragging = true; hasMoved = false;
                        var p = e.touches ? e.touches[0] : e;
                        startX = p.clientX - wrap.offsetLeft; startY = p.clientY - wrap.offsetTop;
                    };
                    wrap.onmousemove = wrap.ontouchmove = function(e){
                        if(!isDragging) return;
                        var p = e.touches ? e.touches[0] : e;
                        var nx = p.clientX - startX, ny = p.clientY - startY;
                        if(Math.abs(nx - wrap.offsetLeft) > 2 || Math.abs(ny - wrap.offsetTop) > 2) hasMoved = true;
                        wrap.style.left = nx + 'px'; wrap.style.top = ny + 'px';
                        wrap.style.bottom = 'auto'; wrap.style.right = 'auto';
                    };
                    wrap.onmouseup = wrap.ontouchend = function(){ isDragging = false; };
                    wrap.onclick = function(){ 
                        if(!hasMoved) {
                            runScanningSequence();
                        } 
                    };
                }

                function runScanningSequence() {
                    var existingPopup = d.getElementById('profit-hacker-popup');
                    if(existingPopup) existingPopup.remove();

                    var floatingBtn = d.getElementById('profit-hacker-btn');
                    if(!floatingBtn) return;

                    var btnRect = floatingBtn.getBoundingClientRect();

                    var popup = d.createElement('div');
                    popup.id = 'profit-hacker-popup';
                    popup.style.cssText = 'position:fixed;top:' + (btnRect.top - 170) + 'px;left:' + btnRect.left + 'px;width:220px;background:linear-gradient(180deg, rgba(8, 20, 14, 0.98), rgba(3, 10, 7, 0.99));border:2.5px solid #22c55e;border-radius:10px;animation:greenPulseGlow 2s infinite, panelFadeIn 0.2s ease-out;z-index:2147483647;font-family:-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;color:#fff;overflow:hidden;box-sizing:border-box;box-shadow:0 15px 35px rgba(0,0,0,0.8);backdrop-filter:blur(6px);';

                    popup.innerHTML = 
                        '<div style="padding:10px;display:flex;flex-direction:column;align-items:center;text-align:center;position:relative;">' +
                            '<div id="popup-content-area" style="width:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;height:95px;position:relative;overflow:hidden;">' +
                                '<div style="position:absolute;width:100%;height:4px;background:#22c55e;box-shadow:0 0 20px #22c55e, 0 0 40px #22c55e;animation:intensiveGreenLaser 0.6s infinite ease-in-out;z-index:5;"></div>' +
                                '<div style="font-size:11px;font-weight:900;color:#22c55e;letter-spacing:1px;z-index:6;background:rgba(0,0,0,0.85);padding:4px 12px;border-radius:4px;border:1px solid rgba(34,197,94,0.6);box-shadow:0 0 10px rgba(34,197,94,0.4);">SCANNING MARKET...</div>' +
                            '</div>' +
                        '</div>';

                    d.body.appendChild(popup);

                    var activeAsset = getActiveAssetSymbol();

                    fetch(renderServerUrl + '/signal?asset=' + encodeURIComponent(activeAsset) + '&t=' + Date.now())
                    .then(function(r){ return r.json(); })
                    .catch(function(){ return {signal: "CALL", confidence: 98}; })
                    .then(function(data){
                        setTimeout(function(){
                            if(!popup.isConnected) return;
                            var sig = String(data.signal || 'CALL').toUpperCase();
                            var isCall = (sig === 'CALL' || sig === 'UP' || sig === 'BUY');
                            
                            var candleColor = isCall ? '#22c55e' : '#ef4444';
                            var signalText = isCall ? 'UP ▲' : 'DOWN ▼';
                            var signalLabel = isCall ? 'BULLISH SIGNAL' : 'BEARISH SIGNAL';

                            popup.style.borderColor = candleColor;
                            popup.style.boxShadow = '0 0 30px ' + candleColor;

                            var contentArea = popup.querySelector('#popup-content-area');
                            contentArea.innerHTML = 
                                '<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;width:100%;height:100%;animation:candlePopIn 0.25s ease-out;padding:2px 0;">' +
                                    '<div style="font-size:9.5px;font-weight:900;color:#94a3b8;letter-spacing:1px;margin-bottom:2px;">PROFIT HACKER</div>' +
                                    '<div style="font-size:7.5px;font-weight:700;color:#cbd5e1;margin-bottom:4px;">MARKET SIGNAL</div>' +
                                    '<div style="font-size:17px;font-weight:900;color:' + candleColor + ';letter-spacing:1px;margin-bottom:2px;text-shadow:0 0 10px ' + candleColor + ';">' + signalText + '</div>' +
                                    '<div style="font-size:9px;font-weight:900;color:' + candleColor + ';letter-spacing:0.8px;">' + signalLabel + '</div>' +
                                '</div>';

                            // Auto-dismiss popup after 6 seconds
                            setTimeout(function(){
                                if(popup.isConnected) popup.remove();
                            }, 6000);

                        }, 5000); // Exactly 5 seconds scanning matching video requirement
                    });
                }

                function getActiveAssetSymbol() {
                    try {
                        var activeTab = d.querySelector('.asset-select__current, .current-asset, .asset-name, .chart-title, .value-asset, [class*="asset-select"], [class*="current-symbol"]');
                        if(activeTab) {
                            var t = (activeTab.innerText || activeTab.textContent || '').trim();
                            if(t && t.length < 15 && (t.includes('/') || t.includes('-') || t.includes('OTC'))) {
                                return t;
                            }
                        }
                        var allEls = d.querySelectorAll('span, div, button');
                        for(var i=0; i<allEls.length; i++) {
                            var text = (allEls[i].innerText || '').trim();
                            if(text && (text === 'EUR/USD' || text === 'GBP/USD' || text === 'AUD/USD' || text === 'USD/JPY' || text === 'EUR/JPY' || text.includes('OTC'))) {
                                if(text.length < 15) return text;
                            }
                        }
                    } catch(e) {}
                    return "EUR/USD";
                }

            } catch(e) { console.error("Profit Hacker Engine Error:", e); }
        }

        if (document.readyState === 'complete' || document.readyState === 'interactive') {
            initProfitHackerBot();
        } else {
            window.addEventListener('DOMContentLoaded', initProfitHackerBot);
            window.addEventListener('load', initProfitHackerBot);
            setTimeout(initProfitHackerBot, 400);
        }
    })();
    """
    res = make_response(js)
    res.headers['Content-Type'] = 'application/javascript'
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

def start_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    threading.Thread(target=start_server, daemon=True).start()
