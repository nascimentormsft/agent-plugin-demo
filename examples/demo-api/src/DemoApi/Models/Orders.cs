namespace DemoApi.Models;

public record CreateOrderRequest(string OrderId, string ProductCode, int Quantity, string CustomerName, string CustomerEmail);

public record OrderResult(string OrderId, string Status);
