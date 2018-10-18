using System.IO;
using System;
using System.Reflection;
using System.Text;


public class MainTest {
  public static int Main(string[] args){
    Console.WriteLine("TEST");
    StringBuilder builder=new StringBuilder();
    Assembly x=Assembly.LoadFile(Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "YUSoMeta.exe"));
    Console.WriteLine(x);
    var attrs=CustomAttributeData.GetCustomAttributes(x);
    Console.WriteLine(attrs);
    if (true)foreach (CustomAttributeData current in attrs)
    {
      if (current!=null){
        Console.WriteLine("HAVE ONE" + current.GetHashCode());
        //builder.Append(current.ToString());
      }else{
        Console.WriteLine("BAD");
      }
    }
    Console.WriteLine("GOT >> "+builder.ToString());
    return 0;


  }
}

