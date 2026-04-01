package com.speech.util;

import com.kitfox.svg.app.beans.SVGIcon;

import javax.swing.*;
import java.awt.*;
import java.net.URL;

public class SVGIconHelper {
    public static Icon getIcon(String path) {
        try {
            URL url = SVGIconHelper.class.getResource("/icons/" + path);
            if (url != null) {
                SVGIcon icon = new SVGIcon();
                icon.setSvgURI(url.toURI());
                icon.setPreferredSize(new Dimension(20, 20));
                icon.setAntiAlias(true);
                return icon;
            }
        } catch (Exception e) {
            System.err.println("Could not load SVG: " + path);
        }
        
        // Fallback dummy icon
        return new Icon() {
            @Override public void paintIcon(Component c, Graphics g, int x, int y) {
                g.setColor(Color.LIGHT_GRAY);
                g.fillRect(x, y, 16, 16);
            }
            @Override public int getIconWidth() { return 16; }
            @Override public int getIconHeight() { return 16; }
        };
    }
}
