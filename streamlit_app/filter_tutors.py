import pandas as pd 
from bs4 import BeautifulSoup
import requests

url = 'https://care.grainger.illinois.edu/tutoring/tutors'

response = requests.get(url)

# soup = BeautifulSoup(response.text, 'html.parser')
# print(soup.prettify())



raw_html = """<div class="sm-paginated-list-items directory-list directory-list-3"><div class="item person" id="id68071" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=95908&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/aarnav" class="stretched-link">Aarnav</a></div>
		<div class="title">Physics</div>
	</div>
</div><div class="item person" id="id67407" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=94150&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/aaron" class="stretched-link">Aaron</a></div>
		<div class="title">Physics</div>
	</div>
</div><div class="item person" id="id73094" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=104865&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/adelaide" class="stretched-link">Adelaide</a></div>
		<div class="title">Materials Science and Engineering</div>
	</div>
</div><div class="item person" id="id80448" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=117241&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/aditya" class="stretched-link">Aditya</a></div>
		<div class="title">Neural Engineering</div>
	</div>
</div><div class="item person" id="id76005" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=108780&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/aidan" class="stretched-link">Aidan</a></div>
		<div class="title">Aerospace Engineering</div>
	</div>
</div><div class="item person" id="id75996" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=107400&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/akshay" class="stretched-link">Akshay</a></div>
		<div class="title">Mechanical Engineering</div>
	</div>
</div><div class="item person" id="id63312" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=87679&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/alex_g" class="stretched-link">Alex G.</a></div>
		<div class="title">Civil and Environmental Engineering</div>
	</div>
</div><div class="item person" id="id68610" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=95537&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/alex_s" class="stretched-link">Alex S.</a></div>
		<div class="title">Physics</div>
	</div>
</div><div class="item person" id="id73031" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=101504&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/aman" class="stretched-link">Aman</a></div>
		<div class="title">Mechanical Engineering</div>
	</div>
</div><div class="item person" id="id80470" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=117343&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/amy" class="stretched-link">Amy</a></div>
		<div class="title">Civil and Environmental Engineering</div>
	</div>
</div><div class="item person" id="id76030" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=108131&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/andy" class="stretched-link">Andy</a></div>
		<div class="title">Bioengineering</div>
	</div>
</div><div class="item person" id="id67355" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=94067&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/anthony" class="stretched-link">Anthony</a></div>
		<div class="title">Civil and Environmental Engineering</div>
	</div>
</div></div><div class="sm-paginated-list-items directory-list directory-list-3"><div class="item person" id="id63302" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=88132&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/aparna" class="stretched-link">Aparna</a></div>
		<div class="title">Physics</div>
	</div>
</div><div class="item person" id="id76006" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=108899&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/avni" class="stretched-link">Avni</a></div>
		<div class="title">Bioengineering</div>
	</div>
</div><div class="item person" id="id67347" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=94061&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/ben" class="stretched-link">Ben</a></div>
		<div class="title">Aerospace Engineering</div>
	</div>
</div><div class="item person" id="id57108" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=81543&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/camila" class="stretched-link">Camila</a></div>
		<div class="title">Civil and Environmental Engineering</div>
	</div>
</div><div class="item person" id="id76008" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=107255&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/camille_w" class="stretched-link">Camille W.</a></div>
		<div class="title">Computer Engineering</div>
	</div>
</div><div class="item person" id="id56816" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=81007&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/charlie" class="stretched-link">Charlie</a></div>
		<div class="title">Aerospace Engineering</div>
	</div>
</div><div class="item person" id="id67559" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=94375&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/clive" class="stretched-link">Clive</a></div>
		<div class="title">Civil and Environmental Engineering</div>
	</div>
</div><div class="item person" id="id63300" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=95068&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/david" class="stretched-link">David</a></div>
		<div class="title">Physics</div>
	</div>
</div><div class="item person" id="id76001" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=108516&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/diego" class="stretched-link">Diego</a></div>
		<div class="title">Mechanical Engineering</div>
	</div>
</div><div class="item person" id="id73037" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=101636&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/emma" class="stretched-link">Emma</a></div>
		<div class="title">Chemical Engineering</div>
	</div>
</div><div class="item person" id="id72928" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=101318&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/eric_j" class="stretched-link">Eric J. </a></div>
		<div class="title">CS+Math</div>
	</div>
</div><div class="item person" id="id80536" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=117467&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/francesco" class="stretched-link">Francesco</a></div>
		<div class="title">Aerospace Engineering</div>
	</div>
</div></div><div class="sm-paginated-list-items directory-list directory-list-3"><div class="item person" id="id57086" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=81490&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/gabe" class="stretched-link">Gabe</a></div>
		<div class="title">Civil and Environmental Engineering</div>
	</div>
</div><div class="item person" id="id63297" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=111500&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/geo" class="stretched-link">Geo</a></div>
		<div class="title">Systems Engineering and Design</div>
	</div>
</div><div class="item person" id="id56863" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=81204&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/grace" class="stretched-link">Grace</a></div>
		<div class="title">Mechanical Engineering</div>
	</div>
</div><div class="item person" id="id73035" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=101525&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/hriday" class="stretched-link">Hriday</a></div>
		<div class="title">Electrical Engineering</div>
	</div>
</div><div class="item person" id="id67373" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=94097&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/jacob" class="stretched-link">Jacob</a></div>
		<div class="title">Materials Science and Engineering</div>
	</div>
</div><div class="item person" id="id80452" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=117247&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/jaylin" class="stretched-link">Jaylin </a></div>
		<div class="title">Electrical Engineering</div>
	</div>
</div><div class="item person" id="id73034" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=101512&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/jiya" class="stretched-link">Jiya</a></div>
		<div class="title">Materials Science and Engineering</div>
	</div>
</div><div class="item person" id="id73036" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=101527&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/johail" class="stretched-link">Johail</a></div>
		<div class="title">Computer Engineering</div>
	</div>
</div><div class="item person" id="id68730" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=95596&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/johan" class="stretched-link">Johan</a></div>
		<div class="title">Electrical Engineering</div>
	</div>
</div><div class="item person" id="id80445" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=117207&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/kimaya" class="stretched-link">Kimaya</a></div>
		<div class="title">Chemical Engineering</div>
	</div>
</div><div class="item person" id="id76000" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=95596&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/kristie" class="stretched-link">Kristie</a></div>
		<div class="title">Computer Engineering</div>
	</div>
</div><div class="item person" id="id76007" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=108129&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/liz" class="stretched-link">Liz</a></div>
		<div class="title">Electrical Engineering</div>
	</div>
</div></div><div class="sm-paginated-list-items directory-list directory-list-3"><div class="item person" id="id73132" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=102355&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/logan" class="stretched-link">Logan</a></div>
		<div class="title">Nuclear Plasma &amp; Radiological Engineering</div>
	</div>
</div><div class="item person" id="id67614" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=94984&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/lucas" class="stretched-link">Lucas</a></div>
		<div class="title">Mechanical Engineering</div>
	</div>
</div><div class="item person" id="id56833" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=81034&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/lucy" class="stretched-link">Lucy</a></div>
		<div class="title">Materials Science and Engineering</div>
	</div>
</div><div class="item person" id="id72835" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=101252&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/lucy_p" class="stretched-link">Lucy P.</a></div>
		<div class="title">Engineering Mechanics</div>
	</div>
</div><div class="item person" id="id72932" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=101295&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/luke" class="stretched-link">Luke</a></div>
		<div class="title">Physics</div>
	</div>
</div><div class="item person" id="id67940" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=94886&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/lydia" class="stretched-link">Lydia</a></div>
		<div class="title">Engineering Mechanics</div>
	</div>
</div><div class="item person" id="id72930" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=101317&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/maheen" class="stretched-link">Maheen</a></div>
		<div class="title">Aerospace Engineering</div>
	</div>
</div><div class="item person" id="id67720" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=94730&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/maria" class="stretched-link">Maria</a></div>
		<div class="title">Mechanical Engineering</div>
	</div>
</div><div class="item person" id="id67737" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=94751&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/meredith" class="stretched-link">Meredith</a></div>
		<div class="title">Mechanical Engineering</div>
	</div>
</div><div class="item person" id="id72914" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=101296&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/nehan" class="stretched-link">Nehan</a></div>
		<div class="title">Computer Science</div>
	</div>
</div><div class="item person" id="id75998" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=108230&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/nico" class="stretched-link">Nico</a></div>
		<div class="title">Mechanical Engineering</div>
	</div>
</div><div class="item person" id="id73096" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=101586&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/noah" class="stretched-link">Noah</a></div>
		<div class="title">Electrical Engineering</div>
	</div>
</div></div><div class="sm-paginated-list-items directory-list directory-list-3"><div class="item person" id="id75999" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=110127&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/pat" class="stretched-link">Pat</a></div>
		<div class="title">Civil and Environmental Engineering</div>
	</div>
</div><div class="item person" id="id67585" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=94463&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/regina" class="stretched-link">Regina</a></div>
		<div class="title">Materials Science and Engineering</div>
	</div>
</div><div class="item person" id="id80451" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=117361&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/rodrigo" class="stretched-link">Rodrigo</a></div>
		<div class="title">Mechanical Engineering</div>
	</div>
</div><div class="item person" id="id56803" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=80883&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/rohan" class="stretched-link">Rohan</a></div>
		<div class="title">Mechanical Engineering</div>
	</div>
</div><div class="item person" id="id73032" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=101505&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/sarah" class="stretched-link">Sarah</a></div>
		<div class="title">Electrical Engineering</div>
	</div>
</div><div class="item person" id="id57107" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=81540&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/sean" class="stretched-link">Sean</a></div>
		<div class="title">Bioengineering</div>
	</div>
</div><div class="item person" id="id80453" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=117363&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/serge" class="stretched-link">Serge</a></div>
		<div class="title">Physics</div>
	</div>
</div><div class="item person" id="id80466" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=117333&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/siddh" class="stretched-link">Siddh</a></div>
		<div class="title">Computer Engineering</div>
	</div>
</div><div class="item person" id="id57106" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=94988&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/sophia" class="stretched-link">Sophia</a></div>
		<div class="title">Bioengineering</div>
	</div>
</div><div class="item person" id="id67348" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=96108&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/sushrut" class="stretched-link">Sushrut</a></div>
		<div class="title">Computer Engineering</div>
	</div>
</div><div class="item person" id="id73152" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=101638&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/teddy" class="stretched-link">Teddy</a></div>
		<div class="title">Bioengineering</div>
	</div>
</div><div class="item person" id="id80454" data-items="12">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=117248&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/tommy" class="stretched-link">Tommy</a></div>
		<div class="title">Mechanical Engineering</div>
	</div>
</div></div><div class="sm-paginated-list-items directory-list directory-list-3"><div class="item person" id="id77093" data-items="3">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=109379&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/yaseen" class="stretched-link">Yaseen</a></div>
		<div class="title">Aerospace Engineering</div>
	</div>
</div><div class="item person" id="id76002" data-items="3">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=108587&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/yashwanth" class="stretched-link">Yash</a></div>
		<div class="title">Mechanical Engineering</div>
	</div>
</div><div class="item person" id="id57090" data-items="3">
	<div class="photo" style="background-image: url(/_sitemanager/viewphoto.aspx?id=95970&amp;s=300)"></div>
	<div class="details">
		<div class="name"><a href="/tutoring/tutors/zaahi" class="stretched-link">Zaahi</a></div>
		<div class="title">Mechanical Engineering</div>
	</div>
</div></div>"""
soup = BeautifulSoup(raw_html, 'html.parser')
stretched_links = soup.find_all("a", class_="stretched-link")
names = [tag.contents[0] for tag in stretched_links]
print(names)

