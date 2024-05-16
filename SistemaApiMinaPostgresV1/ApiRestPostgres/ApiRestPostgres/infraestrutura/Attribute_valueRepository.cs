using ApiRestPostgres.Model;

namespace ApiRestPostgres.infraestrutura
{
  

            public class Attribute_valueRepository : IAttribute_valueRepository
            {

                private readonly ConnectionContext _context = new ConnectionContext();  


                public void Add(Attribute_value attribute_value)
                {
                    _context.Attribute_values.Add(attribute_value);
                    _context.SaveChanges();
                }

                public List<Attribute_value> Get()
                {
                    return _context.Attribute_values.ToList();
            }
        }

    
}
