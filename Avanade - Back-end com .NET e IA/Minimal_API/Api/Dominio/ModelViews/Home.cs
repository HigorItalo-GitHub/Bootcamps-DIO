namespace MinimalAPI.Dominio.ModelViews;

public struct Home
{
    public string Mensagem { get => "Bem vindo à documentação de veículos - Minimal API"; }
    public string Documentacao { get => "/swagger"; }
}