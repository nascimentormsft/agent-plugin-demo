---
name: 'Team standard – structured logging (ASP.NET Core)'
description: 'Use when writing, changing or reviewing logging, error handling or tracing in ASP.NET Core / .NET Web API code (controllers, minimal API endpoints, services, middleware, background services).'
applyTo: 'src/**/*.cs'
---

# Structured logging – team standard for ASP.NET Core Web APIs

**Scope guard:** Apply these rules only to application code under `src/`. If the task is about
tests, documentation, build scripts or infrastructure files, ignore this file.

## Why
Support teams search logs by correlation ID and event name across all APIs. String-interpolated
log lines cannot be queried as structured fields, and logging full request bodies risks leaking
personal data or secrets into the log store.

## Rules
1. Log through `ILogger<T>` from `Microsoft.Extensions.Logging`, injected by constructor or
   primary constructor. Do NOT use `Console.WriteLine`, `Debug.WriteLine`, `Trace` or a new
   logging library.
2. Use **message templates** with named placeholders, never string interpolation:
   `logger.LogInformation("Order {OrderId} received", orderId)` – not `$"Order {orderId} received"`.
3. Log one event per step, with an `EventId` and PascalCase name: `Received` (1000),
   `Completed` (1001), `Failed` (1002). Use the constants in `src/Logging/LogEvents.cs`.
4. The correlation ID comes from the `CorrelationIdMiddleware` (`X-Correlation-ID` header,
   generated if missing) and is added to every log entry through a logging scope. Do not pass it
   by hand or create a second mechanism.
5. In the error path, log `Failed` with the exception as the **first argument**
   (`logger.LogError(ex, ...)`), then rethrow with `throw;` – never `throw ex;`.
6. NEVER log request or response bodies, personal data (names, email addresses, postal
   addresses), tokens, keys or connection strings. Log identifiers and status only.

## Example – preferred
```csharp
[ApiController]
[Route("api/orders")]
public class OrdersController(IOrderService orders, ILogger<OrdersController> logger) : ControllerBase
{
    [HttpPost]
    public async Task<ActionResult<OrderResult>> Create(CreateOrderRequest request, CancellationToken ct)
    {
        logger.LogInformation(LogEvents.Received, "Order {OrderId} received", request.OrderId);
        try
        {
            var result = await orders.CreateAsync(request, ct);
            logger.LogInformation(LogEvents.Completed, "Order {OrderId} completed with status {Status}",
                request.OrderId, result.Status);
            return Ok(result);
        }
        catch (Exception ex)
        {
            logger.LogError(LogEvents.Failed, ex, "Order {OrderId} failed", request.OrderId);
            throw;
        }
    }
}
```

## Example – avoid
```csharp
Console.WriteLine($"got request {JsonSerializer.Serialize(request)}"); // no logger, interpolated, logs the full body
```

## Done when
- Every endpoint logs `Received`, `Completed` and `Failed` through `ILogger<T>` with `LogEvents`.
- No `Console.WriteLine` / `Debug.WriteLine` and no interpolated log messages remain in changed files.
- `CorrelationIdMiddleware` is registered in `Program.cs` (`app.UseMiddleware<CorrelationIdMiddleware>()`).
- No log call includes a request/response body or a personal-data field.