df = pd.read_csv('/Users/seanguno/Documents/senior year/tutor tribe project/Tutor-tribe SP26/data-Table 1.csv')
df_renamed = df.rename({"PageTitle" : "Name", "FieldValue" : "Course"}, axis=1)
df_core_columns = df_renamed.drop(columns=["PageID", "Unnamed: 3", "Unnamed: 4"])
df_filtered = df_core_columns[df_core_columns["Name"].isin(names)]
df_francesco = pd.DataFrame([{'Name': 'Francesco', 'Course' : 'MATH 285'}, {'Name': 'Francesco', 'Course' : 'MATH 415'}, {'Name': 'Francesco', 'Course' : 'PHYS 211'},
                {'Name': 'Francesco', 'Course' : 'PHYS 212'}, {'Name': 'Francesco', 'Course' : 'ECE 205'}, {'Name': 'Francesco', 'Course' : 'TAM 210'}])
df_final = pd.concat([df_filtered, df_francesco], ignore_index=True)
print(df_final['Name'].nunique())
print(df_final[df_final['Name'] == "Sean"])
df_final = df_final.rename({"Name" : "PageTitle", "Course" : "FieldValue"}, axis=1)
print(df_final) 
df_final = df_final.drop(range(550, 558))
print(df_final[df_final['PageTitle'] == "Sean"])
df_final.to_csv('updated_tutor_course_list.csv', index=False)
# print(df_filtered[df_filtered['Name'] == 'Eric J.'])
# print(df_filtered['Name'].unique())
# print(df_filtered['Name'].nunique())
# print(len(names))
# print(type(df))
# print(df['PageTitle'].nunique())
