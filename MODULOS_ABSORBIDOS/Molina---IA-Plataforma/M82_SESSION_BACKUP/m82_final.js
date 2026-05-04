const express = require('express');
const app = express();
const port = 8080;

app.get('/', (req, res) => {
    res.send(`
        <html><head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <style>
            body, html { background: #000; margin: 0; padding: 0; overflow: hidden; width: 100vw; height: 100vh; }
            
            /* ZOOM CHAIRMAN: Estiramos la imagen para ocultar la barra de IP de Chrome */
            .m82-canvas { 
                width: 104vw; height: 108vh; 
                margin-top: -5vh; margin-left: -2vw;
                display: flex; flex-direction: column;
            }

            .grid { 
                display: grid; grid-template-columns: repeat(3, 1fr); grid-template-rows: repeat(3, 1fr);
                height: 90vh; gap: 4px; padding: 4px;
            }
            .panel { position: relative; border: 2px solid #D4AF37; background: #111; overflow: hidden; }
            iframe { width: 100%; height: 100%; border: none; }
            
            .m82-footer { 
                height: 10vh; background: #000; border-top: 4px solid #D4AF37;
                display: flex; align-items: center; justify-content: center;
            }
        </style>
        </head>
        <body onclick="document.querySelectorAll('iframe').forEach(i => { i.src = i.src + '&mute=0'; });">
            <div class="m82-canvas">
                <div class="grid">
                    <div class="panel"><iframe src="https://www.youtube.com/embed/live_stream?channel=UCIALMKvObZNtJ6AmdCLP7Lg&autoplay=1&mute=0"></iframe></div>
                    <div class="panel"><iframe src="https://www.youtube.com/embed/live_stream?channel=UCoMdktPbST7msyoFBQYL7_Q&autoplay=1&mute=1"></iframe></div>
                    <div class="panel"><iframe src="https://www.youtube.com/embed/live_stream?channel=UCEAZeUIeJs0IjQiqTCUcSIg&autoplay=1&mute=1"></iframe></div>
                    <div class="panel"><iframe src="https://www.youtube.com/embed/live_stream?channel=UChqUTbLjd9Mrscy_um_on_A&autoplay=1&mute=1"></iframe></div>
                    <div class="panel"><iframe src="https://www.youtube.com/embed/live_stream?channel=UC7L_UfS26X4xS6Z6Xqf_fLg&autoplay=1&mute=1"></iframe></div>
                    <div class="panel"><iframe src="https://www.youtube.com/embed/live_stream?channel=UChgjxy06K5As-Z89G8Z8S9w&autoplay=1&mute=1"></iframe></div>
                    <div class="panel"><iframe src="https://s.tradingview.com/widgetembed/?symbol=TVC:UKOIL&interval=1&theme=dark"></iframe></div>
                    <div class="panel"><iframe src="https://s.tradingview.com/widgetembed/?symbol=OANDA:XAUUSD&interval=1&theme=dark"></iframe></div>
                    <div class="panel"><iframe src="https://s.tradingview.com/widgetembed/?symbol=BITSTAMP:BTCUSD&interval=1&theme=dark"></iframe></div>
                </div>
                <div class="m82-footer">
                    <iframe width="100%" height="100%" src="https://s.tradingview.com/embed-widget/ticker-tape/?colorTheme=dark&symbols=OANDA:WTICOIL,ICE:B1!,CURRENCYCOM:GOLD,BITSTAMP:BTCUSD&locale=es"></iframe>
                </div>
            </div>
        </body></html>
    `);
});
app.listen(port, '0.0.0.0', () => console.log('🚀 M82 V16 ACTIVA EN PUERTO 8080'));
