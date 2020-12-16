using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using SsdWebApi.Models;

namespace SsdWebApi.Controllers
{
    /*
    ControllerBase è la definizione generica ed astratta di un controller.
    */
    [ApiController]
    [Route("api/Indici")]
    public class IndiciController : ControllerBase
    {
        private readonly IndiciContext _context; //IndiciContext è il modello di storage -> riferimento al DB
        private Persistence persistence;
        public IndiciController(IndiciContext context)
        {
            _context = context;
            persistence = new Persistence(context);
        }


        //GET by ID action: es. https://localhost:5001/api/indici  --> togliere ID
        [HttpGet]
        public string GetSerie()
        {

            string res = "{";
            string[] indiciSerie = new string[] { "SP_500", "FTSE_MIB", "GOLD_SPOT", "MSCI_EM", "MSCI_EURO", "All_Bonds", "US_Treasury" };

            //non gli passo più l'indice per cui devo ciclare un foreach su indiciserie e li passo alla read e generare tutti i csv
            foreach(string indici in indiciSerie)
            {
                persistence.ReadColumnIndexAndCsv(indici);
            }

            Forecast forecast = new Forecast();
            res += forecast.forecastIndici();
            res += "}";

            return res;
        }

    }
}