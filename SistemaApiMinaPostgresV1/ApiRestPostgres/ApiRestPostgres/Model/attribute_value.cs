using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace ApiRestPostgres.Model
{
    [Table("attribute_value", Schema = "your_schema_name")]
    public class Attribute_value
    {
        [Key]
        public int? attribute_id { get; set; }

        public DateTime? date { get; set; }
        public int? entity_type_id { get; set; }
        public int? entity_id { get; set; }
        public int? operational_unit_id { get; set; }
        public double? value { get; set; }
        public string? string_value { get; set; }
        public int? fault { get; set; }

        public DateTime? last_change_date { get; set; }


        // Construtor padrão
        public Attribute_value() { }

        // Construtor com todos os campos
        public Attribute_value(DateTime? date, int? entityTypeId, int? entityId, int? attributeId, int? operationalUnitId, double? value, string? stringValue, int? fault, DateTime? last_change_date)
        {
            this.date = date;
            this.entity_type_id = entityTypeId;
            this.entity_id = entityId;
            this.attribute_id = attributeId;
            this.operational_unit_id = operationalUnitId;
            this.value = value;
            this.string_value = stringValue;
            this.fault = fault;
            this.last_change_date = last_change_date;
        }

        // Construtor com apenas o ID do atributo
        public Attribute_value(int? attribute_id)
        {
            this.attribute_id = attribute_id;
        }
    }
}