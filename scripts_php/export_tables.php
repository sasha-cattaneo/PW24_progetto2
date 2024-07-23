<?php
include("config.php");
$connessione = mysqli_connect($host, $username, $password, $database);

if(!$connessione)
    die("Errore di connessione: " . $connessione->connect_error);

if($_GET['table']=="" || !isset($_GET['table'])){
    die("ERRORE GET['table'] vuoto");
}
$tables = array();
foreach($_GET['table'] as $i => $value){
    $q = "DESCRIBE ".$value;

    $query = $connessione->prepare($q);
    if($query == false)
        die("Errore query:".$q);
    $query->execute();
    //print($query);
    //$result = mysqli_query($connessione, $query);
    $result = $query->get_result();

    $tables[] = tableToArray($value, $result);
}

echo json_encode($tables);
?>

<?php
function tableToArray ($table, $result){
    
    $rows = array();

    while($row = $result->fetch_assoc()) {
        $rows[] = $row;
    }

    $json_table = array($table => $rows);

    return $json_table;
}
?>