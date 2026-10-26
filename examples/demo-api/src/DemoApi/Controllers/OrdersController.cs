using System.Text.Json;
using DemoApi.Models;
using DemoApi.Services;
using Microsoft.AspNetCore.Mvc;

namespace DemoApi.Controllers;

// Demo target for the plugin: this controller deliberately does NOT follow the logging standard.
[ApiController]
[Route("api/orders")]
public class OrdersController(IOrderService orders) : ControllerBase
{
    [HttpPost]
    public async Task<ActionResult<OrderResult>> Create(CreateOrderRequest request, CancellationToken ct)
    {
        Console.WriteLine($"got request {JsonSerializer.Serialize(request)}");
        var result = await orders.CreateAsync(request, ct);
        Console.WriteLine("done");
        return Ok(result);
    }

    [HttpGet("{orderId}")]
    public async Task<ActionResult<OrderResult>> Get(string orderId, CancellationToken ct)
    {
        var result = await orders.GetAsync(orderId, ct);
        if (result is null)
        {
            return NotFound();
        }

        return Ok(result);
    }
}
