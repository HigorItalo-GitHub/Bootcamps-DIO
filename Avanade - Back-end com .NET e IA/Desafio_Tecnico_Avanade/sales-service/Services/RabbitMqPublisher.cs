using System.Text;
using System.Text.Json;
using RabbitMQ.Client;
using SalesService.Models;

namespace SalesService.Services;
public class RabbitMqPublisher
{
    public Task PublishOrderCreated(Order order)
    {
        var factory = new ConnectionFactory() { HostName = "rabbitmq" };
        using var connection = factory.CreateConnection();
        using var channel = connection.CreateModel();
        channel.ExchangeDeclare("orders", ExchangeType.Fanout, durable: false);
        var msg = new OrderCreatedMessage { OrderId = order.Id, Items = order.Items.Select(i => new OrderItemMsg { ProductId = i.ProductId, Quantity = i.Quantity }).ToList() };
        var body = Encoding.UTF8.GetBytes(JsonSerializer.Serialize(msg));
        channel.BasicPublish("orders", "", basicProperties: null, body: body);
        return Task.CompletedTask;
    }
    private class OrderCreatedMessage { public int OrderId { get; set; } public List<OrderItemMsg> Items { get; set; } = new(); }
    private class OrderItemMsg { public int ProductId { get; set; } public int Quantity { get; set; } }
}
