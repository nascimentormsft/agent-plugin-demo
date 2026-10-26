using System.Collections.Concurrent;
using DemoApi.Models;

namespace DemoApi.Services;

public interface IOrderService
{
    Task<OrderResult> CreateAsync(CreateOrderRequest request, CancellationToken ct);
    Task<OrderResult?> GetAsync(string orderId, CancellationToken ct);
}

public class OrderService : IOrderService
{
    private readonly ConcurrentDictionary<string, OrderResult> _orders = new();

    public Task<OrderResult> CreateAsync(CreateOrderRequest request, CancellationToken ct)
    {
        if (request.Quantity <= 0)
        {
            throw new ArgumentOutOfRangeException(nameof(request), "Quantity must be positive.");
        }

        var result = new OrderResult(request.OrderId, "Accepted");
        _orders[request.OrderId] = result;
        return Task.FromResult(result);
    }

    public Task<OrderResult?> GetAsync(string orderId, CancellationToken ct) =>
        Task.FromResult(_orders.TryGetValue(orderId, out var result) ? result : null);
}
