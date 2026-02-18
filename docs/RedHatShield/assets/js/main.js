const PATTERN_VIDEO = /\/videos\.html$/;
const PATTERN_TRANSCRIPT = /_TS\.html$/;

document.addEventListener("DOMContentLoaded", function() {
    const sidebar = document.getElementById('sidebar');
    const toggleBtn = document.getElementById('menu-toggle');
    const overlay = document.getElementById('sidebar-overlay');

    // 1. Menü laden und aktiven Link markieren
	fetch('menu.html')
		.then(response => response.text())
		.then(data => {
			sidebar.innerHTML = data;

			// Hilfsfunktion, um "index.html" am Ende zu entfernen
			const normalize = (url) => url.replace(/index\.html$/, '').replace(/\/$/, '');

			// Aktuelle URL normalisieren
			const currentLoc = normalize(window.location.href.split('#')[0].split('?')[0]);
			const isTranscipt = PATTERN_TRANSCRIPT.test(currentLoc);

			const navLinks = sidebar.querySelectorAll('a');
			navLinks.forEach(link => {
				// Die absolute URL des Links normalisieren
				const linkLoc = normalize(link.href);
				const isVideo = PATTERN_VIDEO.test(linkLoc);

				if (linkLoc === currentLoc) {
					link.classList.add('active-link');
					
					// NEU: Den übergeordneten Hauptpunkt markieren
					const parentSubmenu = link.closest('.has-submenu');
					if (parentSubmenu) {
						parentSubmenu.classList.add('child-active');
					}
				}

				if (isVideo && isTranscipt) {
					link.classList.add('active-transcript-link');
				}
			});

			// Prüfe, ob ein aktiver Link in einem Submenü steckt
			const activeSubLink = sidebar.querySelector('.submenu a.active-link');
			if (activeSubLink) {
				// Wenn ja, finde das übergeordnete Submenü und öffne es
				activeSubLink.closest('.has-submenu').classList.add('open');
			}

			// NEU: Submenü-Logik
			const toggles = sidebar.querySelectorAll('.submenu-toggle');
			toggles.forEach(toggle => {
				toggle.addEventListener('click', function(e) {
					e.preventDefault(); // Verhindert das Springen der Seite
					const parent = this.parentElement;
					parent.classList.toggle('open');
				});
			});
		});
		
    function toggleMenu() {
        if (window.innerWidth > 768) {
            sidebar.classList.toggle('hidden');
        } else {
            sidebar.classList.toggle('active');
        }
    }

    // Toggle bei Button-Klick
    toggleBtn.addEventListener('click', toggleMenu);

    // Schließen bei Klick auf Overlay (Mobile)
    overlay.addEventListener('click', () => {
        sidebar.classList.remove('active');
    });
});