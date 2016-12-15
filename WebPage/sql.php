<?php 

$servername = "localhost";
$username = "root";
$password = "raspberry";
$dbname = "Greenhouse";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
} 

$sql = "SELECT light, soil_moist, air_humidity, air_temp, Timestamp FROM measurements";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // output data of each row
    while($row = $result->fetch_assoc()) {
        echo "light: " . $row["light"]. " Soil: " . $row["soil_moist"]. " Air humidity " . $row["air_humidity"]. " Air Temp " . $row["air_temp"]. " Timestamp " . $row["Timestamp"]. "<br>";
    }
} else {
    echo "0 results";
}
$conn->close();

phpinfo();

?>