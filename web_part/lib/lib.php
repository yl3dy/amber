<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html lang=ru>

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
function show_search() {
	echo '	<div id="searchbar">';
	echo '		[________________________________________________________________________] [Поиск]';
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
