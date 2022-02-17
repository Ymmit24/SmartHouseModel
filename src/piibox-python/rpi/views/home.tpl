<h2>Timilehin in charge 2021/22</h2>
<h3>Energy modes</h3>
<table style="width:100%;margin-top:2em;margin-bottom:2em;padding:1em;">
<tr><th>Auto Mode</th><th>Turn off all</th><th>CO2 Mode</th><th>SolarPV Mode</th><th>Grid Mode</th></tr>
<tr>
<td style="text-align:left">
  <a class="btn {{ 'active' if deviceAuto == 1 else ''}}" href="/action?device=AutoMode&value=1">On</a> |
  <a class="btn {{ 'active' if deviceAuto == 0 else ''}}" href="/action?device=AutoMode&value=0">Off</a></td>
<td style="text-align:left">
  <a class="btn {{ 'active' if deviceAllOff == 1 else ''}}" href="/action?device=AllOff&value=1">On</a> |
  <a class="btn {{ 'active' if deviceAllOff == 0 else ''}}" href="/action?device=AllOff&value=0">Off</a></td>

<!-- Preparation for additional energy modes
<td style="text-align:left">
  <a class="btn {{ 'active' if deviceAllOff == 1 else ''}}" href="/action?device=AllOff&value=1">On</a> |
  <a class="btn {{ 'active' if deviceAllOff == 0 else ''}}" href="/action?device=AllOff&value=0">Off</a></td>
<td style="text-align:left">
  <a class="btn {{ 'active' if deviceAllOff == 1 else ''}}" href="/action?device=AllOff&value=1">On</a> |
  <a class="btn {{ 'active' if deviceAllOff == 0 else ''}}" href="/action?device=AllOff&value=0">Off</a></td>
<td style="text-align:left">
  <a class="btn {{ 'active' if deviceAllOff == 1 else ''}}" href="/action?device=AllOff&value=1">On</a> |
  <a class="btn {{ 'active' if deviceAllOff == 0 else ''}}" href="/action?device=AllOff&value=0">Off</a></td>
-->

</tr>
</table>

<h3><a href="/dashboard">Monitoring</a></h3>
<table style="width:100%;margin-top:2em;margin-bottom:2em;padding:1em;">
<tr><th>Total Load</th><th></tr>
<tr>
<td id="houseLoad" style="text-align:left">
  Loading...</td>
</tr>
<tr><th>Solar Generation</th><th>Net load</th><th>External Temp</th><th>Internal Temp</th></tr>
<tr>
<td id="solarFeed" style="text-align:left">
  Loading...</td>
<td id="netLoad" style="text-align:left">
  Loading...</td>
<td id="extTemp" style="text-align:left">
  Loading...</td>
<td id="intTemp" style="text-align:left">
  Loading...</td>
</tr>
<tr><th>Kitchen Temp</th><th>Dinning Temp</th><th>Bathroom Temp</th><th>Bedroom Temp</th></tr>
<tr>
<td id="kitchenTemp" style="text-align:left">
  Loading...</td>
<td id="dinningTemp" style="text-align:left">
  Loading...</td>
<td id="bathroomTemp" style="text-align:left">
  Loading...</td>
<td id="bedroomTemp" style="text-align:left">
  Loading...</td>
</tr>
</table>

<h3>Heating</h3>
<table style="width:100%;margin-top:2em;margin-bottom:2em;padding:1em;">
<tr><th>Downstairs Heating</th><th>Upstairs Heating</th><th>Hot Water Heating</th></tr>
<tr>
<td style="text-align:left">
  <a class="btn {{ 'active' if device1 == 1 else ''}}" href="/action?device=DownHeat&value=1">On</a> |
  <a class="btn {{ 'active' if device1 == 0 else ''}}" href="/action?device=DownHeat&value=0">Off</a></td>
<td style="text-align:left">
  <a class="btn {{ 'active' if device0 == 1 else ''}}" href="/action?device=UpHeat&value=1">On</a> |
  <a class="btn {{ 'active' if device0 == 0 else ''}}" href="/action?device=UpHeat&value=0">Off</a></td>
<td style="text-align:left">
  <a class="btn {{ 'active' if device12 == 1 else ''}}" href="/action?device=HotWater&value=1">On</a> |
  <a class="btn {{ 'active' if device12 == 0 else ''}}" href="/action?device=HotWater&value=0">Off</a></td>
</tr>
</table>

<!-- Comment here -->
<h3>Appliances</h3>
<table style="width:100%;margin-top:2em;margin-bottom:2em;padding:1em;">
<tr><th>Fridge</th><th>Cooker</th><th>Kettle</th><th>Dishwasher</th></th></tr>
<tr>
<td style="text-align:left">
  <a class="btn {{ 'active' if device15 == 1 else ''}}" href="/action?device=HomeSupply&value=1">On</a> |
  <a class="btn {{ 'active' if device15 == 0 else ''}}" href="/action?device=HomeSupply&value=0">Off</a></td>
