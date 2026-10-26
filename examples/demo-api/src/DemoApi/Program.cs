using DemoApi.Services;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddSingleton<IOrderService, OrderService>();

var app = builder.Build();

app.MapControllers();

app.Run();
