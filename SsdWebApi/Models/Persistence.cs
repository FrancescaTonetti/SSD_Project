using System;
using System.Collections.Generic;
using Microsoft.EntityFrameworkCore;
using System.IO;
using System.Linq;

namespace SsdWebApi.Models
{
    public class Persistence
    {
        private readonly IndiciContext _context;

        public Persistence(IndiciContext context)
        {
            _context = context;
        }


        public List<string> ReadColumnIndexAndCsv(string attribute)
        {
            List<string> indiciSerie = new List<string>();
            StreamWriter writer = new StreamWriter(attribute + ".csv", false);

            indiciSerie.Add(attribute);
            writer.WriteLine(attribute);

            using (var command = _context.Database.GetDbConnection().CreateCommand())
            {
                command.CommandText = $"SELECT {attribute} FROM indici";
                _context.Database.OpenConnection();
                using (var reader = command.ExecuteReader())
                {
                    while (reader.Read())
                    {
                        writer.WriteLine(reader[attribute]);
                        indiciSerie.Add(reader[attribute].ToString());
                    }
                }
            }
            writer.Close();

            return indiciSerie;
        }

}
}