<td style="text-align:left">
  <a class="btn {{ 'active' if device4 == 1 else ''}}" href="/action?device=Cooker&value=1">On</a> |
  <a class="btn {{ 'active' if device4 == 0 else ''}}" href="/action?device=Cooker&value=0">Off</a></td>
<td style="text-align:left">
  <a class="btn {{ 'active' if device13 == 1 else ''}}" href="/action?device=SolarPV&value=1">On</a> |
  <a class="btn {{ 'active' if device13 == 0 else ''}}" href="/action?device=SolarPV&value=0">Off</a></td>
<td style="text-align:left">
  <a class="btn {{ 'active' if device14 == 1 else ''}}" href="/action?device=BatteryStorage&value=1">On</a> |
  <a class="btn {{ 'active' if device14 == 0 else ''}}" href="/action?device=BatteryStorage&value=0">Off</a></td>
</tr>
<!--Comment here  -->

</table>
<h3>Lights</h3> 
<!--   
<img id="Image-Maps-Com-iesd-demo-map" src="/static/img/Demo_house.png" class="map" border="0" width="1400" height="455" orgWidth="1400" orgHeight="455" usemap="#iesd-demo-map" alt="" />
<map name="iesd-demo-map" id="ImageMapsCom-iesd-demo-map">
<area id="Bed1" alt="MasterBedroom" title="MasterBedroom" href="/action?device=Bed1Light&value={{ '0' if device9 == 1 else '1'}}" shape="rect" coords="70,156,327,300" target="_self"  data-maphilight='{"strokeColor":"000000","strokeWidth":5,"fillColor":"ffff00","fillOpacity":0.6}'   />
<area id="Bed2" alt="Bedroom2" title="Bedroom2" href="/action?device=Bed2Light&value={{ '0' if device10 == 1 else '1'}}" shape="rect" coords="329,155,586,299" target="_self"  data-maphilight='{"strokeColor":"000000","strokeWidth":5,"fillColor":"ffff00","fillOpacity":0.6}'   />
<area id="LivingRoom" alt="LivingRoom" title="LivingRoom" href="/action?device=LivingLight&value={{ '0' if device5 == 1 else '1'}}" shape="rect" coords="72,304,375,444"   data-maphilight='{"strokeColor":"000000","strokeWidth":5,"fillColor":"ffff00","fillOpacity":0.6}'   />
<area id="DiningRoom" alt="DiningRoom" title="DiningRoom" href="/action?device=DiningLight&value={{ '0' if device7 == 1 else '1'}}" shape="rect" coords="378,304,586,443"  target="_self" data-maphilight='{"strokeColor":"000000","strokeWidth":5,"fillColor":"ffff00","fillOpacity":0.6}'    />
<area id="Bed3" alt="Bedroom3" title="Bedroom3" href="/action?device=Bed3Light&value={{ '0' if device11 == 1 else '1'}}" shape="rect" coords="1163,160,1325,299" target="_self" data-maphilight='{"strokeColor":"000000","strokeWidth":5,"fillColor":"ffff00","fillOpacity":0.6}'    />
<area id="Bathroom" alt="Bathroom" title="Bathroom" href="/action?device=BathroomLight&value={{ '0' if device8 == 1 else '1'}}" shape="rect" coords="807,158,963,297"  target="_self" data-maphilight='{"strokeColor":"000000","strokeWidth":5,"fillColor":"ffff00","fillOpacity":0.6}'    />
<area id="Kitchen" alt="Kitchen" title="Kitchen" href="/action?device=KitchenLight&value={{ '0' if device2 == 1 else '1'}}" shape="rect" coords="808,302,985,445"  target="_self" data-maphilight='{"strokeColor":"000000","strokeWidth":5,"fillColor":"ffff00","fillOpacity":0.6}'    />
<area shape="rect" coords="1398,453,1400,455" alt="Image Map" style="outline:none;" title="Image Map" href="http://www.image-maps.com/index.php?aff=mapped_users_0" />
</map> -->

<table style="width:100%;margin-top:2em;margin-bottom:2em;padding:1em;">
<tr><th>Master Bedroom</th><th>Bedroom 2</th><th>Bedroom 3</th><th>Bathroom</th></tr>
<tr>
<td style="text-align:left">
  <a class="btn {{ 'active' if device9 == 1 else ''}}" href="/action?device=Bed1Light&value=1">On</a> |
  <a class="btn {{ 'active' if device9 == 0 else ''}}" href="/action?device=Bed1Light&value=0">Off</a></td> 
