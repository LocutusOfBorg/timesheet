<!DOCTYPE html>
<html>
  <head>
    <title></title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- Bootstrap -->
    <link rel="icon" href="/static/images/favicon.ico" />
    <link href="/static/css/bootstrap.min.css" rel="stylesheet" media="screen">
    <link rel='stylesheet' type='text/css' href='/static/css/redmond/jquery-ui-1.10.3.custom.min.css' />
    <link href="/static/css/timesheet.css" rel="stylesheet" media="screen">
    <!-- JavaScript plugins (requires jQuery) -->
    <script src="/static/js/jquery-1.10.2.js"></script>
    <script src="/static/js/json2.js"></script>
    <script src="/static/js/jquery-ui-1.10.3.custom.min.js"></script>
    <script src="/static/js/jquery.validate.min.js"></script>
    <script src="/static/js/common.js"></script>
  </head>
  <body>
<div class="row">
<div class="col-lg-4"><h2>Timesheet</h2></div>
<div class="col-lg-4">
<div id="msgbox"></div>
</div>
</div>
<div class="row">
    <div class="col-lg-2">
<ul class="nav nav-pills nav-stacked">
  <li>
    <a href="#">
      <span class="badge pull-right">5</span>
      Notifiche
    </a>
  </li>
  <li class="${'active' if view == 'calendar' else ''}">
    <a href="/index/calendar">
      Consuntivazione
    </a>
  </li>
      <li class="${'active' if view == 'trips' else ''} dropdown">
	<a href="#" data-toggle="dropdown" role="button">Trasferte<b class="caret"></b></a>
        <ul aria-labelledby="drop4" role="menu" class="dropdown-menu" id="menurep">
            <li role="presentation"><a href="#" tabindex="-1" role="menuitem">Nuova richiesta</a></li>
            <li role="presentation"><a href="#" tabindex="-1" role="menuitem">In approvazione</a></li>
	    <li class="divider" role="presentation"></li>
            <li role="presentation"><a href="/index/trips" tabindex="-1" role="menuitem">Elenco</a></li>
        </ul>

    </a>
  </li>
<li class="${'active' if view == 'expences' else ''}">
    <a href="#">
      Note spese
    </a>
  </li>
<li>
  <a href="/auth/logout">Logout</a>
</li>
## TODO: add project managers menu view
% if group == 'administrator':
	
	<li><hr></li>
	 <li class="${'active' if view == 'report' else ''} dropdown">
	    <a href="#" data-toggle="dropdown" role="button">Report<b class="caret"></b></a>
		<ul aria-labelledby="drop4" role="menu" class="dropdown-menu" id="menurep">
	            <li role="presentation"><a href="/index/reports" tabindex="-1" role="menuitem">By user</a></li>
	            <li role="presentation"><a href="/index/reports_prj" tabindex="-1" role="menuitem">By project</a></li>
	            <li role="presentation"><a href="#" tabindex="-1" role="menuitem">Per cliente</a></li>
	            <li class="divider" role="presentation"></li>
	            <li role="presentation"><a href="#" tabindex="-1" role="menuitem">Totale mese</a></li>
	        </ul>
	  </li>
	  <li class="${'active' if view == 'customers' else ''} dropdown">
	    <a href="#" data-toggle="dropdown" role="button">Customers<b class="caret"></b></a>
		<ul aria-labelledby="drop4" role="menu" class="dropdown-menu" id="menucust">
	            <li role="presentation"><a href="#" tabindex="-1" role="menuitem">Aggiungi</a></li>
	            <li role="presentation"><a href="#" tabindex="-1" role="menuitem">Elimina</a></li>
	            <li class="divider" role="presentation"></li>
	            <li role="presentation"><a href="/index/customers" tabindex="-1" role="menuitem">List</a></li>
	        </ul>
	  </li>
	<li class="${'active' if view == 'projects' else 'active' if view == 'offers' else ''} dropdown">
	    <a href="#" data-toggle="dropdown" role="button">Projects<b class="caret"></b></a>
		<ul aria-labelledby="drop4" role="menu" class="dropdown-menu" id="menucust">
	            <li role="presentation"><a href="/index/projects" tabindex="-1" role="menuitem">List</a></li>
	            <li role="presentation"><a href="/index/offers" tabindex="-1" role="menuitem">Offers</a></li>
	        </ul>
	  </li>
	<li class="${'active' if view == 'users' else ''}">
	    <a href="/index/users">
	      Users
	    </a>
	  </li>
	  <li class="${'active' if view == 'invoice' else ''} dropdown">
	    <a href="#" data-toggle="dropdown" role="button">Fatture<b class="caret"></b></a>
		<ul aria-labelledby="drop4" role="menu" class="dropdown-menu" id="menuin">
	            <li role="presentation"><a href="#" tabindex="-1" role="menuitem">Crea Nuova</a></li>
	            <li role="presentation"><a href="#" tabindex="-1" role="menuitem">Visualizza esistenti</a></li>
	        </ul>
	  </li>

% endif

</ul>




</div>
<div class="col-lg-9">
  ${view_page}
</div>
</div>  

    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="/static/js/bootstrap.min.js"></script>
    <script src="/static/js/fullcalendar.min.js"></script>
    <!-- Enable responsive features in IE8 with Respond.js (https://github.com/scottjehl/Respond) 
    <script src="/static/js/respond.js"></script> -->
  </body>
</html>

