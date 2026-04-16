fetch('./src/actividades.json')
  .then(res => res.json())
  .then(data => {
    const grid = document.querySelector('.grid-actividades');
    const actividades = data.actividades.sort((b,a) => a.id - b.id).slice(0,4);
    actividades.forEach(act => {
      const tarjeta = document.createElement('div');
      tarjeta.className = 'tarjeta';
      tarjeta.innerHTML = `
        <a href="${act.url}">
          <img src="${act.imagen}" alt="${act.titulo}">
          <p>${act.titulo}</p>
        </a>
      `;
      grid.appendChild(tarjeta);
    });
  })
  .catch(err => console.error('Error al cargar actividad: ', err));