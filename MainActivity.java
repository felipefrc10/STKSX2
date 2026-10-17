// UI prototype only. This file does not implement PS2 emulation.
package com.stk.stksx2;

import android.app.Activity;
import android.os.Bundle;
import android.graphics.Color;
import android.view.Gravity;
import android.widget.LinearLayout;
import android.widget.TextView;

public class MainActivity extends Activity {
  @Override public void onCreate(Bundle state) {
    super.onCreate(state);
    LinearLayout root = new LinearLayout(this);
    root.setOrientation(LinearLayout.VERTICAL);
    root.setGravity(Gravity.CENTER);
    root.setPadding(24, 24, 24, 24);
    root.setBackgroundColor(Color.rgb(16, 20, 29));
    TextView title = new TextView(this);
    title.setText("STKSX2");
    title.setTextColor(Color.WHITE);
    title.setTextSize(30);
    title.setGravity(Gravity.CENTER);
    root.addView(title);
    TextView note = new TextView(this);
    note.setText("Protótipo de interface\nO núcleo de emulação é compilado separadamente com Android NDK.");
    note.setTextColor(Color.LTGRAY);
    note.setTextSize(15);
    note.setGravity(Gravity.CENTER);
    LinearLayout.LayoutParams p = new LinearLayout.LayoutParams(-1, -2);
    p.topMargin = 18;
    root.addView(note, p);
    setContentView(root);
  }
}
