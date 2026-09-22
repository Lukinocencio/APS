package calculo;

public class conta_residencial extends informacao_conta{
    public double resultadoResidencial;

    public double ValorResidencial(double entrada) {
        if (entrada >= 1 & entrada <= 90) {
            double custoResidencialTE = entrada * ValorTE;
            custoResidencialTE += custoResidencialTE * ICMSResidencial12;
            custoResidencialTE *= COFINS;
            custoResidencialTE *= PIS;

            double custoResidencialTUSD = entrada * ValorTUSD + CIP;
            custoResidencialTUSD += custoResidencialTUSD * ICMSResidencial12;
            custoResidencialTUSD *= COFINS;
            custoResidencialTUSD *= PIS;

            resultadoResidencial = custoResidencialTE + custoResidencialTUSD;
        } else if (entrada >= 91 & entrada <= 200) {
            double custoResidencialTE = entrada * ValorTE;
            custoResidencialTE += custoResidencialTE * ICMSResidencial25;
            custoResidencialTE *= COFINS;
            custoResidencialTE *= PIS;

            double custoResidencialTUSD = entrada * ValorTUSD;
            custoResidencialTUSD += custoResidencialTUSD * ICMSResidencial12;
            custoResidencialTUSD *= COFINS;
            custoResidencialTUSD *= PIS;

            resultadoResidencial = custoResidencialTE + custoResidencialTUSD;
        } else if (entrada > 201) {
            double custoResidencialTE = entrada * ValorTE;
            custoResidencialTE *= COFINS;
            custoResidencialTE *= PIS;

            double custoResidencialTUSD = entrada * ValorTUSD;
            custoResidencialTUSD *= COFINS;
            custoResidencialTUSD *= PIS;
            resultadoResidencial = custoResidencialTE + custoResidencialTUSD;

        }
        return resultadoResidencial;
    }
}

