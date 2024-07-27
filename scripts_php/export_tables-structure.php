<?php
// Creo connessione al DB
include("config.php");
$connessione = mysqli_connect($host, $username, $password, $database);

// In caso di errore di connessione termino e restituisco l'errore
if(!$connessione)
    die("Errore di connessione: " . $connessione->connect_error);

// Controllo se sono stati passati, tramite GET o POST, i parametri necessari
// cioè la lista di tabelle da esportare
// Salvo la lista in una variabile
$table_list = "";
    if($_GET['table']=="" || !isset($_GET['table'])){
        if($_POST['table']=="" || !isset($_POST['table'])){
            die("ERRORE GET['table'] e POST['table'] vuoto");
        }else{
            $table_list = $_POST['table'];
        }
    }else{
        $table_list = $_GET['table'];
    }
// Per ogni tabella richiesta chiamo una query per ottenere la sua struttura
// Salvo il risultato in un array
$tables = array();
foreach($table_list as $i => $value){
    $q = "DESCRIBE ".$value;

    $query = $connessione->prepare($q);
    if($query == false)
        die("Errore query:".$q);
    $query->execute();
    //print($query);
    //$result = mysqli_query($connessione, $query);
    $result = $query->get_result();

    // Creo un array chiave:valore dal nome della tabella e il risultato della query 
    $tables[] = tableToArray($value, $result);
}
mysqli_close($connessione);

header('Content-Type: application/json; charset=utf-8');
echo json_encode($tables);
?>

<?php
// Creo un array chiave:valore
function tableToArray ($table, $result){
    
    $rows = array();

    while($row = $result->fetch_assoc()) {
        $rows[] = $row;
    }

    $json_table = array($table => $rows);

    return $json_table;
}
?>