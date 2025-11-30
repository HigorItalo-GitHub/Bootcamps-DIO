using System.Text;
using System.Text.Json;
using RabbitMQ.Client;
using RabbitMQ.Client.Events;
using StockService.Data;

namespace StockService.Services;
public class RabbitMqListener
{
    private readonly StockContext _ctx;
    public RabbitMqListener(StockContext ctx) { _ctx = ctx; }

    public void StartListening()
    {
        Task.Run(() =>
        {
            try
            {
                var factory = new ConnectionFactory() { HostName = "rabbitmq" };
                using var connection = factory.CreateConnection();
                using var channel = connection.CreateModel();
                channel.ExchangeDeclare("orders", ExchangeType.Fanout, durable: false);
                var q = channel.QueueDeclare().QueueName;
                channel.QueueBind(q, "orders", "");
                var consumer = new EventingBasicConsumer(channel);
                consumer.Received += async (s, ea) =>
                {
                    var json = Encoding.UTF8.GetString(ea.Body.ToArray());
                    var msg = JsonSerializer.Deserialize<OrderCreatedMessage>(json);
                    if (msg != null)
                    {
                        foreach (var item in msg.Items)
                        {
                            var p = _ctx.Products.FirstOrDefault(pp => pp.Id == item.ProductId);
                            if (p != null) p.Quantity -= item.Quantity;
                        }
                        await _ctx.SaveChangesAsync();
                    }
                };
                channel.BasicConsume(q, autoAck: true, consumer: consumer);
                while (true) Thread.Sleep(1000);
            }
            catch { /* add logging and retry here */ }
        });
    }

    private class OrderCreatedMessage { public int OrderId { get; set; } public List<OrderItem> Items { get; set; } = new(); }
    private class OrderItem { public int ProductId { get; set; } public int Quantity { get; set; } }
}
