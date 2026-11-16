const { withAndroidManifest, withDangerousMod } = require('@expo/config-plugins');
const fs = require('fs');
const path = require('path');

const RECEIVER_CODE = `package com.mmolina82.app;

import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.os.Build;
import androidx.core.app.NotificationCompat;

public class M82PushReceiver extends BroadcastReceiver {
    @Override
    public void onReceive(Context context, Intent intent) {
        String title = intent.getStringExtra("title");
        String body = intent.getStringExtra("body");
        String url = intent.getStringExtra("url");
        if (title == null) title = "M82 BREAKING NEWS";
        if (body == null) body = "Despacho Ejecutivo M82";
        if (url == null) url = "http://127.0.0.1:8282/?brief=1";

        String chId = "M82_SOVEREIGN_WIRE";
        NotificationManager nm = (NotificationManager) context.getSystemService(Context.NOTIFICATION_SERVICE);
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            NotificationChannel ch = new NotificationChannel(chId, "M82 Sovereign Wire", NotificationManager.IMPORTANCE_HIGH);
            nm.createNotificationChannel(ch);
        }

        Intent openIntent = new Intent(context, MainActivity.class);
        openIntent.setAction(Intent.ACTION_VIEW);
        openIntent.setData(Uri.parse(url));
        openIntent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TOP);

        PendingIntent pi = PendingIntent.getActivity(
            context, (int) System.currentTimeMillis(), openIntent,
            PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE
        );

        int iconId = context.getResources().getIdentifier("notification_icon", "drawable", context.getPackageName());
        if (iconId == 0) iconId = context.getApplicationInfo().icon;

        NotificationCompat.Builder nb = new NotificationCompat.Builder(context, chId)
            .setSmallIcon(iconId)
            .setContentTitle(title)
            .setContentText(body)
            .setStyle(new NotificationCompat.BigTextStyle().bigText(body))
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .setAutoCancel(true)
            .setContentIntent(pi);

        nm.notify((int) (System.currentTimeMillis() % 100000), nb.build());
    }
}
`;

module.exports = function withM82Push(config) {
  config = withAndroidManifest(config, (cfg) => {
    const app = cfg.modResults.manifest.application[0];
    if (!app.receiver) app.receiver = [];
    if (!app.receiver.some((r) => r.$['android:name'] === '.M82PushReceiver')) {
      app.receiver.push({
        $: {
          'android:name': '.M82PushReceiver',
          'android:enabled': 'true',
          'android:exported': 'true',
        },
        'intent-filter': [{ action: [{ $: { 'android:name': 'com.mmolina82.app.M82_ALERT' } }] }],
      });
    }
    return cfg;
  });

  config = withDangerousMod(config, ['android', async (cfg) => {
    const dir = path.join(cfg.modRequest.platformProjectRoot, 'app/src/main/java/com/mmolina82/app');
    fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(path.join(dir, 'M82PushReceiver.java'), RECEIVER_CODE);
    return cfg;
  }]);

  return config;
};
