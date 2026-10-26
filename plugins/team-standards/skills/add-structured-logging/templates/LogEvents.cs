using Microsoft.Extensions.Logging;

namespace YourCompany.YourApi.Logging;

/// <summary>Standard event IDs for the team logging standard.</summary>
public static class LogEvents
{
    public static readonly EventId Received = new(1000, nameof(Received));
    public static readonly EventId Completed = new(1001, nameof(Completed));
    public static readonly EventId Failed = new(1002, nameof(Failed));
}
