const { default: makeWASocket, useMultiFileAuthState, DisconnectReason } = require('@whiskeysockets/baileys');
const express = require('express');
const pino = require('pino');

const app = express();
app.use(express.json());

let sock = null;
let targetJid = null;
const MY_NUMBER = "16156147155";

async function startBridge() {
    const { state, saveCreds } = await useMultiFileAuthState('m82_baileys_auth');

    sock = makeWASocket({
        auth: state,
        logger: pino({ level: 'silent' }),
        browser: ["Chrome (Linux)", "", ""]
    });

    sock.ev.on('creds.update', saveCreds);

    sock.ev.on('connection.update', async (update) => {
        const { connection, lastDisconnect, qr } = update;

        if (connection === 'connecting') {
            console.log('⚡ Conectando a los servidores de WhatsApp...');
        }

        if (connection === 'close') {
            const statusCode = lastDisconnect?.error?.output?.statusCode;
            if (statusCode !== DisconnectReason.loggedOut) {
                setTimeout(startBridge, 3000);
            }
        } else if (connection === 'open') {
            console.clear();
            console.log('====================================================');
            console.log('✅ Molina82 WhatsApp Bot CONECTADO Y ACTIVO');
            console.log('====================================================');
            console.log('\nEnvía la palabra M82 desde tu WhatsApp para activar las alertas.');
        }

        // Solicitar el código solo cuando la conexión preliminar esté lista
        if (!sock.authState.creds.registered && !sock.pairingCodeRequested) {
            sock.pairingCodeRequested = true;
            setTimeout(async () => {
                try {
                    const code = await sock.requestPairingCode(MY_NUMBER);
                    console.clear();
                    console.log('====================================================');
                    console.log(`🔑 TU CÓDIGO DE VINCULACIÓN ES:   ${code}`);
                    console.log('====================================================\n');
                    console.log('1. Abre WhatsApp en tu celular.');
                    console.log('2. Ve a Dispositivos vinculados -> Vincular un dispositivo.');
                    console.log('3. Toca abajo: "Vincular con el número de teléfono".');
                    console.log(`4. Introduce los 8 dígitos: ${code}\n`);
                } catch (err) {
                    console.error('❌ Error generando código:', err.message);
                    sock.pairingCodeRequested = false;
                }
            }, 2000);
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

startBridge();
