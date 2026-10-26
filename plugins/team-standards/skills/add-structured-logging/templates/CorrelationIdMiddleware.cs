using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;

namespace YourCompany.YourApi.Logging;

/// <summary>
/// Reads the X-Correlation-ID header (or creates one), returns it in the response,
/// and adds it to every log entry written during the request through a logging scope.
/// Register in Program.cs: app.UseMiddleware&lt;CorrelationIdMiddleware&gt;();
/// </summary>
public sealed class CorrelationIdMiddleware(RequestDelegate next, ILogger<CorrelationIdMiddleware> logger)
{
    public const string HeaderName = "X-Correlation-ID";

    public async Task InvokeAsync(HttpContext context)
    {
        var correlationId = context.Request.Headers.TryGetValue(HeaderName, out var value)
                            && !string.IsNullOrWhiteSpace(value)
            ? value.ToString()
            : Guid.NewGuid().ToString();

        context.TraceIdentifier = correlationId;
        context.Response.OnStarting(() =>
        {
            context.Response.Headers[HeaderName] = correlationId;
            return Task.CompletedTask;
        });

        using (logger.BeginScope(new Dictionary<string, object> { ["CorrelationId"] = correlationId }))
        {
            await next(context);
        }
    }
}
