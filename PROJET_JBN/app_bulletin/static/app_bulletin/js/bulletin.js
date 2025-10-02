document.addEventListener('DOMContentLoaded', ()=>{

  const tbody = document.querySelector("#listeBulletin tbody");
  const bulletinPage = document.getElementById('bulletinPage');
  const listeContainer = document.getElementById('listeContainer');
  const logoCachetContainer = document.getElementById('logoCachetContainer');
  const btnAfficherFormulaire = document.getElementById('btnAfficherFormulaire');
  const formulairePage = document.getElementById('formulairePage');
  const inputCodeForm = document.getElementById('inputCodeForm');
  const btnValiderForm = document.getElementById('btnValiderForm');
  const btnRetourForm = document.getElementById('btnRetourForm');

  function afficherBulletin(nom, prenom, classe, logo='logo_ecole.png', cachet='cachet_directeur.png'){
    listeContainer.style.display = 'none';
    formulairePage.style.display = 'none';
    btnAfficherFormulaire.style.display = 'inline-block';
    bulletinPage.innerHTML = `
      <img id="bulletinLogo" src="${logo}" alt="Logo École" style="max-width:150px;margin-bottom:10px;">
      <h3>Bulletin de ${nom} ${prenom} | Classe: ${classe}</h3>
      <table border="1" style="width:100%;margin-top:10px">
        <thead><tr><th>Matière</th><th>Coef</th><th>Note</th><th>Pondérée</th></tr></thead>
        <tbody>
          <tr><td>Mathématiques</td><td>4</td><td>15</td><td>60</td></tr>
          <tr><td>Français</td><td>3</td><td>14</td><td>42</td></tr>
          <tr><td>Anglais</td><td>2</td><td>16</td><td>32</td></tr>
        </tbody>
        <tfoot>
          <tr><td colspan="3">Total</td><td>134</td></tr>
          <tr><td colspan="3">Moyenne</td><td>14.89 (Bien)</td></tr>
        </tfoot>
      </table>
      <img id="bulletinCachet" src="${cachet}" alt="Cachet Directeur" style="max-width:150px;margin-top:10px;">
      <div style="margin-top:10px">
        <button onclick="window.print()">Imprimer / PDF</button>
      </div>
      <div>
        <button id="btnRetour">Retour à la liste</button>
      </div>
    `;

    logoCachetContainer.innerHTML = `
      <input type="file" id="logoChoix" accept="image/*">
      <input type="file" id="cachetChoix" accept="image/*">
    `;

    document.getElementById('btnRetour').addEventListener('click', ()=>{
      bulletinPage.innerHTML = '';
      logoCachetContainer.innerHTML = '';
      listeContainer.style.display = 'block';
    });

    document.getElementById('logoChoix').addEventListener('change', e=>{
      const file = URL.createObjectURL(e.target.files[0]);
      document.getElementById('bulletinLogo').src = file;
    });

    document.getElementById('cachetChoix').addEventListener('change', e=>{
      const file = URL.createObjectURL(e.target.files[0]);
      document.getElementById('bulletinCachet').src = file;
    });
  }

  tbody.addEventListener('click', e=>{
    if(e.target.classList.contains('btnRechercher')){
      const tr = e.target.parentElement.parentElement;
      const nom = tr.children[1].textContent;
      const prenom = tr.children[2].textContent;
      const classe = tr.children[3].textContent;
      afficherBulletin(nom, prenom, classe);
      logoCachetContainer.innerHTML = '';
      btnAfficherFormulaire.style.display = 'none';
    }
  });

  btnAfficherFormulaire.addEventListener('click', ()=>{
    formulairePage.style.display = 'block';
    inputCodeForm.focus();
    listeContainer.style.display = 'none';
    bulletinPage.innerHTML = '';
    btnAfficherFormulaire.style.display = 'none';
  });

  btnValiderForm.addEventListener('click', ()=>{
    const code = inputCodeForm.value.trim();
    if(!code) return alert("Entrez le code de l'élève !");
    const tr = Array.from(tbody.children).find(tr=>tr.children[0].textContent===code);
    if(!tr) return alert("Élève non trouvé !");
    const nom = tr.children[1].textContent;
    const prenom = tr.children[2].textContent;
    const classe = tr.children[3].textContent;
    afficherBulletin(nom, prenom, classe);
  });

  btnRetourForm.addEventListener('click', ()=>{
    formulairePage.style.display = 'none';
    listeContainer.style.display = 'block';
    btnAfficherFormulaire.style.display = 'inline-block';
  });

});
