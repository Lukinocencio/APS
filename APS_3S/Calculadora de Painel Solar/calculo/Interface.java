package calculo;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class Interface {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new CalculadoraEnergiaGUI().setVisible(true));
    }
}

class CalculadoraEnergiaGUI extends JFrame {
    private conta_comercial contComer = new conta_comercial();
    private conta_residencial contResiden = new conta_residencial();

    private JComboBox<String> tipoContaComboBox;
    private JTextField entradaTextField;
    private JTextArea resultadoTextArea;

    public CalculadoraEnergiaGUI() {
        setTitle("Calculadora de Energia Solar");
        setSize(500, 300);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);

        ImageIcon icon = new ImageIcon("ico.png");
        Image image = icon.getImage();
        setIconImage(image);

        JPanel panel = new JPanel(new GridBagLayout());
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(10, 10, 10, 10);
        gbc.fill = GridBagConstraints.HORIZONTAL;

        JLabel tipoContaLabel = new JLabel("Tipo da Conta:");
        gbc.gridx = 0;
        gbc.gridy = 0;
        panel.add(tipoContaLabel, gbc);

        tipoContaComboBox = new JComboBox<>(new String[]{"Comercial", "Residencial"});
        gbc.gridx = 1;
        gbc.gridy = 0;
        panel.add(tipoContaComboBox, gbc);


        JLabel entradaLabel = new JLabel("Consumo (em KWH):");
        gbc.gridx = 0;
        gbc.gridy = 1;
        panel.add(entradaLabel, gbc);

        entradaTextField = new JTextField();
        gbc.gridx = 1;
        gbc.gridy = 1;
        panel.add(entradaTextField, gbc);

        JButton calcularButton = new JButton("Calcular");
        calcularButton.addActionListener(new CalcularButtonListener());
        gbc.gridx = 0;
        gbc.gridy = 2;
        gbc.gridwidth = 2;
        gbc.anchor = GridBagConstraints.CENTER;
        panel.add(calcularButton, gbc);

        resultadoTextArea = new JTextArea();
        resultadoTextArea.setEditable(false);
        resultadoTextArea.setLineWrap(true);
        resultadoTextArea.setWrapStyleWord(true);

        gbc.gridx = 0;
        gbc.gridy = 3;
        gbc.gridwidth = 2;
        gbc.fill = GridBagConstraints.BOTH;
        gbc.weightx = 1;
        gbc.weighty = 1;
        panel.add(new JScrollPane(resultadoTextArea), gbc);

        tipoContaComboBox.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                resultadoTextArea.setText("");
                entradaTextField.setText("");
}
        });
        add(panel);
    }

    private class CalcularButtonListener implements ActionListener {
        @Override
        public void actionPerformed(ActionEvent e) {
            try {
                String tipoConta = (String) tipoContaComboBox.getSelectedItem();
                double entrada = Double.parseDouble(entradaTextField.getText());

                String resultado;
                if (tipoConta.equals("Comercial")) {
                    contComer.ValorComercial(entrada);
                    int painesSolares = (int) Math.ceil(entrada / 38.16);
                    double resposta = contComer.resultadoComercial;
                    resultado = String.format("Gasto total em R$: %.2f\n" +
                            "Utilizando panéis solares on-grid de 265W de potência, seria gerado aproximadamente 38,16 KWH/mês com 7 horas de luz solar por dia.\n" +
                            "Você precisaria de %d painéis solares para reduzir o custo da conta de energia elétrica.\n", resposta, painesSolares);
                } else {
                    contResiden.ValorResidencial(entrada);
                    int painesSolares = (int) Math.ceil(entrada / 38.16);
                    double resposta = contResiden.resultadoResidencial;
                    resultado = String.format("Gasto total em R$: %.2f\n" +
                            "Utilizando panéis solares on-grid de 265W de potência, seria gerado aproximadamente 38,16 KWH/mês com 7 horas de luz solar por dia.\n" +
                            "Você precisaria de %d painéis solares para reduzir o custo da conta de energia elétrica.\n", resposta, painesSolares);
                }
                resultadoTextArea.setText(resultado);
            } catch (NumberFormatException ex) {
                JOptionPane.showMessageDialog(CalculadoraEnergiaGUI.this, "Por favor, insira um valor numérico válido!", "Erro", JOptionPane.ERROR_MESSAGE);
                resultadoTextArea.setText("");
            }
        }
    }
}
