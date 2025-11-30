using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using SalesService.Data;
using SalesService.Models;
using SalesService.Services;

namespace SalesService.Controllers;
[ApiController]
[Route("api/[controller]")]
[Authorize]
public class OrdersController : ControllerBase
{
    private readonly SalesContext _ctx;
    private readonly RabbitMqPublisher _publisher;
    public OrdersController(SalesContext ctx, RabbitMqPublisher publisher) { _ctx = ctx; _publisher = publisher; }

    [HttpPost]
    public async Task<IActionResult> Create(Order order)
    {
        if (order.Items == null || !order.Items.Any()) return BadRequest(new { Error = "Order must contain items" });

        // In a real flow, check product availability via HTTP call to stock-service
        // Here we rely on eventual consistency: create order and publish event
        _ctx.Orders.Add(order);
        await _ctx.SaveChangesAsync();

        await _publisher.PublishOrderCreated(order);

        order.Status = "Confirmed";
        await _ctx.SaveChangesAsync();

        return CreatedAtAction(nameof(GetById), new { id = order.Id }, order);
    }

    [HttpGet("{id:int}")]
    public async Task<IActionResult> GetById(int id)
    {
        var o = await _ctx.Orders.FindAsync(id);
        return o == null ? NotFound() : Ok(o);
    }

    [HttpGet]
    public async Task<IActionResult> GetAll() => Ok(await _ctx.Orders.ToListAsync());
}
