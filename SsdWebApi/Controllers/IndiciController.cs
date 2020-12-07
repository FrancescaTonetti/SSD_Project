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

        [HttpGet]
        public ActionResult<List<Indici>> GetAll() => _context.indici.ToList();


        //GET by ID action: es. https://localhost:5001/api/indici/3
        [HttpGet("{idSerie}", Name = "GetSerie")]
        public string GetSerie(int idSerie)
        {
            if (idSerie > 8)
            {
                idSerie = 8;
            }

            string res = "{";
            string[] indiciSerie = new string[] { "SP_500", "FTSE_MIB", "GOLD_SPOT", "MSCI_EM", "MSCI_EURO", "All_Bonds", "US_Treasury" };
            string attribute = indiciSerie[idSerie];

            persistence.ReadColumnIndexAndCsv(attribute);

            Forecast forecast = new Forecast();
            res += forecast.forecastIndici(attribute);
            res += "}";

            return res;
        }

    }
}