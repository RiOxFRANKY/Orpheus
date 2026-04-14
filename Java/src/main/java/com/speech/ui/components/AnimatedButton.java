package com.speech.ui.components;

import javax.swing.*;
import java.awt.*;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;

public class AnimatedButton extends JButton {

    private float hoverAlpha = 0.0f;
    private float pressAlpha = 0.0f;
    private final Timer hoverTimer;
    private final Timer pressTimer;
    private boolean isSpecialGlow = false;

    public AnimatedButton(String text) {
        this(text, null);
    }

    public AnimatedButton(String text, Icon icon) {
        super(text, icon);
        setContentAreaFilled(false);
        setFocusPainted(false);
        setBorderPainted(false);
        setOpaque(false);
        setCursor(new Cursor(Cursor.HAND_CURSOR));

        // Smooth Hover Animation (Fade In/Out)
        hoverTimer = new Timer(15, e -> {
            if (getModel().isRollover()) {
                hoverAlpha = Math.min(1.0f, hoverAlpha + 0.1f);
            } else {
                hoverAlpha = Math.max(0.0f, hoverAlpha - 0.1f);
            }
            if (hoverAlpha == 0.0f || hoverAlpha == 1.0f) {
                ((Timer)e.getSource()).stop();
            }
            repaint();
        });

        // Click Logic
        pressTimer = new Timer(15, e -> {
            if (getModel().isPressed()) {
                pressAlpha = Math.min(1.0f, pressAlpha + 0.2f);
            } else {
                pressAlpha = Math.max(0.0f, pressAlpha - 0.2f);
            }
            if (pressAlpha == 0.0f || pressAlpha == 1.0f) {
                ((Timer)e.getSource()).stop();
            }
            repaint();
        });

        addMouseListener(new MouseAdapter() {
            @Override
            public void mouseEntered(MouseEvent e) {
                if (isEnabled()) hoverTimer.start();
            }

            @Override
            public void mouseExited(MouseEvent e) {
                hoverTimer.start();
            }

            @Override
            public void mousePressed(MouseEvent e) {
                if (isEnabled()) pressTimer.start();
            }

            @Override
            public void mouseReleased(MouseEvent e) {
                pressTimer.start();
            }
        });
    }

    public void setSpecialGlow(boolean specialGlow) {
        this.isSpecialGlow = specialGlow;
    }

    @Override
    protected void paintComponent(Graphics g) {
        Graphics2D g2 = (Graphics2D) g.create();
        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);

        int w = getWidth();
        int h = getHeight();
        int arc = 12;

        // 1. Draw Base Background (Theme Background)
        if (isEnabled()) {
            // Calculate hover color (Default theme highlight or Special Blue Glow)
            Color highlightColor = isSpecialGlow ? new Color(0, 120, 215) : UIManager.getColor("Button.hoverBackground");
            if (highlightColor == null) highlightColor = new Color(60, 60, 60);

            // Paint Hover Highlight
            if (hoverAlpha > 0) {
                g2.setColor(new Color(highlightColor.getRed(), highlightColor.getGreen(), highlightColor.getBlue(), (int)(hoverAlpha * 40)));
                g2.fillRoundRect(2, 2, w-4, h-4, arc, arc);
                
                // Extra Outer Glow for 'Special' buttons like RUN
                if (isSpecialGlow) {
                    g2.setColor(new Color(highlightColor.getRed(), highlightColor.getGreen(), highlightColor.getBlue(), (int)(hoverAlpha * 20)));
                    g2.setStroke(new BasicStroke(3f));
                    g2.drawRoundRect(1, 1, w-2, h-2, arc, arc);
                }
            }

            // Paint Pressed Effect
            if (pressAlpha > 0) {
                g2.setColor(new Color(highlightColor.getRed(), highlightColor.getGreen(), highlightColor.getBlue(), (int)(pressAlpha * 80)));
                g2.fillRoundRect(2, 2, w-4, h-4, arc, arc);
            }
        } else {
            // Fill disabled buttons with a dim standard shape rather than hollowing them out completely
            g2.setColor(new Color(60, 60, 60, 80));
            g2.fillRoundRect(2, 2, w-4, h-4, arc, arc);
        }

        // 2. Draw Standard FlatLaf Border (very thin)
        g2.setColor(new Color(100, 100, 100, 50));
        g2.setStroke(new BasicStroke(1f));
        g2.drawRoundRect(2, 2, w-4, h-4, arc, arc);

        g2.dispose();
        
        // Super handles centered text and icon painting
        super.paintComponent(g);
    }
}
