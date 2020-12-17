using System;
using System.Drawing;

namespace SsdWebApi.Models
{
    public class Forecast
    {
        public Forecast()
        {

        }

        public string forecastIndici()
        {
            string res = "";
            string interpreter = @"/opt/anaconda3/bin/python";            
            string environment = "opanalytics";

            int timeout = 10000;
            
            PythonRunner pythonRunner = new PythonRunner(interpreter, environment, timeout);

            try
            {
                string command = $"Models/Module1.py";
                string list = pythonRunner.runDosCommands(command);

                if (string.IsNullOrWhiteSpace(list))
                {
                    Console.WriteLine("Lista:"+ list);
                    Console.WriteLine("Error in the script call");
                    goto lend;
                }

                string[] lines = list.Split(new[] { Environment.NewLine }, StringSplitOptions.None);
                Console.WriteLine("lines"+lines);
                
                foreach (string s in lines)
                {
                    res += s;
                }
 
                goto lend;
            }
            catch (Exception exception)
            {  
                Console.WriteLine(exception.ToString());
                goto lend;
            }

            lend:
            return res;
        }
    }
}