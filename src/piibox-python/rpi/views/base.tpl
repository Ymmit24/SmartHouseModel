<!DOCTYPE html><html>
<head>
  <title>{{title or 'No title'}}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link href="/static/css/bootstrap-flatly.min.css" rel="stylesheet" media="screen">
  <link href="/static/css/custom.css" rel="stylesheet" media="screen">
  <link href="/static/css/bootstrap-responsive.min.css" rel="stylesheet" media="screen">
  <script type="text/javascript" src="/static/js/jquery-1.10.2.min.js"></script>
  <script type="text/javascript" src="/static/js/jquery.maphilight.js"></script>
   
    <script type="text/javascript">
     
    //WebSocket handling code    
    $(document).ready(function() 
    {
        
        connect();
        
        function connect()
        {
            try
            {
                var host = "ws://"+window.location.host+"/websocket";
                var socket = getSocket(host);
                if (socket == null)
                {
                    alert("To monitor the house, the browser requires Websocket support, sorry!!");
                }

                    socket.onmessage = function(msg){
                         parsedMsg  = JSON && JSON.parse(msg.data) || $.parseJSON(msg.data);
                         
                         if (parsedMsg.intTemp)
                         {
                             document.getElementById("intTemp").innerHTML = parseFloat(parsedMsg.intTemp);
                         }
                         if (parsedMsg.extTemp)
                         {
                             document.getElementById("extTemp").innerHTML = parseFloat(parsedMsg.extTemp);
                         }
                         if (parsedMsg.houseLoad)
                         {
                            document.getElementById("houseLoad").innerHTML = (Math.round(1000 *parseFloat(parsedMsg.houseLoad)))/1000;
                         } 
                         if (parsedMsg.solarFeed)
                         {
                            document.getElementById("solarFeed").innerHTML = (Math.round(1000 *parseFloat(parsedMsg.solarFeed)))/1000;
                         }              
                         if (parsedMsg.houseLoad && (parsedMsg.solarFeed+0.1))
                         {
                             netLoad = (Math.round(1000 *parseFloat(parsedMsg.houseLoad)))/1000;
                             document.getElementById("netLoad").innerHTML = netLoad;
                         }
                         if (parsedMsg.kitchenTemp)
                         {
                            document.getElementById("kitchenTemp").innerHTML = parseFloat(parsedMsg.kitchenTemp);
                         }
                         if (parsedMsg.dinningTemp)
                         {
                            document.getElementById("dinningTemp").innerHTML = parseFloat(parsedMsg.dinningTemp);
                         }
                         if (parsedMsg.bathroomTemp)
                         {
                            document.getElementById("bathroomTemp").innerHTML = parseFloat(parsedMsg.bathroomTemp);
                         }
                         if (parsedMsg.bedroomTemp)
                         {
                            document.getElementById("bedroomTemp").innerHTML = parseFloat(parsedMsg.bedroomTemp);
                         }
                    }

                    //socket.onclose = function(){
                        // message('<p class="event">Socket Status: '+socket.readyState+' (Closed)');
                    //}			

            } catch(exception)
            {
                 message('<p>Error'+exception);
            }
        }
        
        function getSocket(host)
        {
                    if(window.WebSocket)
                        return new WebSocket(host);
                    else if(window.MozWebSocket)
                        return new MozWebSocket(host);
                    else
                        return null;
        }
        
    });

    </script>
    
<!--  <meta http-equiv="refresh" content="2;" > -->
</head>
<body>
  %include includes/header action=action

  <div class="container">
    %include
  </div>

  %include includes/footer

</body>
</html>
