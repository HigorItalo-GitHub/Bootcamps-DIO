namespace SalesService.Models;
public class Order
{
    public int Id { get; set; }
    public string Customer { get; set; } = null!;
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    public List<OrderItem> Items { get; set; } = new();
    public string Status { get; set; } = "Pending";
}
public class OrderItem { public int ProductId { get; set; } public int Quantity { get; set; } }
