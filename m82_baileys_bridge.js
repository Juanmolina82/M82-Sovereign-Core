const { default: makeWASocket, useMultiFileAuthState, DisconnectReason } = require('@whiskeysockets/baileys');
const qrcode = require('qrcode-terminal');
const express = require('express');
const pino = require('pino');

const app = express();
app.use(express.json());

let sock = null;
let targetJid = null;

async function connectToWhatsApp() {
    const { state, saveCreds } = await useMultiFileAuthState('m82_baileys_auth');

    sock = makeWASocket({
        auth: state,
        logger: pino({ level: 'silent' }), // Silenciar logs para que el QR no se mueva
        browser: ['Molina82 Terminal', 'Chrome', '1.0.0']
    });

    sock.ev.on('creds.update', saveCreds);

    sock.ev.on('connection.update', (update) => {
        const { connection, lastDisconnect, qr } = update;

        if (qr) {
            console.clear();
            console.log('====================================================');
            console.log('⚡ ESCANEA ESTE CÓDIGO QR EN TU WHATSAPP:');
            console.log('====================================================\n');
            qrcode.generate(qr, { small: true });
        }

        if (connection === 'close') {
            const statusCode = lastDisconnect?.error?.output?.statusCode;
            if (statusCode !== DisconnectReason.loggedOut) {
                setTimeout(connectToWhatsApp, 3000); // Esperar 3s antes de reintentar si se corta
            }
        } else if (connection === 'open') {
            console.clear();
            console.log('====================================================');
            console.log('✅ Molina82 WhatsApp Bot CONECTADO Y ACTIVO');
            console.log('====================================================');
            console.log('\nEnvia la palabra M82 desde tu WhatsApp para vincular.');
        }
    });

    sock.ev.on('messages.upsert', async (m) => {
        const msg = m.messages[0];
        if (!msg.key.fromMe && m.type === 'notify') {
            const text = msg.message?.conversation || msg.message?.extendedTextMessage?.text || '';
            if (text.trim().toUpperCase() === 'M82' || text.trim().toUpperCase() === 'START') {
                targetJid = msg.key.remoteJid;
                await sock.sendMessage(targetJid, { text: '🔴 *Molina82 Terminal Vinculada*\n\nA partir de este momento recibirás las alertas de mercado, Hormuz, diésel y reestructuración de deuda directamente en este chat.' });
                console.log(`📌 Chat vinculado a: ${targetJid}`);
            }
        }
    });
}

// Endpoint HTTP
app.post('/send-alert', async (req, res) => {
    const { message } = req.body;
    try {
        if (!targetJid) {
            return res.status(400).json({ status: 'error', message: 'Envía M82 desde WhatsApp primero.' });
        }
        await sock.sendMessage(targetJid, { text: message });
        res.json({ status: 'success' });
    } catch (err) {
        res.status(500).json({ status: 'error', error: err.toString() });
    }
});

app.listen(8085, () => {});

connectToWhatsApp();
