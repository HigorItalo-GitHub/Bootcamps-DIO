using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using StockService.Data;
using StockService.Models;

namespace StockService.Controllers;
[ApiController]
[Route("api/[controller]")]
[Authorize]
public class ProductsController : ControllerBase
{
    private readonly StockContext _ctx;
    public ProductsController(StockContext ctx) => _ctx = ctx;

    [HttpPost]
    public async Task<IActionResult> Create(Product p)
    {
        _ctx.Products.Add(p);
        await _ctx.SaveChangesAsync();
        return CreatedAtAction(nameof(GetById), new { id = p.Id }, p);
    }

    [AllowAnonymous]
    [HttpGet]
    public async Task<IActionResult> GetAll() => Ok(await _ctx.Products.ToListAsync());

    [AllowAnonymous]
    [HttpGet("{id:int}")]
    public async Task<IActionResult> GetById(int id)
    {
        var p = await _ctx.Products.FindAsync(id);
        return p == null ? NotFound() : Ok(p);
    }

    [HttpPost("adjust/{id:int}")]
    public async Task<IActionResult> Adjust(int id, [FromQuery] int delta)
    {
        var p = await _ctx.Products.FindAsync(id);
        if (p == null) return NotFound();
        p.Quantity += delta;
        if (p.Quantity < 0) return BadRequest(new { Error = "Resulting stock cannot be negative" });
        await _ctx.SaveChangesAsync();
        return Ok(p);
    }
}
