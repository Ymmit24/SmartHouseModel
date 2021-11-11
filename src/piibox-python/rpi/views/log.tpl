<h1>Dynamic Demand Log</h1>
%for line in lines:
{{ line }}<br/>
%end

<a href="/clearlog">Clear logs</a>

%rebase base title='Home', action='home'
