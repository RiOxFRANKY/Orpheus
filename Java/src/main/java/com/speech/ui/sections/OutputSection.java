package com.speech.ui.sections;

import com.speech.ui.AbstractDashboardSection;
import com.speech.ui.components.AnimatedButton;
import net.miginfocom.swing.MigLayout;

public class OutputSection extends AbstractDashboardSection {

    private AnimatedButton saveCsvButton;
    private AnimatedButton saveZipButton;

    @Override
    public String getSectionTitle() {
        return "5. Output Section (Download Results)";
    }

    @Override
    protected void initializeComponents() {
        // Increased gap between buttons for a cleaner layout
        panel.setLayout(new MigLayout("fillx, insets 10", "[grow]15[grow]", "[grow]"));

        saveCsvButton = new AnimatedButton("Save Processed Audio (CSV)");
        saveCsvButton.setIcon(com.speech.util.SVGIconHelper.getIcon("download.svg"));
        saveCsvButton.setEnabled(false);

        saveZipButton = new AnimatedButton("Save Processed Audio (ZIP)");
        saveZipButton.setIcon(com.speech.util.SVGIconHelper.getIcon("download.svg"));
        saveZipButton.setEnabled(false);

        // Allow Output buttons to demand a tall, prominent vertical space (minimum 50px, up to 100!
        panel.add(saveCsvButton, "growx, h 50::100");
        panel.add(saveZipButton, "growx, h 50::100");
    }

    public void enableButtons() {
        saveCsvButton.setEnabled(true);
        saveZipButton.setEnabled(true);
    }
}
