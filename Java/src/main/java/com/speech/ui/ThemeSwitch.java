package com.speech.ui;

import com.formdev.flatlaf.FlatLaf;
import com.formdev.flatlaf.extras.FlatAnimatedLafChange;
import com.formdev.flatlaf.themes.FlatMacDarkLaf;
import com.formdev.flatlaf.themes.FlatMacLightLaf;
import com.speech.util.SVGIconHelper;

import javax.swing.*;
import java.awt.*;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;

public class ThemeSwitch extends JComponent {
    private boolean isDarkMode = true;
    private boolean isAnimating = false;
    private int knobX = 46; 
    private final int KNOB_SIZE = 30;
    private final int MAX_X = 46;
    private final int MIN_X = 4;
    private Timer animationTimer;

    private Icon sunIcon;
    private Icon moonIcon;

    public ThemeSwitch() {
        setPreferredSize(new Dimension(80, 38));
        setCursor(new Cursor(Cursor.HAND_CURSOR));
        setToolTipText("Toggle Theme");

        // Load the actual SVG icons dynamically
        sunIcon = SVGIconHelper.getIcon("sun.svg");
        moonIcon = SVGIconHelper.getIcon("moon.svg");

        addMouseListener(new MouseAdapter() {
            @Override
            public void mouseClicked(MouseEvent e) {
                // Ignore clicks if the slide is already happening
                if (!isAnimating) {
                    toggle();
                }
            }
        });
    }

    private void toggle() {
        isAnimating = true;
        isDarkMode = !isDarkMode;
        
        int targetX = isDarkMode ? MAX_X : MIN_X;
        
        // Fix glitchy animation: Animate the knob smoothly first before triggering the global UI crossfade!
        animationTimer = new Timer(12, e -> {
            int step = (targetX > knobX) ? 3 : -3;
            knobX += step;
            
            // Prevent overshoot
            if ((step > 0 && knobX >= targetX) || (step < 0 && knobX <= targetX)) {
                knobX = targetX;
                animationTimer.stop();
                isAnimating = false;
                
                // Once slide algorithm perfectly finishes, trigger the massive UI repaint snapshot
                EventQueue.invokeLater(this::changeTheme);
            }
            repaint();
        });
        animationTimer.start();
    }
    
    private void changeTheme() {
        try {
            FlatAnimatedLafChange.showSnapshot();
            
            // Re-enforce global font before invoking the new theme to ensure it never gets overridden 
            // We use 12f to match the original App.java baseline!
            javax.swing.plaf.FontUIResource mainFont = new javax.swing.plaf.FontUIResource(com.speech.util.FontHelper.getAnticycloneFont(Font.PLAIN, 12f));
            UIManager.put("defaultFont", mainFont);

            if (isDarkMode) {
                UIManager.setLookAndFeel(new FlatMacDarkLaf());
            } else {
                UIManager.setLookAndFeel(new FlatMacLightLaf());
            }
            
            // Standard updateUI only hits the current component tree; we want to ensure the ENTIRE window (including borders) is refreshed!
            Window window = SwingUtilities.getWindowAncestor(this);
            if (window != null) {
                SwingUtilities.updateComponentTreeUI(window);
            } else {
                FlatLaf.updateUI();
            }

            FlatAnimatedLafChange.hideSnapshotWithAnimation();
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    @Override
    protected void paintComponent(Graphics g) {
        Graphics2D g2 = (Graphics2D) g.create();
        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);

        // 0.0 means fully Light Mode (Left), 1.0 means fully Dark Mode (Right)
        float ratio = (float) (knobX - MIN_X) / (MAX_X - MIN_X);
        
        // Dynamically crossfade the pill background color
        int pr = (int) (210 + ratio * (30 - 210));
        g2.setColor(new Color(pr, pr, pr));
        g2.fillRoundRect(0, 0, getWidth(), getHeight(), getHeight(), getHeight());

        // Dynamically crossfade the sliding knob color (White -> Blue)
        int kr = (int) (255 + ratio * (20 - 255));
        int kg = (int) (255 + ratio * (100 - 255));
        int kb = (int) (255 + ratio * (255 - 255)); 
        g2.setColor(new Color(kr, kg, kb));
        g2.fillOval(knobX, 4, KNOB_SIZE, KNOB_SIZE);

        // Calculate exact absolute centers for the stationary icons
        int leftCenterX = MIN_X + (KNOB_SIZE / 2);
        int rightCenterX = MAX_X + (KNOB_SIZE / 2);
        int CenterY = 4 + (KNOB_SIZE / 2);

        // Draw stationary Sun on the left
        if (sunIcon != null) {
            float sunAlpha = 1.0f - (0.6f * ratio); // 1.0 at start, fading to 0.4
            g2.setComposite(AlphaComposite.getInstance(AlphaComposite.SRC_OVER, sunAlpha));
            sunIcon.paintIcon(this, g2, leftCenterX - (sunIcon.getIconWidth() / 2), CenterY - (sunIcon.getIconHeight() / 2));
        }

        // Draw stationary Moon on the right
        if (moonIcon != null) {
            float moonAlpha = 0.4f + (0.6f * ratio); // 0.4 at start, brightening to 1.0
            g2.setComposite(AlphaComposite.getInstance(AlphaComposite.SRC_OVER, moonAlpha));
            moonIcon.paintIcon(this, g2, rightCenterX - (moonIcon.getIconWidth() / 2), CenterY - (moonIcon.getIconHeight() / 2));
        }

        g2.dispose();
    }
}
