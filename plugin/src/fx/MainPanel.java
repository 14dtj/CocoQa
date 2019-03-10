package fx;


import javafx.application.Platform;
import javafx.embed.swing.JFXPanel;
import javafx.scene.Scene;
import javafx.scene.web.WebView;

import javax.swing.*;
import java.awt.*;

/**
 * Created by liwei on 2018/11/26.
 */

public class MainPanel {
    private JPanel mainPanel = null;

    public MainPanel() {
        mainPanel = new JPanel();
        mainPanel.setLayout(new BorderLayout(5, 5));
        mainPanel.add(createWebPanel(), BorderLayout.CENTER);
    }

    public JPanel createPanel() {
        return mainPanel;
    }

    private JFXPanel createWebPanel() {
        JFXPanel webPanel = new JFXPanel();
        Platform.runLater(() -> {
            WebView webView = new WebView();
            webPanel.setScene(new Scene(webView));
            webView.getEngine().load("http://202.120.40.28:4461/ordinary");
        });
        return webPanel;
    }

    //为了单独测试使用
    public static void main(String[] args) {
        MainPanel mainPanel = new MainPanel();
        JFrame frame = new JFrame();
        frame.setLayout(new BorderLayout());
        frame.setSize(800, 600);
        frame.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
        frame.add(mainPanel.createPanel(), "Center");
        frame.setVisible(true);
    }
}
