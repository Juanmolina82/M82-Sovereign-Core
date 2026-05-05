const express = require('express');
const app = express();
const port = 3000;

app.get('/', (req, res) => {
    res.send(`
        <html><head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
        <style>
            body, html { background: #000; margin: 0; padding: 0; overflow: hidden; width: 100vw; height: 100vh; font-family: 'Arial Black', sans-serif; }
            .main-frame { display: flex; flex-direction: column; width: 104vw; height: 106vh; margin-top: -3vh; margin-left: -2vw; }
            .grid-live { display: grid; grid-template-columns: 1fr; height: 88vh; gap: 6px; padding: 6px; background: #000; }
            .panel { position: relative; border: 2px solid #D4AF37; overflow: hidden; background: #000; }
            iframe { width: 100%; height: 100%; border: none; transform: scale(1.05); }
            .tag { position: absolute; top: 8px; left: 10px; background: #D4AF37; color: #000; font-size: 1.5vw; padding: 4px 10px; z-index: 20; font-weight: 900; }
            .footer-m82 { height: 12vh; background: #000; border-top: 5px solid #D4AF37; display: flex; align-items: center; width: 100%; }
            .brand-tag { background: #D4AF37; height: 100%; width: 15%; display: flex; align-items: center; justify-content: center; clip-path: polygon(0 0, 100% 0, 85% 100%, 0% 100%); }
            .brand-tag h1 { color: #000; font-size: 4vw; margin: 0; font-style: italic; font-weight: 900; }
            .ticker-tape { width: 85%; height: 100%; }
        </style>
        </head>
        <body onclick="document.querySelectorAll('iframe').forEach(i => { i.src = i.src.replace('mute=1', 'mute=0'); });">
            <div class="main-frame">
                <div class="grid-live">
                    <div class="panel">
                        <div class="tag">M82 | BLOOMBERG LIVE</div>
                        <iframe src="https://www.youtube.com/embed/live_stream?channel=UCIALMKvObZNtJ6AmdCLP7Lg&autoplay=1&mute=0&controls=0"></iframe>
                    </div>
                </div>
                <div class="footer-m82">
                    <div class="brand-tag"><h1>M82</h1></div>
                    <div class="ticker-tape">
                        <iframe src="https://s.tradingview.com/embed-widget/ticker-tape/?colorTheme=dark&symbols=OANDA:WTICOIL,ICE:B1!,CURRENCYCOM:GOLD,FX:USDVES,BITSTAMP:BTCUSD,FX:EURUSD&locale=es"></iframe>
                    </div>
                </div>
            </div>
        </body></html>
    `);
});
app.listen(port, '0.0.0.0', () => console.log('🚀 M82 V15 RESTABLECIDA PARA EL CHAIRMAN'));
