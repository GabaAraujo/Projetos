using ApiRestPostgres.Model;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;

namespace ApiRestPostgres.infraestrutura
{
    public class ConnectionContext : DbContext
    {
        // faz a conexão
        public DbSet<Attribute_value> Attribute_values { get; set; }

        // construtor postgress acesso de dados
        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            if (!optionsBuilder.IsConfigured)
            {
                optionsBuilder.UseNpgsql(
                    "Server=localhost;" +
                    "Port=5432;Database=jmc;" +
                    "User Id=postgres;" +
                    "Password=1234;"
                );

                // Configure logging
                optionsBuilder.UseLoggerFactory(LoggerFactory.Create(builder =>
                {
                    builder.AddConsole(); // Output to console
                    // You can add more logging providers here, like Debug, etc.
                }));

                // Enable detailed errors
                optionsBuilder.EnableSensitiveDataLogging();
            }
        }

        // Define schema for entities
        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            // Specify schema for each entity
            modelBuilder.Entity<Attribute_value>().ToTable("attribute_value", schema: "hm_attr");
            // Add other entities with their schemas if needed
        }
    }
}