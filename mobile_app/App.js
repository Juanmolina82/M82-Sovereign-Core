import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View, ScrollView, TouchableOpacity, SafeAreaView } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import * as LocalAuthentication from 'expo-local-authentication';

const API_URL = 'https://wire.molina82.com/api?t=23bd5bf695350216506321df0466834b'; // Cambiar a https://wire.molina82.com en produccion

export default function App() {
  const [unlocked, setUnlocked] = useState(false);
  const [tab, setTab] = useState('news');
  const [data, setData] = useState({ q: {}, n: [], a: [] });

  const auth = async () => {
    const res = await LocalAuthentication.authenticateAsync({ promptMessage: 'M82 Sovereign Core :: Acceso Ejecutivo' });
    if (res.success) setUnlocked(true);
  };

  useEffect(() => { auth(); }, []);
  useEffect(() => {
    if (!unlocked) return;
    const load = async () => { try { const r = await fetch(API_URL); setData(await r.json()); } catch (e) {} };
    load(); const t = setInterval(load, 15000); return () => clearInterval(t);
  }, [unlocked]);

  if (!unlocked) return (
    <SafeAreaView style={s.lock}>
      <StatusBar style="light" />
      <Text style={s.logo}>M82 QUANTUM TERMINAL</Text>
      <Text style={s.sub}>MOLINA HOLDINGS LLC &bull; BUNKER 0.30x LOCK</Text>
      <TouchableOpacity style={s.btn} onPress={auth}><Text style={s.btnT}>DESBLOQUEAR CON BIOMETRIA</Text></TouchableOpacity>
    </SafeAreaView>
  );

  const q = data.q || {};
  return (
    <SafeAreaView style={s.container}>
      <StatusBar style="light" />
      <View style={s.top}><Text style={s.brand}>M82 QUANTUM WIRE</Text><View style={s.badge}><Text style={s.badgeT}>BUNKER 0.30x</Text></View></View>
      <ScrollView style={s.body}>
        {tab === 'news' && (
          <View>
            <View style={s.banner}><Text style={s.banH}>M82 breaking wire</Text><Text style={s.banS}>LSEG / REUTERS &bull; NODO CHARALLAVE EDGE</Text></View>
            {(data.n || []).map((x, i) => (
              <View key={i} style={s.card}>
                <Text style={s.meta}>{x.s} &bull; {(x.ts || '').slice(0, 16)}</Text>
                <Text style={s.head}>{x.h}</Text>
                <Text style={s.risk}>RISK SCORE: {x.r} &bull; {x.t}</Text>
              </View>
            ))}
          </View>
        )}
        {tab === 'mkt' && (
          <View style={s.grid}>
            {[['WTI (CLc1)', '$' + q.CLc1], ['Brent (LCOc1)', '$' + q.LCOc1], ['Crack 3-2-1', '$' + q.crack_321_usd], ['UST 10Y', q['US10YT=RR'] + '%'], ['DXY', q['.DXY']], ['HO (HOc1)', '$' + q.HOc1]].map((m, i) => (
              <View key={i} style={s.box}><Text style={s.lbl}>{m[0]}</Text><Text style={s.val}>{m[1] || '-'}</Text></View>
            ))}
          </View>
        )}
        {tab === 'port' && (
          <View style={s.grid}>
            <View style={s.box}><Text style={s.lbl}>EXPOSICION</Text><Text style={[s.val, { color: '#00e676' }]}>0.22x / 0.30x</Text></View>
            <View style={s.box}><Text style={s.lbl}>DRY POWDER</Text><Text style={s.val}>78.0%</Text></View>
            <View style={s.box}><Text style={s.lbl}>VaR DIARIO</Text><Text style={[s.val, { color: '#ffb300' }]}>1.68%</Text></View>
            <View style={s.box}><Text style={s.lbl}>WARSH SPREAD</Text><Text style={s.val}>102.0 bps</Text></View>
          </View>
        )}
      </ScrollView>
      <View style={s.ticker}><Text style={s.tkT}>WTI ${q.CLc1 || '-'} | BRENT ${q.LCOc1 || '-'} | CRACK ${q.crack_321_usd || '-'} | 10Y {q['US10YT=RR'] || '-'}%</Text></View>
      <View style={s.nav}>
        {[['mkt', 'Mercados'], ['port', 'Portafolio'], ['news', 'Noticias']].map(([k, l]) => (
          <TouchableOpacity key={k} onPress={() => setTab(k)}><Text style={[s.navT, tab === k && { color: '#1e90ff' }]}>{l}</Text></TouchableOpacity>
        ))}
      </View>
    </SafeAreaView>
  );
}
const s = StyleSheet.create({
  lock: { flex: 1, backgroundColor: '#000', justifyContent: 'center', alignItems: 'center', padding: 24 },
  logo: { color: '#1e90ff', fontSize: 22, fontWeight: '900', letterSpacing: 1 },
  sub: { color: '#888', fontSize: 11, marginTop: 8, marginBottom: 32 },
  btn: { backgroundColor: '#1e90ff', paddingVertical: 14, paddingHorizontal: 24, borderRadius: 8 },
  btnT: { color: '#000', fontWeight: '900', fontSize: 13 },
  container: { flex: 1, backgroundColor: '#000' },
  top: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', padding: 14, borderBottomWidth: 1, borderColor: '#1a1a1a' },
  brand: { color: '#1e90ff', fontWeight: '900', fontSize: 16 },
  badge: { backgroundColor: '#2a080d', borderWidth: 1, borderColor: '#ff1744', paddingHorizontal: 8, paddingVertical: 3, borderRadius: 4 },
  badgeT: { color: '#ff5252', fontSize: 10, fontWeight: '800' },
  body: { flex: 1 },
  banner: { backgroundColor: '#c62828', padding: 16 },
  banH: { color: '#fff', fontSize: 24, fontWeight: '900' },
  banS: { color: '#ffcdd2', fontSize: 10, marginTop: 4, letterSpacing: 1 },
  card: { padding: 14, borderBottomWidth: 1, borderColor: '#181818' },
  meta: { color: '#888', fontSize: 11 },
  head: { color: '#fff', fontSize: 16, fontWeight: '700', marginVertical: 6 },
  risk: { color: '#ffb300', fontSize: 11, fontWeight: '700' },
  grid: { flexDirection: 'row', flexWrap: 'wrap', padding: 10, gap: 10 },
  box: { width: '47%', backgroundColor: '#0b0b0b', borderWidth: 1, borderColor: '#222', borderRadius: 8, padding: 14 },
  lbl: { color: '#888', fontSize: 10 },
  val: { color: '#fff', fontSize: 20, fontWeight: '800', marginTop: 4 },
  ticker: { backgroundColor: '#0a0a0a', borderTopWidth: 1, borderColor: '#222', padding: 8, alignItems: 'center' },
  tkT: { color: '#00e676', fontSize: 11, fontWeight: '700' },
  nav: { flexDirection: 'row', justifyContent: 'space-around', paddingVertical: 14, backgroundColor: '#050505', borderTopWidth: 1, borderColor: '#1a1a1a' },
  navT: { color: '#777', fontSize: 12, fontWeight: '800' }
});
