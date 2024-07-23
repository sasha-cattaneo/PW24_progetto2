<?php
include("config.php");
$connessione = mysqli_connect($host, $username, $password, $database);

if(!$connessione)
    die("Errore di connessione: " . $connessione->connect_error);

if($_GET['table']==""){
    die("ERRORE GET['table'] vuoto");
}else{
    $q = "SHOW CREATE TABLE ".$_GET['table'];
}

$query = $connessione->prepare($q);
if($query == false)
    die("Errore query:".$q);
$query->execute();
//print($query);
//$result = mysqli_query($connessione, $query);
$result = $query->get_result();

$table = $result->fetch_row();
echo $table[1];

echo "<br><br>";

$final_table = str_replace("`","",$table[1]);
$final_table = str_replace("int","INT",$final_table);
$final_table = str_replace("AUTO_INCREMENT","",$final_table);

$final_table = explode("ENGINE",$final_table)[0];

echo $final_table;

?>