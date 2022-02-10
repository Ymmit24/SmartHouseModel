<h1>Dynamic Log file</h1>
<h2><a href="/clearlog">Clear logs</a></h2>

%for line in lines:
{{ line }}<br/>
%end

<a href="/clearlog">Clear logs</a>

%rebase base title='Home', action='home'
