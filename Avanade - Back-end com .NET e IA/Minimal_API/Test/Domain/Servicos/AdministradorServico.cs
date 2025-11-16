using System.Reflection;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using MinimalAPI.Dominio.Servicos;
using MinimalAPI.Entidades;
using MinimalAPI.Infraestrutura.Db;

namespace Test.Domain.Entidades;

[TestClass]
public class AdministradorServicoTest
{
    private DbContexto CriarContextoDeTeste()
    {
        var assemblyPath = Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location);
        var path = Path.GetFullPath(Path.Combine(assemblyPath ?? "", "..", "..", ".."));

        var builder = new ConfigurationBuilder()
            .SetBasePath(path ?? Directory.GetCurrentDirectory())
            .AddJsonFile("appsettings.json", optional: false, reloadOnChange: true)
            .AddEnvironmentVariables();

        var configuration = builder.Build();

        var connectionString = configuration.GetConnectionString("MySql");

        var options = new DbContextOptionsBuilder<DbContexto>()
            .UseMySql(connectionString, ServerVersion.AutoDetect(connectionString))
            .Options;

        return new DbContexto(options);
    }

    [TestMethod]
    public void TestarSalvarAdministrador()
    {
        // Arrange
        var context = CriarContextoDeTeste();
        context.Database.ExecuteSqlRaw("DELETE FROM Administradores");

        var adm = new Administrador
        {
            Email = "teste@teste.com",
            Senha = "teste",
            Perfil = "Adm"
        };

        var administradorServico = new AdministradorServico(context);

        // Act
        administradorServico.Incluir(adm);
        Console.WriteLine($"ID após SaveChanges: {adm.Id}");

        var todos = administradorServico.Todos(1);

        // Assert
        Assert.IsTrue(todos.Any(), "Nenhum administrador foi retornado do banco.");
        Assert.IsTrue(todos.Any(a => a.Id == adm.Id), "O administrador inserido não foi encontrado.");
    }

    [TestMethod]
    public void TestarBuscaPorId()
    {
        // Arrange
        var context = CriarContextoDeTeste();
        context.Database.ExecuteSqlRaw("DELETE FROM Administradores");

        var adm = new Administrador
        {
            Email = "teste@teste.com",
            Senha = "teste",
            Perfil = "Adm"
        };

        var administradorServico = new AdministradorServico(context);

        // Act
        administradorServico.Incluir(adm);
        // Console.WriteLine($"ID após SaveChanges: {adm.Id}");

        var admBanco = administradorServico.BuscaPorId(adm.Id);

        // Assert
        Assert.IsNotNull(admBanco, "Administrador não encontrado no banco.");
        Assert.AreEqual(adm.Id, admBanco.Id, "O ID retornado do banco não corresponde ao ID inserido.");
        Assert.AreEqual(adm.Email, admBanco.Email, "O e-mail retornado não corresponde ao inserido.");
    }
}
