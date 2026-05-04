const axios = require('axios');

const BOT_TOKEN = '8022277515:AAEQhRC8cDlAsYekwUyt-szePmWOfBngD6w';
const CHAT_ID = 1020830115;

async function sendTelegram(text) {
  const url = `https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`;
  await axios.post(url, {
    chat_id: CHAT_ID,
    text,
  });
}

module.exports = { sendTelegram };
