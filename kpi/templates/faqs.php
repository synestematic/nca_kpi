<?php require_once("private/initialize.php"); ?>
<?php include(LIB_PATH.DS."htmls".DS."header.php"); ?>
<body bgcolor="#f3f3f5">
<header>
	<img src="images/logo-small.png" alt="" align="left">
	<h1><b>Merchants | Domande Frequenti</b></h1>
</header>
<nav></nav> <!-- orange line -->





<section class="cd-faq">
	<ul class="cd-faq-categories">
		<li><a class="selected" href="#documenti">Documenti</a></li>
		<li><a href="#trasporti">Trasporti</a></li>
		<li><a href="#auto1">Auto1.com</a></li>
		<li><a href="#iva">IVA</a></li>
		<li><a href="#bollo">Bollo</a></li>
		<li><a href="#coc">Coc</a></li>
		<li><a href="#reclami">Reclami</a></li>
		<li><a href="#altro">Altro</a></li>
	</ul>

	<div class="cd-faq-items">
		<ul id="documenti" class="cd-faq-group">
			<li class="cd-faq-title"><h2>Documenti</h2></li>

			<li>
				<a id="docsTool1" class="cd-faq-trigger" href="#0">A che punto è il passaggio di proprietà della mia macchina? Avete ricevuto i documenti che vi ho inviato?</a>
				<div id="docsTool2" class="cd-faq-content">
					<p>Inserendo lo Stock ID della vettura acquistata è possibile seguire l'avanzamento del relativo passaggio di proprietà e l'eventuale ricezione della documentazione necessaria.</p><br>
			     <iframe src="documents.php" height="190px" width="100%"></iframe><br>
				  <p></p>
				</div>
			</li>

			<li>
				<a class="cd-faq-trigger" href="#0">Come funziona il processo di consegna dei documenti?</a>
				<div class="cd-faq-content">
					<p>Per i nuovi merchant Finproget vi invierà, il giorno dopo il primo acquisto, tramite mail, l’elenco dei documenti da rispedire rispondendo alla mail, in particolar modo il modello C-Corr fondamentale per il ritiro DHL dei moduli TT2120 e ACI PRA presso l'indirizzo fornitoci.<br>
					Per i merchant che hanno già acquistato in passato, Finproget ha già i vostri documenti. Qualora finproget avesse finito i documenti TT2120 e ACI /PRA  invierà la mail con il modello C-Corr per il ritiro dei documenti attraverso il corriere DHL a carico di Auto1.<br><i>
					Il passaggio di proprietà avverrà solamente dopo il pagamento dell’auto e la ricezione di tutti i documenti, e verrà fatto in 4-5 giorni lavorativi.</i><br></p>
				</div>
			</li>

			<li>
				<a class="cd-faq-trigger" href="#0">In quanto tempo viene effettuato il passaggio di proprietà?</a>
				<div class="cd-faq-content">
					<p>Dall’arrivo del corriere per il ritiro dei documenti originali, si possono considerare 2-3 giorni lavorativi entro i quali sarà effettuato il passaggio di proprietà.</p>
				</div>
			</li>
		</ul>

		<ul id="trasporti" class="cd-faq-group">
			<li class="cd-faq-title"><h2>Trasporti</h2></li>

			<li>
				<a id="transpTool" class="cd-faq-trigger" href="#0">Quali sono i costi di trasporto della mia macchina?</a>
				<div class="cd-faq-content">
					<p>Attraverso la seguente piattaforma è possibile calcolare i costi di trasporto in base al punto di partenza e di arrivo della vettura acquistata.</p><br>
					<iframe src="transports.php" height="234px" width="100%"></iframe>
					<div id="blue">I prezzi sono da considerarsi IVA esclusa per i trasporti nazionali ed esenti IVA per i trasporti internazionali.</div>
				</div>
			</li>

			<li>
				<a class="cd-faq-trigger" href="#0">Come funziona il processo di consegna della macchina?</a>
				<div class="cd-faq-content">
					<p>Sulla DASHBOARD è possibile indicare il metodo di trasporto richiesto: PICK-UP o TRANSPORT.<br>
					La data di pick-up potrà essere inserita solo dopo il passaggio di proprietà e il ticket per il ritiro della vettura arriverà dopo l'inserimento della stessa.<br></p>
				</div>
			</li>

			<li>
				<a class="cd-faq-trigger" href="#0">Qualè l'indirizzo del mio Centro di Stoccaggio?</a>
				<div class="cd-faq-content">
					<p>I Centri di Stoccaggio sono aperti tutti i giorni dal Lunedì al Venerdì.</p><br>
					<table id="documents_table">
						<tr>
							<th>Centro di>Stoccaggio</th>
							<th>Indirizzo</th>
							<th>Orario</th>
						</tr>
						<tr>
							<td>Cagliari</td>
							<td>SS. 130 dir Km 2.200 - Decimomannu (CA)</td>
							<td>h 09:00 -13:00<br>14:00-18:30</td>
						</tr>
						<tr>
							<td>Lucernate di Rho</td>
							<td>Via Magenta, 60 - Lucernate di Rho</td>
							<td>h 09:00 -13:00<br>14:00-17:00</td>
						</tr>
						<tr>
							<td>Napoli</td>
							<td>Via La Monaca, 5 - Capua</td>
							<td>h 09:00 -13:00<br>14:00-17:30</td>
						</tr>
						<tr>
							<td>Ostia Antica</td>
							<td>Via Federico Bazzini, 20 - Ostia Antica</td>
							<td>h 09:00 -13:00<br>14:00-17:00</td>
						</tr>
						<tr>
							<td>Padova</td>
							<td>Corso Spagna, 12 - Padova</td>
							<td>h 09:00 -13:00<br>14:00-17:00</td>
						</tr>
						<tr>
							<td>Parma</td>
							<td>Via Romagnoli,25 San Polo di Torrile - Parma</td>
							<td>h 08:00-12:00<br>14:00-17:30</td>
						</tr>
						<tr>
							<td>Torino</td>
							<td>Via G. Reiss Romoli 122/05 INT N - Torino</td>
							<td>h 08:00-12:00<br>14:00-17:00</td>
						</tr>
						<tr>
							<td>Verona</td>
							<td>Via dell'Industria , 20 - Castelnuovo del Garda</td>
							<td>h 09:00-13:00<br>15:00-19:00</td>
						</tr>
					</table>
				</div>
			</li>

			<li>
				<a class="cd-faq-trigger" href="#0">Ho scelto come modalità di consegna il trasporto e non mi è ancora arrivata la macchina, come mai?</a>
				<div class="cd-faq-content">
					<p>Nel caso il merchant abbia scelto come modalità di consegna il trasporto e questo sia INTERNAZIONALE, le tempistiche sono di 15 giorni lavorativi dall’avvenuto pagamento della fattura di trasporto. Se invece il trasporto fosse NAZIONALE le tempistiche sono di 10 giorni lavorativi dal pagamento della fattura di trasporto e del passaggio di proprietà.</p>
				</div>
			</li>

			<li>
				<a class="cd-faq-trigger" href="#0">Non riesco a rispettare la data di pick-up che ho inserito, come posso fare?</a>
				<div class="cd-faq-content">
					<p>Auto1 si riserva la possibilità di addebitare al merchant la somma di € 15,00 per ogni giorno successivo alla data di pick-up.</p>
				</div>
			</li>

			<li>
				<a class="cd-faq-trigger" href="#0">E’ possibile passare a ritirare l'auto prima della data di pick-up?</a>
				<div class="cd-faq-content">
					<p>Non è possibile ritirare l’auto prima della data di pick-up senza prima aver ricevuto il ticket necessario.</p>
				</div>
				</li>
		</ul> <!-- cd-faq-group -->

		<ul id="auto1" class="cd-faq-group">
			<li class="cd-faq-title"><h2>Auto1.com</h2></li>

			<li>
				<a class="cd-faq-trigger" href="#0">Non sono ancora attivo e non vedo i prezzi delle auto, come mai?</a>
				<div class="cd-faq-content">
					<p>Non è possibile vedere i prezzi delle auto fino a quando non si è in possesso delle credenziali di accesso al sito Auto1.<br>
					Per attivare le proprie credenziali, bisogna inviare una mail a <a href="mailto:commercianti@auto1.com">commercianti@auto1.com</a> allegando la propria visura camerale e il proprio recapito telefonico.<br>
					Verrete contattati da un commerciale per attivare la propria posizione.</p>
				</div>
			</li>
		</ul>

		<ul id="iva" class="cd-faq-group">
			<li class="cd-faq-title"><h2>IVA</h2></li>

			<li>
				<a class="cd-faq-trigger" href="#0">Come posso chiedere il rimborso dell'IVA?</a>
				<div class="cd-faq-content">
					<p>E’ possibile chiedere il rimborso dell’IVA, per le auto IVA ESPOSTA e per le auto importate in Italia dall’estero, solo se esse hanno raggiunto la loro destinazione finale e il merchant ha pagato la fattura ed è in possesso della bolla di trasporto.  È possibile chiedere il rimborso inviando una mail a <a href="mailto:iva.italy@auto1.com">iva.italy@auto1.com</a>
					allegando modulo di rimborso corrispondente alla nazionalità dell’auto, CMR, IBAN, SWIFT e intestatario del conto.<br><br></p>
					<a href="files/purchase_declarations_for_export_de.pdf" target="_blank">Scarica il modulo per la GERMANIA</a><br>
					<a href="files/purchase_declarations_for_export_de_new.pdf" target="_blank">Scarica il modulo per la GERMANIA</a> (per auto acquistate dal 16/01/2017)<br>
					<a href="files/purchase_declarations_for_export_fr_new.pdf" target="_blank">Scarica il modulo per la FRANCIA</a><br>
					<a href="files/purchase_declarations_for_export_es.pdf" target="_blank">Scarica il modulo per la SPAGNA</a><br>
					<a href="files/purchase_declarations_for_export_be.pdf" target="_blank">Scarica il modulo per il BELGIO</a><br>
					<a href="files/purchase_declarations_for_export_be_new.pdf" target="_blank">Scarica il modulo per il BELGIO</a> (per auto acquistate dal 09/02/2017 e per auto vendute dal 11/02/2017)<br>
					<a href="files/purchase_declarations_for_export_nl.pdf" target="_blank">Scarica il modulo per l'OLANDA</a><br>
					<a href="files/purchase_declarations_for_export_nl_new.pdf" target="_blank">Scarica il modulo per l'OLANDA</a> (validità dal 24/01/2017)<br>
					<a href="files/purchase_declarations_for_export_pl.pdf" target="_blank">Scarica il modulo per la POLONIA</a><br>
					<a href="files/purchase_declarations_for_export_se.pdf" target="_blank">Scarica il modulo per la SVEZIA</a><br>
					<a href="files/purchase_declarations_for_export_at.pdf" target="_blank">Scarica il modulo per l'AUSTRIA</a><br>
					<a href="files/purchase_declarations_for_export_at_new.pdf" target="_blank">Scarica il modulo per l'AUSTRIA</a> (validità dal 24/01/2017)<br>
					<!-- </p> -->
				</div>
			</li>
		</ul>

		<ul id="bollo" class="cd-faq-group">
			<li class="cd-faq-title"><h2>BOLLO</h2></li>

			<li>
				<a class="cd-faq-trigger" href="#0">Come posso conoscere la situazione bollo di un'auto?</a>
				<div class="cd-faq-content">
					<p>In materia di bollo auto la nostra società segue le direttive imposte dalla Regione Lombardia riguardo la sospensione del bollo.<br>
					E’ possibile contattarci per verificare, sul sito della Regione Lombardia, se il veicolo è stato messo in esenzione da parte nostra fornendo Stock ID e targa della vettura richiesta.</p>
				</div>
			</li>

		</ul>

		<ul id="coc" class="cd-faq-group">
			<li class="cd-faq-title"><h2>COC</h2></li>

			<li>
				<a class="cd-faq-trigger" href="#0">Come faccio per ottenere il Certificato di Conformità dell'auto?</a>
				<div class="cd-faq-content">
					<p>Se questo documento era indicato nella scheda del veicolo e non è stato recapitato potete richiederlo aprendo un reclamo. Se invece il documento non era in nostro possesso potete richiederlo sul sito <a href="https://www.eurococ.eu/it" target="_blank">www.eurococ.eu</a>
					<br>
					</p>
				</div>
			</li>

		</ul>

					<ul id="reclami" class="cd-faq-group">
						<li class="cd-faq-title"><h2>RECLAMI</h2></li>

						<li>
							<a class="cd-faq-trigger" href="#0">Come faccio per presentare un reclamo?</a>
							<div class="cd-faq-content">
								<p>E’ possibile presentare un reclamo direttamente dalla propria DASHBOARD.<br><br><a href="files/guida_reclami.pdf" target="_blank">Scarica la GUIDA RECLAMI</a>
								<br>
								</p>
							</div>
						</li>

						<li>
							<a class="cd-faq-trigger" href="#0">Quanto tempo ho per presentare un reclamo?</a>
							<div class="cd-faq-content">
								<p>E’ possibile presentare un reclamo entro 7 giorni dalla consegna dell’auto.</p>
							</div>
						</li>

						<li>
							<a class="cd-faq-trigger" href="#0">Ho presentato un reclamo e non ho ancora ricevuto risposta, come mai?</a>
							<div class="cd-faq-content">
								<p>La risposta al reclamo è prevista dopo 10 giorni dalla presentazione dello stesso, se completo della documentazione richiesta.<br>
								<br>
								</p>
							</div>
						</li>

					</ul>

					<ul id="altro" class="cd-faq-group">
						<li class="cd-faq-title"><h2>Altro</h2></li>
						<li>
							<a class="cd-faq-trigger" href="#0">La mia domanda non è presente tra quelle sopra elencate, come posso fare?</a>
							<div class="cd-faq-content">
								<p>Per qualsiasi domanda è possibile contattare il supporto telefonico al numero <a href="tel:00390294751066">+39 02 9475 1066</a> oppure inviare una mail all’indirizzo <a href="mailto:aftersales.italy@auto1.com">aftersales.italy@auto1.com</a> .<br></p>
							</div>
						</li>
					</ul>
	</div>
	<a href="#0" class="cd-close-panel">Close</a>
	<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>
	<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>
	<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>
</section>



<footer>
	<h1>Domande? Auto1.com Servizio Clienti <a href="tel:00390294751066">+39 02 9475 1066</a></h1>
</footer>
<script src="js/jquery-2.1.1.js"></script>
<script src="js/jquery.mobile.custom.min.js"></script>
<script src="js/main.js"></script> <!-- Resource jQuery -->
</body>
<?php include(LIB_PATH.DS."htmls".DS."footer.php"); ?>
