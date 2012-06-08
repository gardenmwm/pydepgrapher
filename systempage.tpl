<HTML>
<TITLE>Dependencies for {{system}}</TITLE>
<Body>
<a href=maps/deps{{system}}.png><img src=maps/deps{{system}}.png width=600 height=500></a>
<a href=maps/reqs{{system}}.png><img src=maps/reqs{{system}}.png width=600 height=500></a>
<table><tr><td>Depends</td></tr>
%for node in deps:
	<tr><td><a href='./{{node}}'>{{node}}</a></tr></td>
%end
</table>
<table><tr><td>Reqs</td></tr>
%for node in reqs:
	<tr><td><a href='./{{node}}'>{{node}}</a></tr></td>
%end
</table>
</body>
</html>