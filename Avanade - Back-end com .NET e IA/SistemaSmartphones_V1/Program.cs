using DesafioPOO.Models;

// Realizando os testes com as classes Nokia e Iphone
Smartphone aparelho1 = new Nokia("001", "Kph2025", "199923764829", 32);
Smartphone aparelho2 = new Iphone("002", "Iph2025", "19801883643", 64);

Console.WriteLine($"Operando smartphone Nokia (número{aparelho1.Numero}):");
aparelho1.Ligar();
aparelho1.ReceberLigacao();
aparelho1.InstalarAplicativo("WhatsApp");

Console.WriteLine($"Operando smartphone Iphone (número {aparelho2.Numero}):");
aparelho2.Ligar();
aparelho2.ReceberLigacao();
aparelho1.InstalarAplicativo("Telegram");