<h1>Problem</h1>

<p>Something went wrong or you have arrived at a page that doesn't exist</p>

<p>{{ error.body }}</p>

%if error.exception != None:
  <p>{{ error.exception }}</p>
%end

%rebase base title='Something went wrong', action='error'
