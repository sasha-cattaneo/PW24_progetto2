<?php
include("config.php");
$connessione = mysqli_connect($host, $username, $password, $database);

if(!$connessione)
    die("Errore di connessione: " . $connessione->connect_error);

if($_GET['table']==""){
    die("ERRORE GET['table'] vuoto");
}else{
    $q = "DESCRIBE ".$_GET['table'];
}

$query = $connessione->prepare($q);
if($query == false)
    die("Errore query:".$q);
$query->execute();
//print($query);
//$result = mysqli_query($connessione, $query);
$result = $query->get_result();

echo toJSON($_GET['table'], $result);
?>

<?php
function toJSON ($table, $result){
    
    $rows = array();

    while($row = $result->fetch_assoc()) {
        $rows[] = $row;
    }

    $json_table = array($table => $rows);

    return json_encode($json_table);
}

?>