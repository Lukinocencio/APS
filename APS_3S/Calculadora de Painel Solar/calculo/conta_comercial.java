package calculo;

public class conta_comercial extends informacao_conta{

    public double resultadoComercial = 0;

    public double ValorComercial(double entrada) {
        if (entrada >= 1){
            double custoComercialTE = ValorTE * entrada;
            custoComercialTE += custoComercialTE * ICMSComercial;
            custoComercialTE *= COFINS;
            custoComercialTE *= PIS;

            double CustoComercialTUSD = ValorTUSD * entrada;
            CustoComercialTUSD += CustoComercialTUSD * ICMSComercial;
            CustoComercialTUSD *= COFINS;
            CustoComercialTUSD *= PIS;

            resultadoComercial = custoComercialTE + CustoComercialTUSD;
        }
        return resultadoComercial;
    }
}

