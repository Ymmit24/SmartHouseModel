<div class="navbar navbar-inverse navbar-fixed-top">
	<div class="navbar-inner">
		<div class="container">
			<button type="button" class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
				<span class="icon-bar"></span> <span class="icon-bar"></span> <span class="icon-bar"></span>
			</button>
			<a class="brand" href="/">Smart House</a>
			<div class="nav-collapse collapse">
				<ul class="nav">
					<li
					%if action == 'home':
					 class="active"
					%end
					><a href="/">Home</a></li>
					 <li 
					%if action == 'about':
           class="active"
          %end
          ><a href="/about">About</a></li>

<li
					%if action == 'camera':
	 class='active'
					%end
					><a href="http://10.14.137.70:8080">Camera</a></li>
       <li					<li
					%if action == 'dashboard':
	 class='active'
					%end
					><a href="/dashboard">Dashboard</a></li>
       <li
       %if action == 'sitemap':
     class='active'
       %end
					><a href="/sitemap">Sitemap</a></li>
	   <li
       %if action == 'Graph':
     class='active'
       %end
					><a href="/graph">Graph</a></li>
       <li
       %if action == 'log':
     class='active'
       %end
					><a href="/log">Log</a></li>

                </div>
                <!--/.nav-collapse -->
            </div>
	   </div>
	</div>
</div>
