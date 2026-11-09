// Guard M82 - BUNKER 0.30x LOCK
function canExecute(){ return false; }
function onWebhook(req){
  if(!canExecute()){
    console.log("BLOQUEADO BUNKER - Webhook en silencio - 0 ejecuciones");
    return {status: 403, body: "BUNKER MODE - NO DISPARAR"};
  }
}
module.exports = { canExecute, onWebhook };
