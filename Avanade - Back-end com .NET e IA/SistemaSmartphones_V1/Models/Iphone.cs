namespace DesafioPOO.Models
{
    // Cria classe "Iphone" que herda da classe "Smartphone"
    public class Iphone : Smartphone
    {
        public Iphone(string numero, string modelo, string imei, int memoria) : base (numero, modelo, imei, memoria) {}

        // Sobrescrição do método "InstalarAplicativo"
        public override void InstalarAplicativo(string nomeApp)
        {
            Console.WriteLine($"Instalando aplicativo '{nomeApp}'...");
        }
    }
}