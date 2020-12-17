using Microsoft.EntityFrameworkCore;

namespace SsdWebApi.Models
{
    /* Storage Model:
    Classe che contiene il modello del database, 
    quella che verrà istanziata e farà le chiamate object services.
    */
    public class IndiciContext : DbContext
    {
        public IndiciContext(DbContextOptions<IndiciContext> options) 
            : base(options)
        {

        }

        public DbSet<Indici> indici {get; set;}
    }
}