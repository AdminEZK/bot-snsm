require('dotenv').config();
const TelegramBot = require('node-telegram-bot-api');
const express = require('express');

const token = process.env.TELEGRAM_BOT_TOKEN;
const PORT = process.env.PORT || 3000;

// Variables globales
const enMer = new Map();
const attenteLieu = new Map(); // Suivi des utilisateurs en attente d'un choix de lieu suite à /depart
const LIEUX = ["Plage de Saint Cieux", "Plage de l'Islet"];

// Serveur HTTP pour Render (health check)
const app = express();
app.get('/', (req, res) => {
    res.send('🚤 Bot SNSM Telegram est en ligne !');
});

app.get('/health', (req, res) => {
    res.json({ 
        status: 'ok', 
        bot: 'running',
        enMer: enMer.size,
        timestamp: new Date().toISOString()
    });
});

app.listen(PORT, () => {
    console.log(`🌐 Serveur HTTP démarré sur le port ${PORT}`);
});

const bot = new TelegramBot(token, {
    polling: {
        interval: 1000,
        autoStart: true,
        params: {
            timeout: 10
        }
    }
});

// Enregistre les commandes pour l'UI Telegram (menu '/').
// Ainsi, en tapant '/', les utilisateurs voient les commandes disponibles.
(async () => {
    try {
        await bot.setMyCommands([
            { command: 'depart', description: 'Signaler un départ en mer' },
            { command: 'retour', description: 'Signaler un retour à la station (RAS)' },
            { command: 'status', description: 'Voir qui est en mer actuellement' },
            { command: 'aide', description: "Afficher l'aide" }
        ]);
        console.log('✅ Commandes Telegram enregistrées');
    } catch (error) {
        console.log('Erreur enregistrement commandes:', error.message);
    }
})();

console.log('🚤 Bot SNSM Telegram démarré !');
console.log('En attente de messages...\n');

bot.onText(/\/depart/, async (msg) => {
    const chatId = msg.chat.id;
    const nom = msg.from.first_name + (msg.from.last_name ? ' ' + msg.from.last_name : '');
    const userId = msg.from.id;
    
    console.log('✅ Commande /depart reçue de', nom);
    if (enMer.has(userId)) {
        await bot.sendMessage(chatId, "ℹ️ Tu es déjà signalé en mer. Envoie /retour pour te désinscrire.");
        return;
    }

    attenteLieu.set(userId, true);
    const keyboard = {
        reply_markup: {
            keyboard: [
                [{ text: LIEUX[0] }],
                [{ text: LIEUX[1] }],
                [{ text: 'Annuler' }]
            ],
            resize_keyboard: true,
            one_time_keyboard: true
        }
    };

    await bot.sendMessage(chatId, '📍 Depuis quel lieu pars-tu en mer ? Choisis une option ci-dessous.', keyboard);
});

bot.onText(/\/retour/, async (msg) => {
    const chatId = msg.chat.id;
    const nom = msg.from.first_name + (msg.from.last_name ? ' ' + msg.from.last_name : '');
    const userId = msg.from.id;
    
    console.log('✅ Commande /retour reçue de', nom);
    
    const info = enMer.get(userId);
    if (info) {
        const duree = calculerDuree(info.heureDepart);
        enMer.delete(userId);
        
        try {
            await bot.sendMessage(chatId, `✅ *${nom}* de retour à la station - RAS\n⏱️ Durée de sortie : ${duree}` + (info.lieu ? `\n📍 Lieu de départ : ${info.lieu}` : ''), {parse_mode: 'Markdown'});
            await afficherTableau(chatId);
        } catch (error) {
            console.log('Erreur:', error.message);
        }
    } else {
        await bot.sendMessage(chatId, '❌ Tu n\'étais pas signalé en mer');
    }
});

bot.onText(/\/status/, async (msg) => {
    console.log('✅ Commande /status reçue');
    await afficherTableau(msg.chat.id);
});

bot.onText(/\/aide|\/start|\/help/, async (msg) => {
    console.log('✅ Commande /aide reçue');
    const aide = `🌊 *Bot SNSM - Commandes disponibles*

- /depart - Signaler un départ en mer 📡
- /retour - Signaler un retour à la station (RAS)
- /status - Voir qui est en mer actuellement
- /aide - Afficher cette aide`;
    
    try {
        await bot.sendMessage(msg.chat.id, aide, {parse_mode: 'Markdown'});
    } catch (error) {
        console.log('Erreur:', error.message);
    }
});

async function afficherTableau(chatId) {
    let message = "🌊 *STATUS ÉQUIPE SNSM* 🌊\n\n";
    
    if (enMer.size === 0) {
        message += "✅ Toute l'équipe est à terre\n";
    } else {
        message += "🚤 *En mer actuellement :*\n\n";
        
        for (const [userId, info] of enMer.entries()) {
            const duree = calculerDuree(info.heureDepart);
            const heureDepart = info.heureDepart.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
            const lieuTxt = info.lieu ? `\n   └ 📍 Lieu : ${info.lieu}` : '';
            message += `🟢 *${info.nom}*${lieuTxt}\n   └ Départ : ${heureDepart} (${duree})\n\n`;
        }
    }
    
    const maintenant = new Date().toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
    message += `\n_Mis à jour : ${maintenant}_`;
    
    try {
        await bot.sendMessage(chatId, message, {parse_mode: 'Markdown'});
    } catch (error) {
        console.log('Erreur:', error.message);
    }
}

function calculerDuree(heureDepart) {
    const maintenant = new Date();
    const diff = maintenant - heureDepart;
    const heures = Math.floor(diff / (1000 * 60 * 60));
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    
    if (heures === 0) {
        return `${minutes} min`;
    }
    return `${heures}h${minutes.toString().padStart(2, '0')}`;
}

// Gestion des erreurs de polling
bot.on('polling_error', (error) => {
    console.log('⚠️ Erreur de connexion:', error.message);
});

// Gestion du choix de lieu après /depart
bot.on('message', async (msg) => {
    // Ignorer si ce n'est pas un message texte
    if (!msg.text) return;

    const chatId = msg.chat.id;
    const userId = msg.from.id;
    const nom = msg.from.first_name + (msg.from.last_name ? ' ' + msg.from.last_name : '');

    // Si l'utilisateur est en attente de choisir un lieu
    if (attenteLieu.has(userId)) {
        const texte = msg.text.trim();

        if (texte === 'Annuler') {
            attenteLieu.delete(userId);
            await bot.sendMessage(chatId, '❎ Annulé.', { reply_markup: { remove_keyboard: true } });
            return;
        }

        if (!LIEUX.includes(texte)) {
            await bot.sendMessage(chatId, 'Merci de choisir un lieu parmi les options proposées.');
            return;
        }

        // Enregistrer le départ avec le lieu choisi
        attenteLieu.delete(userId);
        enMer.set(userId, {
            nom: nom,
            heureDepart: new Date(),
            lieu: texte
        });

        const heure = new Date().toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
        try {
            await bot.sendMessage(chatId, `🟢 *${nom}* prend la mer à ${heure}\n📡 Signal actif\n📍 Lieu : ${texte}`, { parse_mode: 'Markdown', reply_markup: { remove_keyboard: true } });
            await afficherTableau(chatId);
        } catch (error) {
            console.log('Erreur:', error.message);
        }
    }
});