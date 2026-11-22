#!/data/data/com.termux/files/usr/bin/bash
set -e

M82_DIR="$HOME/M82"
BUILD_DIR="$M82_DIR/mobile_build/m82_native_v605"
OUT_DIR="$M82_DIR/mobile_build"
PKG_PATH="com/molinaholdings/m82sovereign"
SDK_DIR="$OUT_DIR/sdk"

mkdir -p "$BUILD_DIR/src/$PKG_PATH" "$BUILD_DIR/assets" "$BUILD_DIR/obj" "$BUILD_DIR/bin" "$SDK_DIR"

echo "[1/5] Actualizando telemetría viva en assets/..."
python3 "$M82_DIR/m82_quant_api_bridge.py"
cp "$M82_DIR/static/m82_quant_hud.html" "$BUILD_DIR/assets/index.html"
cp "$M82_DIR/static/m82_quant_master_telemetry.json" "$BUILD_DIR/assets/telemetry.json"

echo "[2/5] Preparando android-34.jar ligero..."
ANDROID_JAR="$SDK_DIR/android.jar"
if false; then
  ANDROID_JAR="$PREFIX/share/aapt/android.jar"
elif [ ! -s "$ANDROID_JAR" ]; then
  curl -fsSL "https://github.com/Sable/android-platforms/raw/master/android-34/android.jar" -o "$ANDROID_JAR"
fi

echo "[3/5] Empaquetando recursos con aapt y compilando DEX (openjdk-21)..."
aapt package -f -m \
  -J "$BUILD_DIR/src" \
  -M "$BUILD_DIR/AndroidManifest.xml" \
  -A "$BUILD_DIR/assets" \
  -I "$ANDROID_JAR" \
  -F "$BUILD_DIR/bin/unaligned.apk"

javac -J-Xmx256m --source 1.8 -target 1.8 -bootclasspath "$ANDROID_JAR" \
  -d "$BUILD_DIR/obj" \
  "$BUILD_DIR/src/$PKG_PATH/MainActivity.java"

dx -JXmx256m --dex --output="$BUILD_DIR/bin/classes.dex" "$BUILD_DIR/obj"
cd "$BUILD_DIR/bin"
zip -qj unaligned.apk classes.dex

echo "[4/5] Firmando APK Release (RSA-2048)..."
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

apksigner verify --print-certs "$FINAL_APK"

echo "[5/5] Abriendo instalador Android para m82-sovereign-v60.5.apk..."
ls -lh "$FINAL_APK"
if command -v termux-open >/dev/null 2>&1; then
  termux-open "$FINAL_APK"
else
  am start -a android.intent.action.VIEW -d "file://$FINAL_APK" -t "application/vnd.android.package-archive" >/dev/null 2>&1
fi
