
<!DOCTYPE html>
<html>
<body>

<h1>Autonomous Greenhouse: A LTU-student project</h1>

<h2>Sensor Graphs</h2>
<a href="/graph.php">Air Temperature</a>
<br>
<a href="/moist_graph.php">Soil Moisture</a>
<br>
<a href="/humidity_graph.php">Air Humidity</a>
<br>
<a href="/light_graph.php">Light Value</a>
<br>

<h2>Greenhouse Status</h2>

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

$sql = "SELECT light, soil_moist, air_humidity, air_temp, time_stamp FROM measurements ORDER BY time_stamp DESC LIMIT 1";
$result = $conn->query($sql);


if ($result->num_rows > 0) {
    // output data of each row
    while($row = $result->fetch_assoc()) {
    	echo "Air Temperature " . $row["air_temp"]. "°C" . "<br>";
    	echo "Soil Moisture: " . $row["soil_moist"]. "<br>";
    	echo "Air Humidity " . $row["air_humidity"]. "<br>";
        echo "Light Value: " . $row["light"]. "<br>";
        echo " Timestamp " . $row["time_stamp"]. "<br>";
        echo gettype($time_stamp);
        echo float(4.04); // 4.04

    }
} else {
    echo "0 results";
}
$conn->close();



?>


</body>
</html>

