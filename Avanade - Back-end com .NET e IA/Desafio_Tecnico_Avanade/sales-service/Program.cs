using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.EntityFrameworkCore;
using Microsoft.IdentityModel.Tokens;
using SalesService.Data;
using SalesService.Services;
using System.Text;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var conn = builder.Configuration.GetConnectionString("DefaultConnection") ?? builder.Configuration["ConnectionStrings__DefaultConnection"];
if (string.IsNullOrEmpty(conn)) conn = "Server=(localdb)\\mssqllocaldb;Database=SalesDb;Trusted_Connection=True;";
builder.Services.AddDbContext<SalesContext>(opt => opt.UseSqlServer(conn));

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

builder.Services.AddSingleton<RabbitMqPublisher>();
var app = builder.Build();
if (app.Environment.IsDevelopment()) { app.UseSwagger(); app.UseSwaggerUI(); }
app.UseAuthentication();
app.UseAuthorization();
app.MapControllers();
app.Run();