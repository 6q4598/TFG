using System.ComponentModel.DataAnnotations;

namespace IOT4246.Models {

    public class Database {

        public int Id { get; set; }
        public string? Title { get; set; }
        public string? Description { get; set; }
        public string? Genre { get; set; }

        [DataType(DataType.Date)]
        public DateTime ReleaseDate { get; set; }

    }

}
