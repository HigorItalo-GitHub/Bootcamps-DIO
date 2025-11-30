using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.EntityFrameworkCore;
using Microsoft.IdentityModel.Tokens;
using StockService.Data;
using StockService.Services;
using System.Text;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var conn = builder.Configuration.GetConnectionString("DefaultConnection") ?? builder.Configuration["ConnectionStrings__DefaultConnection"];
if (string.IsNullOrEmpty(conn))
{
    // fallback to localdb for dev
    conn = "Server=(localdb)\\mssqllocaldb;Database=StockDb;Trusted_Connection=True;";
}
builder.Services.AddDbContext<StockContext>(opt => opt.UseSqlServer(conn));

var key = Encoding.ASCII.GetBytes(builder.Configuration["JWT_SECRET"] ?? "THIS_IS_A_DEMO_SECRET_KEY_CHANGE_IT");
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme).AddJwtBearer(options =>
{
    options.RequireHttpsMetadata = false;
    options.SaveToken = true;
    options.TokenValidationParameters = new TokenValidationParameters
    {
        ValidateIssuerSigningKey = true,
        IssuerSigningKey = new SymmetricSecurityKey(key),
        ValidateIssuer = false,
        ValidateAudience = false
    };
});

builder.Services.AddSingleton<RabbitMqListener>();
var app = builder.Build();

if (app.Environment.IsDevelopment()) { app.UseSwagger(); app.UseSwaggerUI(); }

app.UseAuthentication();
app.UseAuthorization();
app.MapControllers();

// Start listener
var listener = app.Services.GetRequiredService<RabbitMqListener>();
listener.StartListening();

app.Run();