using System;
using System.Windows;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using IOT4246.Models;
using Microsoft.Data.Sqlite;
using System.Data.Entity;

namespace IOT4246.Data {

    public class IOT4246Context : DbContext {

        //public IOT4246Context (DbContextOptions<IOT4246Context> options) : base(options) {

        //}

        public new DbSet<IOT4246.Models.Database> Database { get; set; } = default!;

        public int ConnectDb() {

            try {

                var connection = new SqliteConnection("Data Source=C:\\Users\\farrufi\\Documents\\TFG\\4246\\esp32.db;");
                connection.Open();
                SqliteCommand selectVal = new SqliteCommand(connection);
                selectVal.CommandText = "select id from esp32_table";
                selectVal.CommandType = System.Data.CommandType.Text;


            }

            catch {

                // TODO:
                // Implementar pagina 400.
                return -1;

            }

            return 0;

        }

    }

}
