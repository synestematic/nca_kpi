<?php
// header("Content-Description: File Transfer");
// header("Content-Transfer-Encoding: binary");
// header("Content-Disposition:attachment;filename=downloaded.png");
// header("Content-Type: image/png");
require_once("../private/initialize.php");
if (!$session->is_logged_in()) { redirect("login"); }

$logged_user = User::find_by_id($_SESSION["user_id"]);
if ($logged_user->su == 0) { redirect("users"); } //deveessere HR

$to_be_contested_user = User::find_by_id($_POST["id"]);
// if (!$to_be_contested_user) { redirect("hr"); }


$stringa_protocollo = '2017/CD/'.$logged_user->get_initials().'/'.$to_be_contested_user->get_initials();

$note = print_r($_POST) ;


if (isset($_POST['submit'])) {
    $string = 'Lei potrà presentare se lo riterrà opportuno, le Sue giustificazioni entro 5 giorni dal ricevimento della presente.' ;
    if ($_POST['suspend'] === 'true') {
        $string = 'Mentre attendiamo Sue eventuali giustificazioni entro 5 giorni dal ricevimento della presente, disponiamo la Sua sospensione cautelare immediata dal lavoro ma non dalla retribuzione.' ;
    }
}



?>

<html lang="it">
 <head>
  <title>Contestazione Disciplinare</title>
  <link rel="stylesheet" href="css/contestazioni.css" media="all" type="text/css" />
  <link rel="favicon" href="images/favicon.ico" type="image/x-icon">
</head>
 <body>
<?php
    echo '<div id="img_div"><img id="nca_hr_image" src="images/nca_hr.png"></div>' ;
    echo '<div id="div_1"><b>Noicompriamoauto.it SRL</b><br>Piazzale Luigi Cadorna, 2<br>CAP 20123 - Milano</div>' ;

    echo '<div id="div_2"><b>Raccomandata A MANO</b><br>'.'24.05.2017'.'</div>' ;

    echo '<div id="div_3">Egr. Sig.<br>'.$to_be_contested_user->full_name.'<br>'.$to_be_contested_user->address.'</div>' ;

    echo '<div id="div_6">Prot: '.$stringa_protocollo.'<br>Oggetto: contestazione disciplinare'.'</div>' ;

    echo '<div id="div_7">Ai sensi e per gli effetti di cui all\'art. 7 della legge 300/1970 (Statuto dei Lavoratori) e delle vigenti norme contrattuali Le contestiamo quanto segue:</div>' ;

    echo '<div id="div_8">'.$note.'</div>' ;

    echo '<div id="div_9">'.$string.'<br><br><br>Distinti Saluti</div>' ;



    echo '<div id="div_10"><b>NOI COMPRIAMO AUTO.IT S.r.l.</b><br>Sede Legale: Piazzale Luigi Cadorna n. 2<br>20123 Milano<br><br><br>_______________________________</div>' ;


    echo '<div id="pie1">Noicompriamoauto.it Srl<br>CF e P.IVA 08406540966</div>' ;
    echo '<div id="pie2">Iscritta presso il Registro delle Imprese di Milano n. MI-2024300<br>Socio Unico Auto1 Group GMBH<br>Cap. Sociale € 10.000<br>NoiCompriamoAuto.it Srl è soggetta a direzione e coordinamento da parte di AUTO1 Group Gmbh</div>' ;
    echo '<div id="pie3">Sede: Piazzale Cadorna 2 – 20123 Milano<br>Tel: 800 034 650</div>' ;




    // IL PDF CHE SI SALVA COMUNQUE VA FIRMATO E QUINDI SCANNERIZZATO.
    // QUINDI PER STAMPARLO SI PUO BENISSIMO USARE UN JPG

 ?>


</body>
</html>
