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
 * ImportaStruttura chiama "export_tables-structure.php" su altervista, 
 * inviando come parametro una lista di tabelle di cui si vuole la struttura. 
 * Viene restituito un body JSON contenente le strutture richieste
 * 
 * @param lista di tabelle da importare usando metodo GET o POST, chiave 'table'
 * 
 * @return json con le strutture delle tabelle richieste
 */

public class ImportaStruttura extends HttpServlet {

    @Override
    public void doGet(HttpServletRequest request, HttpServletResponse response)
        throws IOException, ServletException
    {
        // Estraggo la lista di tabelle dai parametri 'table'
        String[] params = request.getParameterValues("table");
        // Con la lista di tabelle creo una stringa formattata come query string (key=value)
        String param_string = "";
        for (String p : params){
            param_string += "table[]="+p+"&";
        }
        param_string = param_string.substring(0, param_string.length() -1);

        //Chiamo lo script PHP, passando la stringa dei parametri
        HttpRequest request_http = HttpRequest.newBuilder()
			.uri(URI.create("http://cattaneo5ie.altervista.org/PW24/db_interaction/export_tables-structure.php?"+param_string))
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
        
        //Restituisco il json ottenuto dallo script PHP
        PrintWriter out = response.getWriter();
        out.println(response_http.body());
    }

    @Override
    public void doPost(HttpServletRequest request, HttpServletResponse response)
        throws IOException, ServletException
    {
        // Estraggo la lista di tabelle dai parametri 'table'
        String[] params = request.getParameterValues("table");
        // Con la lista di tabelle creo una stringa formattata come query string (key=value)
        String param_string = "";
        for (String p : params){
            param_string += "table[]="+p+"&";
        }
        param_string = param_string.substring(0, param_string.length() -1);

        //Chiamo lo script PHP, passando la stringa dei parametri
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
        
        //Restituisco il json ottenuto dallo script PHP
        PrintWriter out = response.getWriter();
        out.println(response_http.body());
    }
}