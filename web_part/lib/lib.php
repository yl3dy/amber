<!--eeeeCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd"-->
<ht1ml lang=ru>

<head>
	<meta content="text/html; charset=utf-8" http-equiv="content-type">
	<meta content="ru-RU" http-equiv="content-language">
	<link rel="stylesheet" type="text/css" href="/styles/struct.css">
	<link rel="stylesheet" type="text/css" href="/styles/text.css">
	<title>Amber search system</title>
</head>

<body>
<div id="container">
    <div id="header"><img src="/images/logo.png"></div>
<?php
function check_search()
{
	if($_GET['s']==1)
	{
		$descriptorspec = array(
		   0 => array("pipe", "r"),  // stdin - канал, из которого дочерний процесс будет читать
  		   1 => array("pipe", "w"),  // stdout - канал, в который дочерний процесс будет записывать 
  		   2 => array("file", "/tmp/error-output.txt", "a") // stderr - файл для записи;
		);

		$process = proc_open('oberon search', $descriptorspec, $pipes, NULL, NULL);

		if (is_resource($process)) {
    		// $pipes теперь выглядит так:
    		// 0 => записывающий обработчик, подключенный к дочернему stdin
    		// 1 => читающий обработчик, подключенный к дочернему stdout
   			 // Вывод сообщений об ошибках будет добавляться в /tmp/error-output.txt
		
    		fwrite($pipes[0], htmlspecialchars($_POST['quest']));
    		fclose($pipes[0]);
			$col_vo=0;
	
			$strt=stream_get_contents($pipes[1]);
			$arr=explode("\n",$strt);

			foreach ($arr as $tt)
			{
				echo  '<a href="'.$tt.'">'.$tt.'</a><br/>';
			} 
//    fclose($pipes[1]);
//			$col_vo=fread($pipes[1],2046)
//			echo $colvo
    		fclose($pipes[1]);

			 proc_close($process);
		}
	}

}
function show_search() {
	echo '	<div id="searchbar">';
	echo '	<form action="index.php?s=1" method="post">
			<input type="text" name="quest"/>
			<input type="submit"/>
			</form>';
	echo '	</div>';
}
function show_menu($name) {
	$sections["news"]         = "Новости";
	$sections["add_to_index"] = "Добавить в поисковый индекс";
	$sections["__links__"]    = "resources";

	echo "	<div id=\"menublock\">\n";
	echo "		<ul class=\"menu\">\n";
    foreach($sections as $key => $value) {
		if($key == "__links__") {
			show_resource_list();
			continue;
		}

        if($name == $key)
			echo "			<li><strong>$value</strong></li>\n";
		else {
			echo "			<li><a href=\"/$key/\">$value</a></li>\n";
		}
	}
	echo '	</div>';
}
function show_resource_list() {
	echo "			<li>Ресурсы локалки</li>\n";
	echo "			<li><ul class=\"default\">\n";
	echo "				<li>Борда</li>\n";
	echo "				<li>Расписание электричек</li>\n";
	echo "				<li>Официальный сайт института</li>\n";
	echo "				<li>Сайт ФПФЭ</li>\n";
	echo "			</ul></li>\n";
}
function show_footer() {
	echo "<div id=\"footer\">Created by blablabla</div> </div></body></html>";
}
?>
