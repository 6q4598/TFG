using Microsoft.AspNetCore.Mvc;
using System.Text.Encodings.Web;

namespace MvcMovie.Controllers;

public class HelloWorldController : Controller {

    // 
    // GET: /HelloWorld/
    public IActionResult Index () {

        return View();

    }

    // 
    // GET: /HelloWorld/Welcome/ 
    public IActionResult Welcome (string s, int k = 1) {

        ViewData["Message"] = "Hello " + s;
        ViewData["NumTimes"] = k;
        return View();
        // return HtmlEncoder.Default.Encode($"Hello {str} num is {k}");

    }

}
