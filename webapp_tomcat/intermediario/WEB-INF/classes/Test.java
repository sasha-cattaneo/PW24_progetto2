import java.io.IOException;
import java.io.PrintWriter;
import java.util.ResourceBundle;

import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import java.net.http.*;
import java.net.URI;

import com.google.gson.*;

/**
 * Servlet per la importare DB da PHPmyAdmin.
 *
 * @author Sasha Cattaneo
 * @author Ilaria Roma
 */

/**
 * IDEA
 * 
 * Intermediario può essere chiamata dalla pagina html,
 * contenente una select per selezionare quali tabelle scaricare da altervista,
 * oppure direttamente da URI, passando come (GET o POST)? la/e tabella/e da ottenere.
 * 
 * Quindi Intermediario deve chiamare la pagina PHP su altervista, che 
 * restituirà un body JSON, e reindirizzare la risposta a chi la chiamata.
 */

public class Test extends HttpServlet {

    @Override
    public void doGet(HttpServletRequest request, HttpServletResponse response)
        throws IOException, ServletException
    {
        // String[] params = request.getParameterValues("table");
        // String param_string = "";
        // for (String p : params){
        //     param_string += "table[]="+p+"&";
        // }
        // param_string = param_string.substring(0, param_string.length() -1);

        java.util.Map<String, String[]> params = request.getParameterMap();
        
        Object [] keys = params.keySet().toArray();

        response.setContentType("application/json");
        response.setCharacterEncoding("UTF-8");
        
        PrintWriter out = response.getWriter();
        if(keys.length==0)
            out.println("<p>No params</p>");
        else{
            for(int i=0; i<keys.length; i++ )
            {
                String item = (String)keys[i];
                String value = params.get(item)[0];
                out.println("<p>" + item + "=" + value + "</p>");

            }
        }
    }

    @Override
    public void doPost(HttpServletRequest request, HttpServletResponse response)
        throws IOException, ServletException
    {
        String[] params = request.getParameterValues("table");
        String param_string = "";
        for (String p : params){
            param_string += "table[]="+p+"&";
        }
        param_string = param_string.substring(0, param_string.length() -1);
        
        PrintWriter out = response.getWriter();
        out.println(param_string);
        // java.util.Map<String, String[]> params = request.getParameterMap();
        
        // Object [] keys = params.keySet().toArray();

        // response.setContentType("application/json");
        // response.setCharacterEncoding("UTF-8");
        
        // PrintWriter out = response.getWriter();
        // if(keys.length==0)
        //     out.println("<p>No params</p>");
        // else{
        //     for(int i=0; i<keys.length; i++ )
        //     {
        //         String item = (String)keys[i];
        //         String value = params.get(item)[0];
        //         out.println("<p>" + item + "=" + value + "</p>");

        //     }
        // }
    }
}