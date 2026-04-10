document.addEventListener('DOMContentLoaded', function() {
  const container = document.getElementById('hal-publications');
  if (!container) return;

  container.innerHTML = '<p class="text-neutral-600 dark:text-neutral-400">Chargement des publications...</p>';

  fetch('https://api.archives-ouvertes.fr/search/?q=ANR-22-EXEN-0002&fq=anrProjectAcronym_s:CATS&wt=json&rows=30')
    .then(response => {
      if (!response.ok) throw new Error(`Erreur HTTP: ${response.status}`);
      return response.json();
    })
    .then(data => {
      if (!data.response?.docs || data.response.docs.length === 0) {
        container.innerHTML = '<p class="text-neutral-600 dark:text-neutral-400">Aucune publication trouvée.</p>';
        return;
      }

      let html = '<ul class="space-y-4">';

      data.response.docs.forEach(pub => {
        // Extraire les auteurs depuis label_s
        const authors = extractAuthors(pub.label_s);

        // Extraire le titre (après le premier ".")
        const title = pub.label_s?.split('.').slice(1).join('.').trim() || 'Sans titre';

        html += `
          <li class="p-4 bg-neutral-50 dark:bg-neutral-800 rounded-lg shadow-sm">
            <a
              href="https://hal.science/${pub.halId_s || pub.docid}"
              target="_blank"
              rel="noopener"
              class="text-lg font-semibold text-primary-600 dark:text-primary-400 hover:underline">
              ${title}
            </a>
            <div class="mt-2 text-sm text-neutral-600 dark:text-neutral-400">
              ${authors}
            </div>
          </li>
        `;
      });

      html += '</ul>';
      container.innerHTML = html;
    })
    .catch(error => {
      console.error('Erreur HAL:', error);
      container.innerHTML = `
        <div class="p-4 bg-red-50 dark:bg-red-900/20 rounded-lg">
          <p class="text-red-600 dark:text-red-400">
            Erreur de chargement : ${error.message}
          </p>
        </div>
      `;
    });

  // Fonction pour extraire les auteurs
  function extractAuthors(label) {
    if (!label) return 'Auteur inconnu';
    const authorsPart = label.split('.')[0];
    return authorsPart.trim() || 'Auteur inconnu';
  }
});