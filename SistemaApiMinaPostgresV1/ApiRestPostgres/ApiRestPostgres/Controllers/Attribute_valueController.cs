using Microsoft.AspNetCore.Mvc;
using ApiRestPostgres.Model;
using ApiRestPostgres.ViewModel;
using Microsoft.EntityFrameworkCore.Metadata.Internal;
using Microsoft.Extensions.Primitives;
using static System.Runtime.InteropServices.JavaScript.JSType;
using System;

namespace ApiRestPostgres.Controllers
{
    [ApiController]
    [Route("api/vq/Attribute_value")]
    public class Attribute_valueController : ControllerBase
    {

        private readonly IAttribute_valueRepository _ValueRepository;

        public Attribute_valueController(IAttribute_valueRepository valueRepository)
        {
            _ValueRepository = valueRepository;
        }


        [HttpPost]
        public IActionResult Add(Attribute_valueViewModelcs Attribute_valueView)
        {
            var attribute_values = new Attribute_value(Attribute_valueView.date, Attribute_valueView.entity_type_id, Attribute_valueView.entity_id, Attribute_valueView.attribute_id, Attribute_valueView.operational_unit_id, Attribute_valueView.value, Attribute_valueView.string_value, Attribute_valueView.fault, Attribute_valueView.last_change_date);


            _ValueRepository.Add(attribute_values);


            return Ok();


        }


        [HttpGet]
        public IActionResult Get()
        {
            var attribute_values = _ValueRepository.Get();

            return Ok(attribute_values);    


        }
    }
}
