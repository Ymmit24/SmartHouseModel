
<table style="width:100%;margin-top:2em;margin-bottom:2em;padding:1em;">
<tr><th>Hot Water</th><th>Space Heating</th></tr>
<tr>
<td style="text-align:center">
  <a class="btn {{ 'active' if device0 == 1 else ''}}" href="/action?device=0&value=1">On</a> |
  <a class="btn {{ 'active' if device0 == 0 else ''}}" href="/action?device=0&value=0">Off</a></td>
<td style="text-align:center">
  <a class="btn {{ 'active' if device1 == 0 else ''}}" href="/action?device=1&value=0">On</a> |
  <a class="btn {{ 'active' if device1 == 1 else ''}}" href="/action?device=1&value=1">Off</a></td>
</tr>
</table>
<p>Live camera stream of demo house</p>
<iframe seamless height=640 src = "http://iesd.dmu.ac.uk:12346/webcam.mjpeg" scrolling="no">
It appears that your browser does not support iFrames.
</iframe>
<p style="text-align:center;"><a href="/log">View device log</a></p>

%rebase base title='Home', action='home'

