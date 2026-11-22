#!/data/data/com.termux/files/usr/bin/bash
set -e

M82_DIR="$HOME/M82"
BUILD_DIR="$M82_DIR/mobile_build/m82_native_v605"
OUT_DIR="$M82_DIR/mobile_build"
PKG_PATH="com/molinaholdings/m82sovereign"

echo "[1/6] Verificando herramientas de compilación Android en Termux..."
pkg install -y openjdk-17 aapt2 apksigner dx zip unzip >/dev/null 2>&1 || true

rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR/src/$PKG_PATH" \
         "$BUILD_DIR/res/values" \
         "$BUILD_DIR/res/drawable" \
         "$BUILD_DIR/res/xml" \
         "$BUILD_DIR/assets" \
         "$BUILD_DIR/obj" \
         "$BUILD_DIR/bin" \
         "$OUT_DIR"

# 2. Copiar HUD y telemetría viva a assets/ para funcionamiento local e instantáneo
python3 "$M82_DIR/m82_quant_api_bridge.py"
cp "$M82_DIR/static/m82_quant_hud.html" "$BUILD_DIR/assets/index.html"
cp "$M82_DIR/static/m82_quant_master_telemetry.json" "$BUILD_DIR/assets/telemetry.json"

# 3. Crear AndroidManifest.xml (Permisos Internet, Cleartext localhost y WakeLock)
cat << 'XML' > "$BUILD_DIR/AndroidManifest.xml"
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.molinaholdings.m82sovereign"
    android:versionCode="605"
    android:versionName="60.5.0">

    <uses-sdk android:minSdkVersion="24" android:targetSdkVersion="34" />
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />

    <application
        android:label="M82 Sovereign Core"
        android:usesCleartextTraffic="true"
        android:hardwareAccelerated="true"
        android:theme="@android:style/Theme.NoTitleBar.Fullscreen">
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:screenOrientation="portrait">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
XML

# 4. Crear MainActivity.java nativo (Conecta a :8080 en vivo con fallback inmediato a assets/index.html)
cat << 'JAVA' > "$BUILD_DIR/src/$PKG_PATH/MainActivity.java"
package com.molinaholdings.m82sovereign;

import android.app.Activity;
import android.graphics.Color;
import android.os.Bundle;
import android.webkit.WebResourceError;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public class MainActivity extends Activity {
    private WebView webView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        webView = new WebView(this);
        webView.setBackgroundColor(Color.parseColor("#070b12"));

        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setAllowFileAccess(true);
        settings.setCacheMode(WebSettings.LOAD_NO_CACHE);

        webView.setWebViewClient(new WebViewClient() {
            @Override
            public void onReceivedError(WebView view, WebResourceRequest request, WebResourceError error) {
                if (request.isForMainFrame()) {
                    view.loadUrl("file:///android_asset/index.html");
                }
            }
        });

        setContentView(webView);
        webView.loadUrl("http://127.0.0.1:8080/m82_quant_hud.html");
    }

    @Override
    public void onBackPressed() {
        if (webView.canGoBack()) {
            webView.goBack();
        } else {
            super.onBackPressed();
        }
    }
}
JAVA

echo "[2/6] Localizando android.jar del SDK en Termux..."
ANDROID_JAR=$(find "$PREFIX" /data/data/com.termux -name "android.jar" 2>/dev/null | head -n 1)
if [ -z "$ANDROID_JAR" ]; then
  echo "[!] Descargando android-34.jar oficial ligero para compilación..."
  mkdir -p "$M82_DIR/mobile_build/sdk"
  curl -sL "https://github.com/Sable/android-platforms/raw/master/android-34/android.jar" -o "$M82_DIR/mobile_build/sdk/android.jar"
  ANDROID_JAR="$M82_DIR/mobile_build/sdk/android.jar"
fi

echo "[3/6] Compilando recursos y bytecode Dalvik (DEX)..."
aapt2 link -o "$BUILD_DIR/bin/unaligned.apk" \
  --manifest "$BUILD_DIR/AndroidManifest.xml" \
  -I "$ANDROID_JAR" \
  -A "$BUILD_DIR/assets" \
  --java "$BUILD_DIR/src"

javac -source 1.8 -target 1.8 -bootclasspath "$ANDROID_JAR" \
  -d "$BUILD_DIR/obj" \
  $(find "$BUILD_DIR/src" -name "*.java")

dx --dex --output="$BUILD_DIR/bin/classes.dex" "$BUILD_DIR/obj"
cd "$BUILD_DIR/bin"
zip -qj unaligned.apk classes.dex

echo "[4/6] Generando Keystore institucional y firmando APK (v1/v2/v3)..."
KEYSTORE="$OUT_DIR/m82_sovereign_release.keystore"
if [ ! -f "$KEYSTORE" ]; then
  keytool -genkeypair -v -keystore "$KEYSTORE" \
    -alias m82sovereign -keyalg RSA -keysize 2048 -validity 10000 \
    -storepass M82Sovereign2026! -keypass M82Sovereign2026! \
    -dname "CN=Juan M. Molina, OU=Molina Holdings LLC, O=M82 Sovereign Core, L=Charallave, ST=Miranda, C=VE" >/dev/null 2>&1
fi

FINAL_APK="$OUT_DIR/m82-sovereign-v60.5.apk"
apksigner sign --ks "$KEYSTORE" \
  --ks-key-alias m82sovereign \
  --ks-pass pass:M82Sovereign2026! \
  --key-pass pass:M82Sovereign2026! \
  --out "$FINAL_APK" \
  "$BUILD_DIR/bin/unaligned.apk"

echo "[5/6] Certificando firma criptográfica del APK..."
apksigner verify --print-certs "$FINAL_APK"

echo "[6/6] Lanzando instalador de Android en su dispositivo..."
ls -lh "$FINAL_APK"
if command -v termux-open >/dev/null 2>&1; then
  termux-open "$FINAL_APK"
else
  am start -a android.intent.action.VIEW -d "file://$FINAL_APK" -t "application/vnd.android.package-archive" >/dev/null 2>&1
fi