<td style="text-align:left">
  <a class="btn {{ 'active' if device10 == 1 else ''}}" href="/action?device=Bed2Light&value=1">On</a> |
  <a class="btn {{ 'active' if device10 == 0 else ''}}" href="/action?device=Bed2Light&value=0">Off</a></td>
<td style="text-align:left">
  <a class="btn {{ 'active' if device11 == 1 else ''}}" href="/action?device=Bed3Light&value=1">On</a> |
  <a class="btn {{ 'active' if device11 == 0 else ''}}" href="/action?device=Bed3Light&value=0">Off</a></td>
<td style="text-align:left">
  <a class="btn {{ 'active' if device8 == 1 else ''}}" href="/action?device=BathroomLight&value=1">On</a> |
  <a class="btn {{ 'active' if device8 == 0 else ''}}" href="/action?device=BathroomLight&value=0">Off</a></td>
</tr>
</table>   

<table style="width:100%;margin-top:2em;margin-bottom:2em;padding:1em;">
<tr><th>Living Room</th><th>Dining Room</th><th>Kitchen</th><th>&nbsp;</th></tr>
<tr>
<td style="text-align:left">
  <a class="btn {{ 'active' if device5 == 1 else ''}}" href="/action?device=LivingLight&value=1">On</a> |
  <a class="btn {{ 'active' if device5 == 0 else ''}}" href="/action?device=LivingLight&value=0">Off</a></td>
<td style="text-align:left">
  <a class="btn {{ 'active' if device7 == 1 else ''}}" href="/action?device=DiningLight&value=1">On</a> |
  <a class="btn {{ 'active' if device7 == 0 else ''}}" href="/action?device=DiningLight&value=0">Off</a></td>
<td style="text-align:left">
  <a class="btn {{ 'active' if device2 == 1 else ''}}" href="/action?device=KitchenLight&value=1">On</a> |
  <a class="btn {{ 'active' if device2 == 0 else ''}}" href="/action?device=KitchenLight&value=0">Off</a></td>
  <td>&nbsp;</td>
  </tr>
</table>
   
<!-- Comment here
<h3>Kitchen</h3>
<table style="width:100%;margin-top:2em;margin-bottom:2em;padding:1em;">
<tr><th>Light</th><th>Fridge</th><th>Cooker</th></tr>      
<tr>
<td style="text-align:left">
  <a class="btn {{ 'active' if device2 == 1 else ''}}" href="/action?device=KitchenLight&value=1">On</a> |
  <a class="btn {{ 'active' if device2 == 0 else ''}}" href="/action?device=KitchenLight&value=0">Off</a></td>
  <td style="text-align:left">
  <a class="btn {{ 'active' if device4 == 1 else ''}}" href="/action?device=Cooker&value=1">On</a> |
  <a class="btn {{ 'active' if device4 == 0 else ''}}" href="/action?device=Cooker&value=0">Off</a></td>
</tr>
</table>
-->

<!-- Comment here -->
<h3>Living Room</h3>
<table style="width:100%;margin-top:2em;margin-bottom:2em;padding:1em;">
<tr><th>Light</th><th>TV</th> <!-- <th>SolarPV</th><th>BatteryStorage</th> --></tr>      
<tr>
<td style="text-align:left">
  <a class="btn {{ 'active' if device5 == 1 else ''}}" href="/action?device=LivingLight&value=1">On</a> |
  <a class="btn {{ 'active' if device5 == 0 else ''}}" href="/action?device=LivingLight&value=0">Off</a></td>
<td style="text-align:left">
  <a class="btn {{ 'active' if device6 == 1 else ''}}" href="/action?device=TV&value=1">On</a> |
  <a class="btn {{ 'active' if device6 == 0 else ''}}" href="/action?device=TV&value=0">Off</a></td>
<!--
<td style="text-align:left">
  <a class="btn {{ 'active' if device13 == 1 else ''}}" href="/action?device=SolarPV&value=1">On</a> |
  <a class="btn {{ 'active' if device13 == 0 else ''}}" href="/action?device=SolarPV&value=0">Off</a></td>
<td style="text-align:left">
  <a class="btn {{ 'active' if device14 == 1 else ''}}" href="/action?device=BatteryStorage&value=1">On</a> |
  <a class="btn {{ 'active' if device14 == 0 else ''}}" href="/action?device=BatteryStorage&value=0">Off</a></td>
-->
</tr>
</table>
<!-- -->

<!-- <p>Live camera stream of demo house</p>
<iframe seamless height=640 src = "/webcam" scrolling="no">
It appears that your browser does not support iFrames.
</iframe> -->

<!-- Comment
<p style="text-align:left;"><a href="/log">View device log</a></p>
-->

%rebase base title='Home', action='home'

