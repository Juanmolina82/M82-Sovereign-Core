import React from 'react';
import { SafeAreaView, StatusBar } from 'react-native';
import { WebView } from 'react-native-webview';
export default function App() {
  return (
    <SafeAreaView style={{ flex: 1, backgroundColor: '#07090d' }}>
      <StatusBar barStyle="light-content" backgroundColor="#07090d" />
      <WebView source={{ uri: 'https://mmolina82.molina82.com' }} allowsBackForwardNavigationGestures />
    </SafeAreaView>
  );
}
