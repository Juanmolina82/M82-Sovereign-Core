import React, { useEffect, useState } from 'react';
import { SafeAreaView, StatusBar, Linking, Platform, PermissionsAndroid } from 'react-native';
import { WebView } from 'react-native-webview';

export default function App() {
  const [uri, setUri] = useState('http://127.0.0.1:8282/');

  useEffect(() => {
    if (Platform.OS === 'android' && Platform.Version >= 33) {
      PermissionsAndroid.request(PermissionsAndroid.PERMISSIONS.POST_NOTIFICATIONS).catch(() => {});
    }
    Linking.getInitialURL().then((u) => {
      if (u && u.startsWith('http')) setUri(u);
    });
    const sub = Linking.addEventListener('url', ({ url }) => {
      if (url && url.startsWith('http')) setUri(url);
    });
    return () => sub.remove();
  }, []);

  return (
    <SafeAreaView style={{ flex: 1, backgroundColor: '#060a12' }}>
      <StatusBar barStyle="light-content" backgroundColor="#060a12" />
      <WebView source={{ uri }} style={{ flex: 1 }} javaScriptEnabled domStorageEnabled />
    </SafeAreaView>
  );
}
