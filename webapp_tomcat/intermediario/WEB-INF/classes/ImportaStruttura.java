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

public class ImportaStruttura extends HttpServlet {

    @Override
    public void doGet(HttpServletRequest request, HttpServletResponse response)
        throws IOException, ServletException
    {
        String[] params = request.getParameterValues("table");
        String param_string = "";
        for (String p : params){
            param_string += "table[]="+p+"&";
        }
        param_string = param_string.substring(0, param_string.length() -1);

        HttpRequest request_http = HttpRequest.newBuilder()
			.uri(URI.create("http://cattaneo5ie.altervista.org/PW24/db_interaction/export_tables.php?"+param_string))
			.method("GET", HttpRequest.BodyPublishers.noBody())
			.build();
		HttpResponse<String> response_http = null;
        
		try {
			response_http = HttpClient.newHttpClient().send(request_http, HttpResponse.BodyHandlers.ofString());
		} catch (IOException e) {
			e.printStackTrace();
		} catch (InterruptedException e) {
			e.printStackTrace();
		}

        response.setContentType("application/json");
        response.setCharacterEncoding("UTF-8");
        
        PrintWriter out = response.getWriter();
        out.println(response_http.body());
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

        HttpRequest request_http = HttpRequest.newBuilder()
			.uri(URI.create("http://cattaneo5ie.altervista.org/PW24/db_interaction/export_tables.php?"+param_string))
			.method("GET", HttpRequest.BodyPublishers.noBody())
			.build();
		HttpResponse<String> response_http = null;
        
		try {
			response_http = HttpClient.newHttpClient().send(request_http, HttpResponse.BodyHandlers.ofString());
		} catch (IOException e) {
			e.printStackTrace();
		} catch (InterruptedException e) {
			e.printStackTrace();
		}

        response.setContentType("application/json");
        response.setCharacterEncoding("UTF-8");
        
        PrintWriter out = response.getWriter();
        out.println(response_http.body());
    }
}