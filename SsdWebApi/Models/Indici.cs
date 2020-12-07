using System;

namespace SsdWebApi.Models
{
    /* Conceptual Model:
    Modello concettuale della tabella del db che andremo ad istanziare, 
    ne avremo una per ogni tabella che vorremo istanziare
    */

    public class Indici
    {
        public int id {get; set;}
        public string Data {get; set;}
        public double SP_500{get; set;}
        public double FTSE_MIB_{get; set;}
        public double GOLD_SPOT{get; set;}
        public double MSCI_EM{get; set;}
        public double MSCI_EURO{get; set;}
        public double All_Bonds{get; set;}
        public double US_Treasury{get; set;}
    }
}