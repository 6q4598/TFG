using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using IOT4246.Data;

/*******************************************************************************
 * Builder                                                                     *
 *******************************************************************************/
var builder = WebApplication.CreateBuilder(args);
builder.Services.AddDbContext<IOT4246Context>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("IOT4246Context") ?? throw new InvalidOperationException("Connection string 'IOT4246Context' not found.")));

// Add services to the container.
builder.Services.AddControllersWithViews();

/*******************************************************************************
 * App                                                                         *
 *******************************************************************************/
var app = builder.Build();

// Configure the HTTP request pipeline.
if (!app.Environment.IsDevelopment()) {

    app.UseExceptionHandler("/Home/Error");

}

app.UseStaticFiles();
app.UseRouting();
app.UseAuthorization();
app.MapControllerRoute(name: "default", pattern: "{controller=Home}/{action=Index}/{id?}");
app.Run();
