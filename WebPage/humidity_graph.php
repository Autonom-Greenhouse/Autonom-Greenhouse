<?php // content="text/plain; charset=utf-8"
require_once ('jpgraph/jpgraph.php');
require_once ('jpgraph/jpgraph_line.php');
require_once( "jpgraph/jpgraph_date.php" );
//require_once ('sql.php');

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

//---------------------------------------------------------
//$start = time();
$sqlCommand = "SELECT air_humidity, time_stamp FROM measurements";
$result = $conn->query($sqlCommand);
$index1 = 0;
DEFINE('SAMPLERATE', 60);
$datay1 = array();
$xdata = array();




if ($result->num_rows > 0) {
   // output dta of each row
   while($row = $result->fetch_assoc()) {
        $datay1[$index1] = $row["air_humidity"];
        //$xdata[$index1] = $row["time_stamp"];
        
	$index1++;
   }
}

 else {
    $conn->close();
}

//---------------------------------------------------------

// Setup the graph
$graph = new Graph(900,800);
$graph->SetScale("textlin");

//$graph->xaxis->scale->SetTimeAlign(MINADJ_5);
 
//$graph->xaxis->scale->ticks->Set(10*60);

//$graph->xaxis->scale->SetDateFormat('H:i');

$theme_class=new UniversalTheme;

$graph->SetTheme($theme_class);
$graph->img->SetAntiAliasing(false);
$graph->title->Set('Air Humidity');
$graph->SetBox(false);

$graph->img->SetAntiAliasing();

$graph->yaxis->HideZeroLabel();
$graph->yaxis->HideLine(false);
$graph->yaxis->HideTicks(false,false);


$graph->xgrid->Show();
$graph->xgrid->SetLineStyle("solid");
$graph->xaxis->SetTickLabels(array());
$graph->xgrid->SetColor('#E3E3E3');
$graph->xaxis->SetTextTickInterval(30,0);

// Create the first line
$p1 = new LinePlot($datay1);
$graph->Add($p1);
$p1->SetColor("#6495ED");

$graph->legend->SetFrameWeight(1);

// Output line
$graph->Stroke();


//---------------------------------------------------------



?>