const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const express = require('express');

const app = express();
app.use(express.json());

const client = new Client({
    authStrategy: new LocalAuth({ dataPath: './m82_wa_session' }),
    puppeteer: {
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    }
});

let targetChatId = null;

client.on('qr', (qr) => {
    console.log('\n⚡ ESCANEA ESTE CÓDIGO QR CON TU WHATSAPP (Dispositivos vinculados):\n');
    qrcode.generate(qr, { small: true });
});

client.on('ready', () => {
    console.log('✅ Molina82 WhatsApp Bot CONECTADO y activo.');
});

app.post('/send-alert', async (req, res) => {
    const { message } = req.body;
    try {
        if (!targetChatId) {
            return res.status(400).json({ status: 'error', message: 'Envía M82 desde tu WhatsApp para vincular el chat.' });
        }
        await client.sendMessage(targetChatId, message);
        console.log('📩 Alerta reenviada a WhatsApp con éxito.');
        res.json({ status: 'success' });
    } catch (err) {
        res.status(500).json({ status: 'error', error: err.toString() });
    }
});

client.on('message', async (msg) => {
    if (msg.body.toUpperCase() === 'M82' || msg.body.toUpperCase() === 'START') {
        targetChatId = msg.from;
        await msg.reply('🔴 *Molina82 Terminal Vinculada*\n\nA partir de este momento recibirás todos los broadcasts de mercado, alertas de Hormuz y análisis de diésel/GPRK en este chat.');
    }
});

app.listen(8085, () => {
    console.log('🚀 Servidor del puente activo en http://127.0.0.1:8085');
});

client.initialize();
