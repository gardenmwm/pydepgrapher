<HTML>
<TITLE>Dependencies for {{system}}</TITLE>
<Body>
<table border=1><tr><td>Dependent Systems</td><td>Required Systems</td>
<tr><td><a href=maps/deps{{system}}.png><img src=maps/deps{{system}}.png width=600 height=500></a></td><td>
<a href=maps/reqs{{system}}.png><img src=maps/reqs{{system}}.png width=600 height=500></a><td></tr>
<tr><td>Dependant Systems</td><Td>Required Systems</td></tr>
%for i in range(len(deps) if len(deps) > len(reqs) else len(reqs)):
	%dep=deps[i] if len(deps) > i else ''
	%req=reqs[i] if len(reqs) > i else '' 
	<tr>
	<td><a href='./{{dep}}'>{{dep}}</a></td>
	<td><a href='./{{req}}'>{{req}}</a></td>
	<tr>
%end
</table>
</body>
</html>