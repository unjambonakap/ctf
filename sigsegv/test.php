<?php
for ($i = 0; $i < 2e9; $i++){
		$h1 = md5("a". $i . "Shrewk");
		if($h1 == "0")
		{
				echo "<!--Bien joué le flag est ".$i."-->";
		}
}
?>
