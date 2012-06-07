<HTML>
<TITLE>Dependencies for {{system}}</TITLE>
<Body>
<a href=maps/{{system}}.png><img src=maps/{{system}}.png width=600 height=500></a>
<table><tr><td>Depends</td></tr>
%for node in deps:
	<tr><td><a href='./{{node}}'>{{node}}</a></tr></td>
%end
</table>
</body>
</html>