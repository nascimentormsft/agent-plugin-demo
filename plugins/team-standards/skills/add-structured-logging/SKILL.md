---
name: add-structured-logging
description: Adds the team's structured logging to an ASP.NET Core Web API controller, minimal API endpoint or service. Use when asked to "add logging", "instrument" or "make this endpoint observable" in C# code under src/.
---

# Add structured logging to an ASP.NET Core Web API

Follow the team logging standard: the `structured-logging` instruction shipped in this plugin
(a copy is in [../setup-project-instructions/templates/structured-logging.instructions.md](../setup-project-instructions/templates/structured-logging.instructions.md)).

## Steps
1. Make sure the project has the shared logging building blocks. If a file is missing, create it
   from the template, adjusting only the namespace to the project's root namespace:
   - `src/<Project>/Logging/LogEvents.cs` from [templates/LogEvents.cs](templates/LogEvents.cs)
   - `src/<Project>/Logging/CorrelationIdMiddleware.cs` from [templates/CorrelationIdMiddleware.cs](templates/CorrelationIdMiddleware.cs)
2. Register the middleware in `Program.cs` early in the pipeline, before the endpoints:
   `app.UseMiddleware<CorrelationIdMiddleware>();`
   To include scopes in console output during development, add to `appsettings.Development.json`:
   `"Logging": { "Console": { "FormatterName": "json", "FormatterOptions": { "IncludeScopes": true } } }`
3. In the controller, endpoint or service the user points to:
   - inject `ILogger<T>` (constructor or primary constructor);
   - log `LogEvents.Received` at the start, `LogEvents.Completed` before returning, and
     `LogEvents.Failed` with the exception in a `catch` that ends with `throw;`;
   - use message templates with named placeholders (`{OrderId}`), never `$"..."`.
4. Remove `Console.WriteLine` / `Debug.WriteLine` calls in the changed code.
5. Never log request or response bodies, personal data, tokens or keys.
6. Run `dotnet build` and fix any errors.
7. Finish with a short checklist showing each "Done when" item from the instruction and whether it is met.
